import pandas as pd
import sqlite3
import json
import numpy as np
import os
from pathlib import Path


def process_data_table(conn):
    try:
        # Get the raw data
        df = pd.read_sql_query('SELECT * FROM Data', conn)
        
        # First, export the original Data table as Data.csv
        df.to_csv('Data.csv', index=False)
        print('✓ Successfully exported original data to Data.csv')
        
        all_trials = []
        
        for _, row in df.iterrows():
            # Get basic info
            trial_info = {
                'worker_id': str(row.get('worker_id', '')),
                'condition': str(row.get('condition', '')),
                'database_id': str(row.get('id', ''))
            }
            
            json_str = row.get('json_data', None)
            if json_str and isinstance(json_str, str):
                try:
                    # Parse JSON while keeping numbers as strings
                    trials = json.loads(json_str, parse_float=str, parse_int=str)
                    if not isinstance(trials, list):
                        trials = [trials]
                    
                    for trial in trials:
                        if not isinstance(trial, dict):
                            continue
                            
                        flat_trial = trial_info.copy()
                        
                        for key, value in trial.items():
                            # Force seed and similar fields to remain as strings
                            if key == 'seed' or (isinstance(value, (int, float)) and value > 1e12):
                                value = str(value)
                            elif isinstance(value, str) and value.isdigit() and len(value) > 12:
                                value = str(value)
                            
                            if isinstance(value, (list, dict)):
                                flat_trial[key] = json.dumps(value)
                            else:
                                flat_trial[key] = value
                        
                        all_trials.append(flat_trial)
                        
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    continue
    
        if all_trials:
            expanded_df = pd.DataFrame(all_trials)
            
            # Convert numeric columns (except seed/large numbers) to appropriate types
            numeric_cols = ['rt', 'time_elapsed', 'total_time']
            for col in numeric_cols:
                if col in expanded_df.columns:
                    try:
                        expanded_df[col] = pd.to_numeric(expanded_df[col])
                    except (ValueError, TypeError):
                        pass
            
            return expanded_df
        return pd.DataFrame()
    
    except Exception as e:
        print(f"Error in process_data_table: {e}")
        raise

def screen_size_check(df):
    """Remove participants with screen_width < 800 and screen_height < 600."""

    screen_trials = df[df['trial_type'] == 'fullscreen'].dropna(subset=['screen_width', 'screen_height'])
    
    # Convert to numeric
    screen_trials['screen_width'] = pd.to_numeric(screen_trials['screen_width'], errors='coerce')
    screen_trials['screen_height'] = pd.to_numeric(screen_trials['screen_height'], errors='coerce')
    
    # Find participants who have at least one trial with acceptable screen size
    passed_participants = screen_trials[
        (screen_trials['screen_width'] >= 800) & 
        (screen_trials['screen_height'] >= 600)
    ]['worker_id'].unique()
    
    # Filter original dataframe to only include these participants
    return df[df['worker_id'].isin(passed_participants)]

def seriousness_self_report_check(df):
    """Remove participants with seriousness < 70 in form_data."""
    # Find all survey trials with form_data
    survey_trials = df[df['trial_type'] == 'render-mustache-template'].dropna(subset=['form_data'])
    
    def check_seriousness(form_data):
        if isinstance(form_data, str):
            try:
                data = json.loads(form_data)
                seriousness = data.get('seriousness', '')
                if isinstance(seriousness, str) and seriousness.isdigit():
                    return int(seriousness) >= 70
                return False
            except (json.JSONDecodeError, AttributeError):
                return False
        return False
    
    # Find participants who passed the seriousness check
    passed_participants = survey_trials[
        survey_trials['form_data'].apply(check_seriousness)
    ]['worker_id'].unique()
    
    # Filter original dataframe to only include these participants
    return df[df['worker_id'].isin(passed_participants)]

def response_reliability_check(df):
    """Correlation-style reliability (-1 to +1) where:
    +1 = perfect consistency
    0 = random responding
    -1 = perfect inconsistency
    """
    reliability_scores = {}
    
    for worker_id in df['worker_id'].unique():
        worker_data = df[df['worker_id'] == worker_id]
        repeats = worker_data[worker_data['repeat'] == True]
        originals = worker_data[worker_data['repeat'] == False]
        
        if len(repeats) == 0:
            continue  # Skip workers with no repeats
            
        comparisons = []
        
        for _, repeat_row in repeats.iterrows():
            stim_num = repeat_row['stimulus_number']
            original_responses = originals[originals['stimulus_number'] == stim_num]['response_label']
            
            if len(original_responses) > 0:
                original = original_responses.values[0]
                repeat = repeat_row['response_label']
                
                # Skip non-binary responses for correlation
                if pd.isna(original) or pd.isna(repeat):
                    continue
                    
                # Score +1 if match, -1 if mismatch
                comparisons.append(1 if original == repeat else -1)
        
        if comparisons:
            reliability_scores[worker_id] = sum(comparisons) / len(comparisons)
    
    # Filter participants with positive reliability
    passed_participants = [wid for wid, score in reliability_scores.items() if score > 0]
    
    print(f"Reliability distribution (n={len(reliability_scores)}):")
    print(pd.Series(reliability_scores).describe())
    
    return df[df['worker_id'].isin(passed_participants)]



def create_output_files():
    database_path = 'database.db'
    
    with sqlite3.connect(database_path) as conn:
        # Process Participant table
        try:
            participant_df = pd.read_sql_query('SELECT * FROM Participant', conn)
            participant_df.to_csv('Participant.csv', index=False)
            print('✓ Successfully exported Participant to Participant.csv')
        except Exception as e:
            print(f"Error exporting Participant table: {e}")
        
        # Process Data table
        try:
            expanded_df = process_data_table(conn)
            print("Original DataFrame:")
            print(expanded_df.head())
            print(f"Total records before checks: {len(expanded_df)}")
            
            if not expanded_df.empty:
                expanded_df.to_csv(
                    'Data_expanded.csv',
                    index=False,
                    quoting=1,
                    encoding='utf-8-sig'
                )
                print('✓ Successfully exported complete Data_expanded.csv')
                
                # screen size check
                after_screen_check = screen_size_check(expanded_df)
                print(f"Records after screen size check: {len(after_screen_check)}")
                
                # seriousness check
                after_all_checks = seriousness_self_report_check(after_screen_check)
                print(f"Records after all checks: {len(after_all_checks)}")

                # creen_size and seriousness checks:
                after_reliability_check = response_reliability_check(after_all_checks)
                print(f"Records after reliability check: {len(after_reliability_check)}")

                # Use after_reliability_check for final exports
                passed_participants = after_reliability_check['worker_id'].unique()
                
                # Save the filtered expanded data
                after_reliability_check.to_csv(
                    'data_expanded_after_checks.csv',
                    index=False,
                    quoting=1,
                    encoding='utf-8-sig'
                )
                print('✓ Successfully exported filtered data_expanded_after_checks.csv')
                
                # Get list of participants who passed all checks
                passed_participants = after_reliability_check['worker_id'].unique()
                
                # Filter Participant table
                passed_participant_df = participant_df[participant_df['worker_id'].isin(passed_participants)]
                passed_participant_df.to_csv('participants_after_checks.csv', index=False)
                print('✓ Successfully exported participants_after_checks.csv')
                
                # Filter original Data table format
                passed_data_df = pd.read_sql_query(
                    'SELECT * FROM Data WHERE worker_id IN ({})'.format(
                        ','.join(['"{}"'.format(p) for p in passed_participants])
                    ), 
                    conn
                )
                passed_data_df.to_csv('data_after_checks.csv', index=False)
                print('✓ Successfully exported data_after_checks.csv')
                
            else:
                print('No trial data found to export')
        except Exception as e:
            print(f"Error processing Data table: {e}")



def calculate_individual_averages(df, condition, latent_dir='latents', output_file='individual_average_latents.csv'):
    
    participant_info = pd.read_csv('Participant.csv')[['anon_id', 'worker_id', 'sona_id']]
    
    results = []
    
    for worker_id, participant_data in df.groupby('worker_id'):
        latent_sums = {
            f'{condition}_average': None,
            f'no_{condition}_average': None,
            'not_sure_average': None
        }
        counts = {
            f'{condition}_average': 0,
            f'no_{condition}_average': 0,
            'not_sure_average': 0
        }
        
        for _, trial in participant_data.iterrows():
            if 'stimulus' not in trial or pd.isna(trial['stimulus']) or 'response' not in trial:
                continue
                
            image_path = trial['stimulus']
            image_name = os.path.basename(image_path)
            
            response = str(trial['response']).lower()
            key_pressed = str(trial.get('key_name', '')).lower()
            
            if response == f"yes {condition}" or key_pressed == 'f':
                avg_key = f'{condition}_average'
            elif response == f"no {condition}" or key_pressed == 'j':
                avg_key = f'no_{condition}_average'
            elif response == "not sure" or key_pressed == 'space':
                avg_key = 'not_sure_average'
            else:
                continue
                
            latent_path = os.path.join(latent_dir, f"{image_name}.npy")
            try:
                latent = np.load(latent_path)
                
                if latent_sums[avg_key] is None:
                    latent_sums[avg_key] = latent.copy()
                else:
                    latent_sums[avg_key] += latent
                    
                counts[avg_key] += 1
            except FileNotFoundError:
                print(f"Warning: Latent file not found for image {image_name}")
                continue
                
        participant_result = {'worker_id': worker_id}
        
        for key in latent_sums:
            if counts[key] > 0:
                participant_result[key] = latent_sums[key] / counts[key]
            else:
                participant_result[key] = None
        
        if (participant_result[f'{condition}_average'] is not None and 
            participant_result[f'no_{condition}_average'] is not None and 
            participant_result['not_sure_average'] is not None):
            
            participant_result['overall_participant_average'] = (
                participant_result[f'{condition}_average'] - 
                participant_result[f'no_{condition}_average'] + 
                participant_result['not_sure_average']
            )
        else:
            participant_result['overall_participant_average'] = None
            
        results.append(participant_result)
    
    results_df = pd.DataFrame(results)
    
    final_df = participant_info.merge(results_df, on='worker_id', how='right')
    
    output_columns = ['anon_id', 'worker_id', 'sona_id', 'overall_participant_average']
    final_df[output_columns].to_csv(output_file, index=False)
    
    print(f"Successfully saved individual averages to {output_file}")
    return final_df

if __name__ == "__main__":
    create_output_files()