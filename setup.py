import os
import sys
import platform

def is_venv():
    """Detect if a virtual environment is currently active."""
    return sys.prefix != sys.base_prefix

def add_to_activate_script(venv_activate_file, repo_path):
    """Add PYTHONPATH to the virtual environment's activate script."""
    if not os.path.exists(venv_activate_file):
        print(f"Activate script not found: {venv_activate_file}")
        return

    # Read the activate script and check if the path is already added
    with open(venv_activate_file, 'r') as file:
        lines = file.readlines()

    if any(f"PYTHONPATH" in line and repo_path in line for line in lines):
        print("PYTHONPATH already set in the virtual environment's activate script.")
        return

    # Add the PYTHONPATH export to the activate script
    with open(venv_activate_file, 'a') as file:
        if platform.system() == "Windows":
            file.write(f'\nset PYTHONPATH={repo_path};%PYTHONPATH%\n')
        else:
            file.write(f'\nexport PYTHONPATH="$PYTHONPATH:{repo_path}"\n')

    print(f"Added PYTHONPATH to the virtual environment's activate script: {venv_activate_file}")

def add_pythonpath_to_venv(repo_path):
    """Modify the virtual environment's activate script to set PYTHONPATH."""
    if not is_venv():
        print("No virtual environment detected. Exiting.")
        return
    
    # Detect OS and select the correct activate script path
    venv_dir = sys.prefix  # This is the virtual environment directory
    if platform.system() == "Windows":
        activate_file = os.path.join(venv_dir, 'Scripts', 'activate.bat')
    else:
        activate_file = os.path.join(venv_dir, 'bin', 'activate')

    add_to_activate_script(activate_file, repo_path)

if __name__ == '__main__':
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    add_pythonpath_to_venv(repo_path)
