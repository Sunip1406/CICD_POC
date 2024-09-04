import subprocess
import json
import sys
import os

template_path = 'schemachange.template.yml'
output_path = 'schemachange.yml'

def read_template(template_path):
    with open('schemachange.template.yml', 'r') as file:
        return file.read()

def load_config(stage):
    with open('config/env_config.json', 'r') as f:
        config = json.load(f)
    return config[stage]

def write_config(config_content, output_path):
    with open(output_path, 'w') as file:
        file.write(config_content)

def replace_placeholders(template_content, config_data):
    for key, value in config_data.items():
        placeholder = f'{{{{{key}}}}}'
        if value is None:
            raise ValueError(f'Value for {key} not set in config file')
        template_content = template_content.replace(placeholder, value)
    return template_content

def config_schemachange(stage):
    # Read the template file
    template_content = read_template(template_path)

    # Read the configuration JSON file
    config_data = load_config(stage)

    # Replace placeholders with values from the configuration file
    config_content = replace_placeholders(template_content, config_data)

    # Write the resulting configuration to the output file
    write_config(config_content, output_path)

def run_schemachange(stage):
    
    config_schemachange(stage)
    
    command = [
        "schemachange","-f", "snowflake_changes",
        "--config","schemachange.yml"
          # Path to the change scripts
             ]
    
    try:
        # Run the command
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"SchemaChange executed successfully for {stage}.")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"SchemaChange failed: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    # The environment is passed as a command-line argument (dev or prod)
    stage = sys.argv[1]
    run_schemachange(stage)
