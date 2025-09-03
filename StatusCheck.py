from datetime import datetime
import subprocess
import json
import os

Services_to_check = ["lunprojects", "wg-quick@wg0.service"]

OUTPUT_FILE = "/tmp/service_status.json"

def check_service_status(service_name: str) -> str:
    """
    Checks if a systemd service is active or not using 'systemctl is-active'.
    This is the recommended method for scripting.

    Args:
        service_name: The name of the service to check.

    Returns:
        A string: 'online', 'offline', or 'not found'.
    """
    try:
        # Note: If running this script as a non-privileged user (like www-data),
        # you might need to configure sudo rules to allow this specific command.
        # The command would then be: ['sudo', '/usr/bin/systemctl', 'is-active', ...]
        command = ['systemctl', 'is-active', '--quiet', service_name]
        result = subprocess.run(command, check=False)

        if result.returncode == 0:
            return "online"
        else:
            # Check if the service is not found (exit code 4) vs. just inactive (exit code 3)
            status_check = subprocess.run(
                ['systemctl', 'status', service_name],
                capture_output=True,
                check=False
            )
            if status_check.returncode == 4:
                return "not found"
            return "offline"

    except FileNotFoundError:
        # This occurs if 'systemctl' isn't in the PATH.
        return "unknown_host_error"
    except Exception:
        return "unknown_script_error"

def update_status_json(service_list: list, output_path: str):
    """
    Checks a list of services and writes their statuses to a JSON file.

    Args:
        service_list: A list of service name strings to check.
        output_path: The full path to the output JSON file.
    """
    service_statuses = {}
    
    print(f"Checking status for {len(service_list)} services...")

    # Loop through each service and get its status
    for service in service_list:
        status = check_service_status(service)
        service_statuses[service] = status
        print(f"  - {service}: {status}")

    # Prepare the final data structure with a timestamp
    # Using ISO 8601 format is the standard and best practice for timestamps.
    output_data = {
        "last_updated_utc": datetime.utcnow().isoformat(),
        "services": service_statuses
    }

    # Write the data to the JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"\nSuccessfully wrote status to {output_path}")
    except IOError as e:
        print(f"\nError: Could not write to file at {output_path}. Check permissions.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during file writing: {e}")

# This block makes the script runnable from the command line
if __name__ == "__main__":
    update_status_json(Services_to_check, OUTPUT_FILE)