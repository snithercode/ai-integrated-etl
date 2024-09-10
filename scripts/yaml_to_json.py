import os
import yaml
import json
import glob
from utils.loader import load_config

def clean_yaml_file(yaml_file_path, cleaned_dir):
    """
    Cleans the YAML file by fixing indentation issues and saves it in the cleaned directory.

    :param yaml_file_path: Path to the input YAML file.
    :param cleaned_dir: Directory to save the cleaned YAML file.
    :return: Path to the cleaned YAML file.
    """
    base_name = os.path.splitext(os.path.basename(yaml_file_path))[0]
    cleaned_file_path = os.path.join(cleaned_dir, f"{base_name}_cleaned.yaml")
    
    with open(yaml_file_path, 'r') as yaml_file, open(cleaned_file_path, 'w') as cleaned_file:
        inside_thread_object = False
        for line in yaml_file:
            stripped_line = line.strip()
            
            if stripped_line == '---':
                # Ensure delimiters are not indented
                cleaned_file.write(line)
                continue
            
            if stripped_line.startswith('threadObject:'):
                inside_thread_object = True
                cleaned_file.write(line)
                continue
            
            if inside_thread_object:
                if stripped_line.startswith('- '):
                    cleaned_file.write(line)
                    continue
                
                if stripped_line.startswith(('systemRoleContent', 'userRoleContent', 'assistantRoleContent')):
                    if not line.startswith(' '):
                        cleaned_file.write('    ' + line)  # Indent with 4 spaces
                    else:
                        cleaned_file.write(line)
                else:
                    if not line.startswith('    '):
                        cleaned_file.write('        ' + line)  # Indent with 8 spaces
                    else:
                        cleaned_file.write(line)
            else:
                cleaned_file.write(line)
    
    return cleaned_file_path

def yaml_to_json(yaml_file_path, json_file_path, cleaned_dir):
    """
    Converts a YAML file to a JSON file.

    :param yaml_file_path: Path to the input YAML file.
    :param json_file_path: Path to the output JSON file.
    :param cleaned_dir: Directory to save the cleaned YAML file.
    """
    # Clean the YAML file
    cleaned_yaml_file_path = clean_yaml_file(yaml_file_path, cleaned_dir)

    # Read the cleaned YAML file
    with open(cleaned_yaml_file_path, 'r') as yaml_file:
        data = list(yaml.safe_load_all(yaml_file))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    # Write the data to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def replace_keys(data):
    """
    Recursively replaces specific keys in the data structure.

    :param data: The data structure (dict or list) to process.
    :return: The processed data structure with keys replaced.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "threadObject":
                new_key = "messages"
                new_data[new_key] = replace_keys(value)
            elif key == "systemRoleContent":
                new_data = {"role": "system", "content": value}
            elif key == "userRoleContent":
                new_data = {"role": "user", "content": value}
            elif key == "assistantRoleContent":
                new_data = {"role": "assistant", "content": value}
            else:
                new_data[key] = replace_keys(value)
        return new_data
    elif isinstance(data, list):
        return [replace_keys(item) for item in data]
    else:
        return data

if __name__ == "__main__":

    # Load configuration and get directory
    config = load_config()
    input_dir = config['yaml_directory']
    output_dir = config['json_directory']
    cleaned_dir = config['cleaned_yaml_directory']
    
    # Ensure the cleaned directory exists
    os.makedirs(cleaned_dir, exist_ok=True)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each YAML file in the directory
    for yaml_file_path in glob.glob(os.path.join(input_dir, '*.yaml')):
        base_name = os.path.splitext(os.path.basename(yaml_file_path))[0]
        json_file_path = os.path.join(output_dir, f"{base_name}.json")
        
        # Load and process the YAML data
        yaml_to_json(yaml_file_path, json_file_path, cleaned_dir)