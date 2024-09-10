import json
import os
from utils.loader import load_config

def json_to_jsonl(input_file_path, output_file_path):
    """Converts a JSON file to JSONL format."""
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            data = json.load(input_file)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for item in data:
                json.dump(item, output_file)
                output_file.write('\n')

    except Exception as e:
        print(f"An error occurred: {e}")

def convert_directory_to_jsonl(input_dir, output_dir):
    """Converts all JSON files in a directory to JSONL format."""
    jsonl_dir = output_dir  # Use the provided directory path directly
    if not os.path.exists(jsonl_dir):
        os.makedirs(jsonl_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(input_dir, file_name)
            jsonl_file_path = os.path.join(jsonl_dir, file_name.replace('.json', '.jsonl'))
            json_to_jsonl(json_file_path, jsonl_file_path)


def main():
    # Load configuration and get directory
    config = load_config()
    input_dir = config['json_directory']
    output_dir = config['jsonl_directory']
    convert_directory_to_jsonl(input_dir, output_dir)

if __name__ == "__main__":
    main()