import pandas as pd
import sqlite3
import json

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
    """
    Remove participants with mean reliability < 0 across repeat trials.
    Compares responses to the same stimulus in original vs. repeat trials.
    """
    # Get all repeat trials and their original counterparts
    repeat_trials = df[df['repeat'] == True]
    original_trials = df[df['repeat'] == False]
    
    reliability_scores = {}
    
    for worker_id in df['worker_id'].unique():
        worker_repeats = repeat_trials[repeat_trials['worker_id'] == worker_id]
        worker_originals = original_trials[original_trials['worker_id'] == worker_id]
        
        scores = []
        
        for _, repeat_row in worker_repeats.iterrows():
            stimulus_num = repeat_row['stimulus_number']
            repeat_response = repeat_row['response_label']
            
            # Find the original trial for this stimulus
            original_response = worker_originals[
                worker_originals['stimulus_number'] == stimulus_num
            ]['response_label'].values
            
            if len(original_response) > 0:
                original_response = original_response[0]
                
                # Skip "not sure" responses
                if repeat_response == "not sure" or original_response == "not sure":
                    continue
                
                # Score +1 if consistent, -1 if inconsistent
                score = 1 if repeat_response == original_response else -1
                scores.append(score)
        
        # Calculate mean reliability (if any valid comparisons exist)
        if scores:
            mean_reliability = sum(scores) / len(scores)
            reliability_scores[worker_id] = mean_reliability
    
    # Filter participants with mean reliability >= 0
    passed_participants = [
        worker_id for worker_id, score in reliability_scores.items() 
        if score >= 0
    ]
    
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

if __name__ == "__main__":
    create_output_files()