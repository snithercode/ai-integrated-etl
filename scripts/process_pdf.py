import os
import PyPDF2
import datetime
import re
from typing import List, Dict
from openai import OpenAI
import importlib
from utils.loader import load_config, init_openai_client

# Initialize OpenAI client
def initialize_openai_client(api_key):
    return OpenAI(api_key=api_key)

# Read PDF file and return text content of each page as a list
def read_pdf(file_path):
    pdf_content = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            try:
                page = reader.pages[page_num]
                pdf_content.append(page.extract_text())
            except PyPDF2.errors.PdfReadError as e:
                print(f"Error reading page {page_num + 1} of {file_path}: {e}")
                pdf_content.append("")  # Append an empty string for the problematic page
    return pdf_content

# Send pdf content to OpenAI and return the response
def send_to_openai(client, pdf_content, prompt_set):
    try:
        # Construct the prompt
        prompt = f"""
        You are generating structured YAML objects for the purpose of fine-tuning an AI model. The YAML object you generate represents a series of messages in a conversation. Your output must always be in valid YAML format.

        Here is an example model for the YAML output.
        **REFRAIN FROM HALLUCINATING OR DEVIATING FROM THE FORMAT OR SYNTAX WITHIN THE EXAMPLE MODEL: **

        <exampleModel>
        threadObject:
            - systemRoleContent: {prompt_set['system_role_content']}
            - userRoleContent: {prompt_set['user_role_content']}
            - assistantRoleContent: "response_to_question"
        </exampleModel>

        For userRoleContent, you will generate a specific request or question directly relevant to the following content that requires a response including generated code:
        
        {pdf_content}
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": prompt_set['system_role_content']},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7,
            top_p=1
        )

        response_text = response.choices[0].message.content if response.choices else None

        # Clean the response text
        if response_text:
            response_text = re.sub(r'^```yaml', '', response_text, count=1).strip()
            response_text = re.sub(r'```$', '', response_text, count=1).strip()

        return response_text
    
    except Exception as e:
        print("An error occurred:", e)
        return None

# Generate a unique filename for the output YAML file
def generate_unique_filename(base_filename, prompt_set_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_filename}_{prompt_set_name}_{timestamp}_fine_tuning.yaml"

# Process a single PDF file with a given prompt set
def process_pdf(client, file_path, output_dir, prompt_set_list):
    for prompt_set in prompt_set_list:
        if isinstance(prompt_set, dict):
            prompt_set_name = prompt_set['name']
            pdf_content = read_pdf(file_path)
            all_responses = []
            print(f"Processing {os.path.basename(file_path)} with prompt set: {prompt_set['name']}")

            for page_num, pdf_page_content in enumerate(pdf_content):
                print(f"Processing page {page_num + 1}/{len(pdf_content)}")
                thread_object_content = send_to_openai(client, pdf_page_content, prompt_set)
                if thread_object_content:
                    all_responses.append(thread_object_content)

            base_filename = os.path.basename(file_path).replace('.pdf', '')
            unique_filename = generate_unique_filename(base_filename, prompt_set_name)
            output_file_path = os.path.join(output_dir, unique_filename)

            with open(output_file_path, 'a', encoding='utf-8') as output_file:
                for i, response in enumerate(all_responses):
                    output_file.write(response)
                    if i < len(all_responses) - 1:
                        output_file.write('\n---\n')  # Newline and delimiter separator
            
            print(f"Finished processing {os.path.basename(file_path)} with prompt: {prompt_set_name}. \nOutput saved to {output_file_path}")
        else:
            raise TypeError("Expected prompt_set to be a dictionary")
        

def process_directory(client, directory_path: str, prompt_sets: List[Dict[str, str]]):
    """Processes all PDF files within a directory using multiple prompt sets and saves the fine-tuning data in a new folder."""
    output_dir = os.path.join(directory_path, 'yaml_files')
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(directory_path, file_name)
            process_pdf(client, file_path, output_dir, prompt_sets)

# Main function to process all PDFs in a directory with a specified prompt set list
def main():
    # Load configuration from config.yaml
    config = load_config()
    
    # Import the prompt_sets module
    prompt_sets_module = importlib.import_module('config.prompt_sets')

    # Access the prompt_set_list specified in the configuration
    selected_prompt_set_list = getattr(prompt_sets_module, config['selected_prompt_set_list'])

    pdf_directory = config['pdf_directory']
    output_dir = config['yaml_directory']

    
    client = init_openai_client()

    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    process_directory(client, pdf_directory, selected_prompt_set_list)

if __name__ == "__main__":
    main()