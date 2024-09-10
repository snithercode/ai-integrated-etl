import os
import time
import json
from datetime import datetime
from openai import OpenAI
from utils.loader import load_config, init_openai_client

client = init_openai_client()

def upload_file(file_path):
    """Uploads a file to OpenAI and returns the file ID."""
    try:
        with open(file_path, "rb") as f:
            response = client.files.create(
                file=f,
                purpose='fine-tune'
            )
        print(response)
        file_id = response.id
        print(f"File {file_path} uploaded successfully with ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file {file_path}: {e}")
        return None

def create_fine_tune(file_id):
    """Creates a fine-tuning job with the uploaded file ID."""
    try:
        response = client.fine_tuning.jobs.create(
            training_file=file_id,
            model="gpt-4o-mini-2024-07-18"  # Specify the base model to fine-tune
        )
        fine_tune_id = response.id
        print(f"Fine-tuning job created with ID: {fine_tune_id}")
        return fine_tune_id
    except Exception as e:
        print(f"Error creating fine-tuning job: {e}")
        return None

def monitor_fine_tune(fine_tune_id):
    """Monitors the fine-tuning job until it is complete and returns the final status."""
    final_status = None
    while True:
        try:
            fine_tune_status = client.fine_tuning.jobs.retrieve(fine_tune_id)
            status = fine_tune_status.status
            print(f"Fine-tune job status: {status}")
            if status in ["succeeded", "failed"]:  # Check for terminal statuses
                final_status = status
                break
            time.sleep(30)  # Wait for 30 seconds before checking again
        except Exception as e:
            print(f"Error monitoring fine-tuning job: {e}")
            final_status = "error"
            break
    return final_status

def log_fine_tune_jobs(directory, log_entries):
    """Logs the fine-tune job entries to fine_tune_log.json in the specified directory."""
    log_file_path = os.path.join(directory, 'fine_tune_log.json')
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            existing_entries = json.load(log_file)
    else:
        existing_entries = []

    existing_entries.extend(log_entries)

    with open(log_file_path, 'w') as log_file:
        json.dump(existing_entries, log_file, indent=4, default=str)

def get_fine_tuned_model_id(fine_tune_id):
    """Retrieves the model ID from a completed fine-tuning job."""
    try:
        fine_tune_details = client.fine_tuning.jobs.retrieve(fine_tune_id)
        model_id = fine_tune_details.fine_tuned_model
        print(f"Fine-tuned model ID: {model_id}")
        return model_id
    except Exception as e:
        print(f"Error retrieving fine-tuned model ID: {e}")
        return None

if __name__ == "__main__":

    config = load_config()
    input_dir = config['combined_jsonl_directory']
    combined_jsonl_file = os.path.join(input_dir, "combined_data.jsonl")

    log_entries = []

    # Upload the combined JSONL file
    file_id = upload_file(combined_jsonl_file)
    if file_id:
        # Create and monitor the fine-tuning job
        fine_tune_id = create_fine_tune(file_id)
        if fine_tune_id:
            final_status = monitor_fine_tune(fine_tune_id)
            log_entry = {
                'timestamp': datetime.now(),
                'file_id': file_id,
                'fine_tune_id': fine_tune_id,
                'status': final_status
            }
            log_entries.append(log_entry)
            log_fine_tune_jobs(input_dir, log_entries)
            
            # Retrieve and log the fine-tuned model ID
            if final_status == "succeeded":
                model_id = get_fine_tuned_model_id(fine_tune_id)
                if model_id:
                    log_entry['model_id'] = model_id
                    log_fine_tune_jobs(input_dir, log_entries)
    # fine_tune_id = "ftjob-xe4decKZxiRRom2sROopGOJk"
    # monitor_fine_tune(fine_tune_id)
