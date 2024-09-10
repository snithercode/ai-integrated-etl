## 🛠 What's Changed?

1. **Added `secrets.yaml`**  
   I've taken extra steps to avoid any more unintended oversharing of our API key by introducing a `secrets.yaml` file to store private data that these scripts need access to. 
   

2. **Added `config.yaml`** 

    These are the only two things you'll be manually updating when you run your scripts:

   - `pdf_directory`: No more manually defining paths in every script. You'll now declare just one path here instead; the path to your PDFs. The scripts handle the rest by dynamically creating the necessary nested directories for processed data and grabbing the paths they need, when they need them.
   - `selected_prompt_set_list`: This is where you'll declare which prompt set list you want to run. 

3. **Added `loader.py`**
   - `load_config` to load configuration settings from a YAML file and set up directory paths dynamically.
   - `load_secrets` to securely load API secrets from a YAML file.
   - `init_openai_client` to initialize the OpenAI client using the loaded API key.

4. **Logging added to `upload_and_fine_tune`**
- Added logging functionality to record fine-tuning job details in `fine_tune_log.json`.
  - Introduced `log_fine_tune_jobs` function to handle logging. 
  - Logs are saved as `fine_tune_log.json` in the `combined_jsonl` folder.
  - Updated the main script to log the file ID, fine-tune job ID, status, and model ID (if available) after each fine-tuning job.

  - **Example:**
    ```json
    [
        {
            "timestamp": "2024-09-05 22:16:53.605465",
            "file_id": "file-jPyhb2uwyZkzbDXyF7KFuDXv",
            "fine_tune_id": "ftjob-eKY5jy7PjvFathqOxjsbNVVm",
            "status": "failed"
        },
        {
            "timestamp": "2024-09-05 22:17:42.833788",
            "file_id": "file-Tpbw3Odw7d9HrLzD1iPQw2ui",
            "fine_tune_id": "ftjob-ezPf1ajMxeGd4zXmGCJB2NyN",
            "status": "failed"
        },
        {
            "timestamp": "2024-09-06 01:32:34.651567",
            "file_id": "file-WyZBEnsOcSFmhfchqgHRbc7X",
            "fine_tune_id": "ftjob-NWk5KDdHgqhTtf1NVrzZNT18",
            "status": "succeeded",
            "fine_tune_model_id": "ft:gpt-4o-mini-2024-07-18:personal::A2SzP8eL"
        }
    ]
    ```
5. **Changes to `process_pdf.py`**
    - Batch processes PDFs using prompt sets from prompt_sets.py You will no longer need to manually process each PDF file with each prompt set; this script will automate the process for you.
    - No longer outputs `.json` files. To reduce the number of formatting issues, I've gone with asking the LLM to generate `.yaml` instead, which is syntactically less complex.
    - Outputs one `.yaml` file for each combination of (PDF file + unique prompt set category)

6. **Added `yaml_to_json.py`**
    - Even though `.yaml` is easier for the LLM to generate, we still want `.json` format so we can convert it to `.jsonl` for our `upload_and_fine_tune.py` script.


## REQUIRED SETUP: Virtual Environment

### 1. Creating a Virtual Environment

Using a virtual environment (`venv`) is a best practice because it isolates the project's dependencies, ensuring that they don't conflict with other projects or system-wide packages. This setup helps maintain consistency across different environments and makes projects easier to manage and deploy.

Here is how to create a virtual environment. We'll name it `.venv` for consistency.

1. **Open a terminal in your IDE** (or use your system terminal).

2. Run the following command to create the virtual environment in a directory called `.venv`:


**For macOS or Linux** (using Terminal: zsh or bash):
```bash
python3 -m venv .venv
```
**For Windows** (using PowerShell or Command Prompt):
```powershell
python -m venv .venv
```

### 2. Activating the Virtual Environment

Once the virtual environment is created, you need to activate it:

### For macOS and Linux (using Terminal):
```bash
source .venv/bin/activate
```

### For Windows:

```powershell
.venv\Scripts\Activate
```

### Deactivating the Virtual Environment

You don't need to do this right now, but when you do want to deactivate the virtual environment, simply run:
```bash
deactivate
```

## Setting the Interpreter in VS Code

After creating and activating your virtual environment, you need to ensure that VS Code is using the correct Python interpreter.

1. **Open the Command Palette**:
   - Press `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (macOS) to open the Command Palette.

2. **Select Interpreter**:
   - Type `Python: Select Interpreter` and select it from the dropdown.

3. **Choose the Virtual Environment**:
   - From the list of available interpreters, select the one that points to your virtual environment. It should look something like `.venv/bin/python` or `.venv\Scripts\python.exe`.

This ensures that all the packages installed in your virtual environment are used by VS Code.

## REQUIRED SETUP: Installing Dependencies

To install all the packages required to make these scripts work, follow these steps:

### 1. Make sure your virtual environment is activated.
If you forget to activate your virtual environment, the packages will be installed globally, which can lead to conflicts with other projects and dependencies on your system.
### **For macOS and Linux** (using Terminal):
    
```bash
source venv/bin/activate
```
### **For Windows** (using PowerShell or Command Prompt):
```powershell
venv\Scripts\activate
```

### 2. Install the dependencies using `pip` and the `requirements.txt` file:
This will install everything you need, all in one go.
```bash
pip install -r requirements.txt
```

## REQUIRED SETUP: Configuring System Path

Having the project directory added to your system's path helps avoid import issues. To configure the project and ensure it is added to your virtual environment's `PYTHONPATH`, follow these steps:

### 1. Run Setup.py

Run the `setup.py` script to configure the environment:

```bash
python setup.py
```


### 2. Restart Your Virtual Environment

After running the setup script, you need to restart your virtual environment to apply the changes. 
If you don't already have a terminal open in your IDE, open one now.

### For macOS and Linux:
```bash
# Deactivate the virtual environment
deactivate

# Reactivate the virtual environment
source venv/bin/activate
```

### For Windows:
```cmd
# Deactivate the virtual environment
deactivate

# Reactivate the virtual environment
venv\Scripts\activate
```

### 3. Verify the Setup

Once your virtual environment is reactivated, you can verify that your project directory has been successfully added to the PYTHONPATH by running:

```bash
python -c "import sys; print(sys.path)"
```


## Final Steps: How To Use
Just a few more things and then you'll be ready to run the scripts.
### 1. Datasheet Organization
Put your PDF documents inside of the `datasheets` folder. I recommend grouping PDFs about the same overarching topic in their own folder inside of the `datasheets` folder. Here is a visual to show what I mean:

```
├── datasheets/             # Folder where you put your PDF documents
│   ├── RISCV/              # Folder for RISCV-related PDFs
│   │   ├── riscv_datasheet1.pdf
│   │   └── riscv_datasheet2.pdf
│   ├── Arduino_Nano/       # Folder for Arduino Nano-related PDFs
│   │   ├── arduino_nano_datasheet1.pdf
│   │   └── arduino_nano_datasheet2.pdf
```

### 2. Create Your Prompt Set List(s)

Your prompt set lists are located in `prompt_sets.py`.
When you open it up, it's going to look something like this:

```python
prompt_set_list_1 = [
    {
        "name": "unique_prompt_set_category_1",
        "user_role_content": "hypothetical user question or request",
        "system_role_content": "how you want the system to respond to the user"
    },
    {
        "name": "unique_prompt_set_category_2",
        "user_role_content": "hypothetical user question or request",
        "system_role_content": "how you want the system to respond to the user"
    }
]
```

### Explaining the List of Dictionaries: `prompt_set_list`

The `prompt_set_list` is a list that contains multiple dictionaries, with each dictionary representing a unique prompt set. Each prompt set defines parameters for configuring system and user roles in generating responses. Below is a description of the keys in each dictionary:

- **`name`**: A short identifier or label for the prompt set.  
  
  **Example**: 
  
  ```
  "riscv_fp_operations"  
  ```
  **Purpose**: This serves as a unique identifier for the specific prompt set, helping distinguish between different tasks or operations (e.g., operations involving RISC-V floating-point instructions).

- **`user_role_content`**: The request or prompt provided by the user, specifying the task they want to accomplish.  
  
  **Example**: 
  ```
  "Generate RISC-V assembly code that performs floating-point addition and multiplication using the MiniFloat-NN ISA extension"
  ``` 
  **Purpose**: Defines the user's specific request, describing what needs to be generated or achieved by the system.

- **`system_role_content`**: The most critical component of the prompt set, this key defines the persona, knowledge base, and behavior of the system (or assistant) responding to the user.
  
  **Example**:  
  ```text
  "You are a well-studied Embedded Systems Engineer with extensive experience in floating-point computation and ISA (Instruction Set Architecture) design. Your deep knowledge spans across floating-point arithmetic standards and optimizations, and includes a detailed understanding of floating-point operations using specialized RISC-V ISA extensions. Apply your expertise to provide comprehensive, accurate, and nuanced responses that cover both general principles and specific technical details, incorporating advanced strategies and real-world examples where applicable."
  
### 3. Update `config.yaml`
`config.yaml` is where you'll specify:
- The path for your PDF files
- Your selected prompt set list *(use the name of the list, <u>NOT</u> the value of the dictionary's name key.)*

### 4. Tweak the prompt in `process_pdf.py` (Optional)
In the `send_to_openai()` function, there is a line that I've included that reads:
```
For userRoleContent, you will generate a specific request or question directly relevant to the following content that requires a response including generated code:
```
This line tells the LLM what kind of synthetic data you're looking for - in this example it's code generation, but if you don't care about whether or not code is generated, you can simply remove the last part: "that requires a response including generated code".

### 4. Update `secrets_file.yaml`
Rename `secrets_file.yaml` to `secrets.yaml` and update it to include your API key.

### 6. Finally: Run the Scripts

Here is the sequence:

    1. process_pdf.py
    2. yaml_to_json.py
    3. json_to_jsonl.py
    4. combine_jsonl_files.py
    5. upload_and_fine_tune.py (if you're ready to)
