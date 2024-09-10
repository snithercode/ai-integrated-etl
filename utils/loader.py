import os
import yaml
from openai import OpenAI

def load_config(file_path='config/config.yaml'):
    """Load configuration from a YAML file and set up directory paths."""
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    pdf_dir = config['pdf_directory']
    yaml_dir = os.path.join(pdf_dir, 'yaml_files')
    cleaned_yaml_dir = os.path.join(yaml_dir, 'cleaned_yaml_files')
    json_dir = os.path.join(cleaned_yaml_dir, 'json_files')
    jsonl_dir = os.path.join(json_dir, 'jsonl_files')
    combined_jsonl_dir = os.path.join(jsonl_dir, 'combined_jsonl')
    

    

    config['yaml_directory'] = yaml_dir
    config['cleaned_yaml_directory'] = cleaned_yaml_dir
    config['json_directory'] = json_dir
    config['jsonl_directory'] = jsonl_dir
    config['combined_jsonl_directory'] = combined_jsonl_dir
    prompt_set_list = config['selected_prompt_set_list']

    return config

def load_secrets(file_path='config/secrets.yaml'):
    """Load secrets from a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
# Initialize OpenAI client
def init_openai_client():
    secrets = load_secrets('config/secrets.yaml')
    client = OpenAI(api_key = secrets['api_key'])
    return client

