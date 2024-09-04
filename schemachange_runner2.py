import subprocess
import json
import sys
import os

def load_config(stage):
    with open('config/env_config.json', 'r') as f:
        config = json.load(f)
    return config[stage]

def run_schemachange(stage):
    config = load_config(stage)
    
    command = [
        "schemachange",
        "-f", "snowflake_changes",  # Path to the change scripts
        "-a", config["snowflake_account"],
        "-u", config["snowflake_user"],
        "-d", config["snowflake_database"],
        "-s", config["snowflake_schema"],
        "--change-history-table", f"{config['snowflake_database']}.{config['snowflake_schema']}.change_history"  
             ]
    
    try:
        subprocess.run(command, check=True)
        print(f"SchemaChange executed successfully for {stage}.")
    except subprocess.CalledProcessError as e:
        print(f"SchemaChange failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # The environment is passed as a command-line argument (dev or prod)
    stage = sys.argv[1]
    run_schemachange(stage)