import os
from utils.loader import load_config

def combine_jsonl_files(input_directory):
    """Combines all JSONL files in a directory into a single JSONL file."""
    try:
        combined_jsonl_directory = os.path.join(input_directory, 'combined_jsonl')
        
        # Create the combined_jsonl directory if it doesn't exist
        if not os.path.exists(combined_jsonl_directory):
            os.makedirs(combined_jsonl_directory)
        
        output_file_path = os.path.join(combined_jsonl_directory, 'combined_data.jsonl')
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for file_name in os.listdir(input_directory):
                if file_name.endswith('.jsonl'):
                    jsonl_file_path = os.path.join(input_directory, file_name)
                    with open(jsonl_file_path, 'r', encoding='utf-8') as input_file:
                        for line in input_file:
                            output_file.write(line)
        print(f"Successfully combined JSONL files into {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Load configuration
    config = load_config()
    input_dir = config['jsonl_directory']
    output_dir = config['combined_jsonl_directory']
    combine_jsonl_files(input_dir)