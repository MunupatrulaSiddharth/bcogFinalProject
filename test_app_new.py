import os
import json
import random
import string
import uuid
import logging
from datetime import datetime, timedelta, timezone
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_app_debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
base_url = "http://127.0.0.1:8000"
experiment_name = "Mental Representations of Mental Illness in Facial Perception"
version_date = "2023-10-21"

def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_uppercase, k=length))

def generate_participant_info():
    return {
        "worker_id": generate_random_string(),
        "hit_id": "XXX",
        "assignment_id": "XXX",
        "platform": "sona",
    }

def generate_completion_code():
    return f"{random.randint(1000000000, 9999999999)}-exa-{random.randint(1000000000, 9999999999)}-mple"

def generate_realistic_trial_data(worker_id, condition):
    """Generates complete trial data matching the exact required format"""
    anon_id = str(uuid.uuid4())
    completion_code = generate_completion_code()
    seed = random.randint(1000000000000, 9999999999999)
    redirect_url = f"https://uiuc.sona-systems.com/webstudy_credit.aspx?experiment_id=21&credit_token=sss&survey_code={worker_id}"
    
    # Calculate consistent timing
    start_time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    total_time = random.randint(120000, 300000)  # 2-5 minutes in ms
    end_time = (datetime.fromisoformat(start_time.replace('Z', '+00:00')) + 
                timedelta(milliseconds=total_time)).isoformat().replace("+00:00", "Z")
    
    trials = []
    
    # 1. Consent trial
    consent_time = random.randint(50000, 120000)
    trials.append({
        "rt": consent_time,
        "url": "src/html/consent.html",
        "experiment_phase": "consent",
        "refresh_count": random.randint(0, 10),
        "trial_type": "render-mustache-template",
        "trial_index": 0,
        "time_elapsed": consent_time + random.randint(0, 100),
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": [
            {"event": "focus", "time": random.randint(10000, 30000)},
            {"event": "blur", "time": random.randint(40000, 60000)},
            {"event": "focus", "time": random.randint(60000, 80000)}
        ]
    })
    
    # 2. Fullscreen trial
    fullscreen_time = trials[-1]["time_elapsed"] + random.randint(1000, 5000)
    trials.append({
        "success": True,
        "trial_type": "fullscreen",
        "trial_index": 1,
        "time_elapsed": fullscreen_time,
        "screen_width": random.choice([1680, 1920, 1366, 1440,700,600,500]),
        "screen_height": random.choice([1050, 1080, 768, 900,600,700,500]),
        "window_width": random.choice([1536, 1680, 1366]),
        "window_height": random.choice([594, 768, 800]),
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": []
    })
    
    # 3. Attrition trial
    attrition_time = fullscreen_time + random.randint(5000, 10000)
    trials.append({
        "rt": random.randint(5000, 10000),
        "url": "src/html/attrition.html",
        "form_name": "attritionForm",
        "form_id": "#attritionForm",
        "experiment_phase": "attrition",
        "trial_type": "render-mustache-template",
        "trial_index": 2,
        "time_elapsed": attrition_time,
        "instructions_viewed_count": 0,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": [{"event": "fullscreenenter", "time": fullscreen_time + 100}]
    })
    
    # 4. Instructions trial
    view_history = []
    total_view_time = 0
    for i in range(6):
        view_time = random.randint(500, 2500)
        view_history.append({
            "page_index": i,
            "viewing_time": view_time
        })
        total_view_time += view_time
    
    instructions_time = attrition_time + total_view_time
    trials.append({
        "view_history": view_history,
        "rt": total_view_time,
        "trial_type": "instructions",
        "trial_index": 3,
        "time_elapsed": instructions_time,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": []
    })
    
    # 5. Main trials (10 images)
    image_numbers = list(range(10))
    random.shuffle(image_numbers)
    responses = ["f", "j", "space"]
    response_labels = ["MDD", "no MDD", "not sure"]
    
    for i, img_num in enumerate(image_numbers):
        rt = random.randint(300, 1500)
        key_press = random.choice(responses)
        response_label = response_labels[responses.index(key_press)]
        
        trials.append({
            "rt": rt,
            "stimulus": f"src/images/main/{img_num}.jpg",
            "key_press": 70 if key_press == "f" else 74 if key_press == "j" else 32,
            "key_name": key_press,
            "response_label": response_label,
            "stimulus_number": img_num,
            "condition": condition,
            "experiment_phase": "main",
            "image_shown_count": 1,
            "repeat": False,
            "trial_type": "single-stim-rev-cor-trial",
            "trial_index": 4 + i,  # Starts after initial trials
            "time_elapsed": trials[-1]["time_elapsed"] + rt,
            "experiment_name": experiment_name,
            "sona_id": worker_id,
            "platform": "sona",
            "start_time": start_time,
            "end_time": end_time,
            "total_time": total_time,
            "version_date": version_date,
            "debug_mode": False,
            "refresh_count": random.randint(0, 10),
            "completion_code": completion_code,
            "seed": seed,
            "redirect_url": redirect_url,
            "worker_info": {"sona_id": worker_id, "platform": "sona"},
            "anon_id": anon_id,
            "browser_events": []
        })
    
    # 6. DMISS Survey
    dmiss_time = trials[-1]["time_elapsed"] + random.randint(10000, 20000)
    responses = {}
    for i in range(28):
        responses[str(i)] = random.randint(1, 5)
    
    trials.append({
        "rt": dmiss_time - trials[-1]["time_elapsed"],
        "responses": json.dumps(responses),
        "experiment_phase": "dmiss_survey",
        "trial_type": "survey-likert",
        "trial_index": len(trials),
        "time_elapsed": dmiss_time,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": []
    })
    
    # 7. Demographic Survey
    survey_time = dmiss_time + random.randint(15000, 25000)
    survey_data = {
        "participatedBefore": random.choice(["Yes", "No"]),
        "issues": random.choice(["anxiety", "depression", "none", "other"]),
        "seriousness": str(random.randint(1, 100)),
        "comments": generate_random_string(10) if random.random() < 0.3 else "",
        "age": str(random.randint(18, 80)),
        "race": random.choice([["White"], ["Black/African American"], ["Asian"], ["Hispanic/Latino"], ["Other"]]),
        "sex": random.choice(["Male", "Female", "Other"]),
        "gender": random.choice(["Male", "Female", "Non-binary", "Other"])
    }
    
    trials.append({
        "rt": survey_time - dmiss_time,
        "url": "src/html/survey.html",
        "form_name": "surveyForm",
        "form_id": "#surveyForm",
        "experiment_phase": "survey",
        "form_data": json.dumps(survey_data),
        "trial_type": "render-mustache-template",
        "trial_index": len(trials),
        "time_elapsed": survey_time,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": []
    })
    
    # 8. Debriefing
    debrief_time = survey_time + random.randint(8000, 12000)
    trials.append({
        "rt": debrief_time - survey_time,
        "url": "src/html/debriefing.html",
        "completion_code": completion_code,
        "experiment_phase": "debriefing",
        "trial_type": "render-mustache-template",
        "trial_index": len(trials),
        "time_elapsed": debrief_time,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": []
    })
    
    # 9. Final fullscreen
    trials.append({
        "success": True,
        "trial_type": "fullscreen",
        "trial_index": len(trials),
        "time_elapsed": total_time - 8,
        "experiment_name": experiment_name,
        "sona_id": worker_id,
        "platform": "sona",
        "start_time": start_time,
        "condition": condition,
        "end_time": end_time,
        "total_time": total_time,
        "version_date": version_date,
        "debug_mode": False,
        "refresh_count": random.randint(0, 10),
        "completion_code": completion_code,
        "seed": seed,
        "redirect_url": redirect_url,
        "worker_info": {"sona_id": worker_id, "platform": "sona"},
        "anon_id": anon_id,
        "browser_events": [{"event": "fullscreenexit", "time": total_time - 1000}]
    })
    
    return trials

def test_single_participant():
    """Tests with one participant using exact required format"""
    try:
        # 1. Initialize participant
        participant = generate_participant_info()
        logger.info(f"Participant: {participant}")
        
        # 2. Call /init
        logger.info("Calling /init")
        init_response = requests.post(
            f"{base_url}/init",
            json=participant,
            timeout=5
        )
        init_response.raise_for_status()
        init_data = init_response.json()
        logger.info(f"/init response: {init_data}")
        
        # 3. Generate complete trial data
        trial_data = generate_realistic_trial_data(
            worker_id=participant['worker_id'],
            condition=init_data.get('condition', 'mdd')
        )
        
        # 4. Prepare final payload
        final_data = {
            "json_data": trial_data,
            "worker_id": participant['worker_id'],
            "assignment_id": participant['assignment_id'],
            "hit_id": participant['hit_id'],
            "platform": participant['platform'],
            "condition": init_data.get('condition', 'mdd')
        }
        logger.info(f"Final payload sample: {json.dumps(trial_data[0], indent=2)}")
        
        # 5. Call /data
        logger.info("Calling /data endpoint")
        data_response = requests.post(
            f"{base_url}/data",
            json=final_data,
            timeout=10
        )
        
        if data_response.status_code == 422:
            errors = data_response.json()
            logger.error(f"Validation errors: {errors}")
            return False
            
        data_response.raise_for_status()
        logger.info(f"Data saved successfully: {data_response.json()}")
        return True
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return False


def test_multiple_participants(num_participants=300):
    """Generate data for multiple participants and send to /data endpoint"""
    success_count = 0
    failure_count = 0
    
    for i in range(num_participants):
        logger.info(f"==== Starting test for Participant {i+1} ====")
        
        # Initialize participant
        participant = generate_participant_info()
        logger.info(f"Participant {i+1}: {participant}")
        
        try:
            # Call /init
            logger.info("Calling /init")
            init_response = requests.post(
                f"{base_url}/init",
                json=participant,
                timeout=5
            )
            init_response.raise_for_status()
            init_data = init_response.json()
            logger.info(f"/init response: {init_data}")
            
            # Generate complete trial data
            trial_data = generate_realistic_trial_data(
                worker_id=participant['worker_id'],
                condition=init_data.get('condition', 'mdd')
            )
            
            # Prepare final payload
            final_data = {
                "json_data": trial_data,
                "worker_id": participant['worker_id'],
                "assignment_id": participant['assignment_id'],
                "hit_id": participant['hit_id'],
                "platform": participant['platform'],
                "condition": init_data.get('condition', 'mdd')
            }
            logger.info(f"Final payload sample: {json.dumps(trial_data[0], indent=2)}")
            
            # Call /data endpoint
            logger.info("Calling /data endpoint")
            data_response = requests.post(
                f"{base_url}/data",
                json=final_data,
                timeout=10
            )
            
            if data_response.status_code == 422:
                errors = data_response.json()
                logger.error(f"Validation errors: {errors}")
                failure_count += 1
                continue
            
            data_response.raise_for_status()
            logger.info(f"Data saved successfully for Participant {i+1}: {data_response.json()}")
            success_count += 1
        except Exception as e:
            logger.error(f"Error for Participant {i+1}: {str(e)}", exc_info=True)
            failure_count += 1
        
        logger.info(f"==== End of test for Participant {i+1} ====")
    
    logger.info(f"Test completed. Success: {success_count}, Failure: {failure_count}")
    print(f"Test completed. Success: {success_count}, Failure: {failure_count}")


if __name__ == "__main__":
    logger.info("==== Starting test ====")
    success = test_multiple_participants(num_participants=300)
    if success:
        logger.info("Test completed successfully!")
    else:
        logger.error("Test failed - check logs")
    logger.info("==== End of test ====")
    print("Check test_app_debug.log for details")