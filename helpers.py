import subprocess
import json

def UpdateJSON(path, newData, flag="message"):
    # Get Data
    oldData = None
    with open(path, "r") as file:
        oldData = json.load(file)

    # Update Using Flag
    if flag == "message":
        oldData["messages"].append(newData)
    else:
        print("No Vaild Flag Given!")

    with open(path, "w") as file:
        json.dump(oldData, file, indent=4)


def ReadJSON(path, flag="message"):
    if flag == "message":
        with open(path, "r") as file:
            data = json.load(file)
            return data
    else:
        print("No Vaild Flag Given!")

def GetStatus(target):
    try:
        # Use --quiet to suppress output and just get the exit code.
        # check=False prevents CalledProcessError from being raised on non-zero exit codes.
        result = subprocess.run(
            ['systemctl', 'is-active', '--quiet', target],
            check=False 
        )

        # An exit code of 0 means the service is active (online).
        if result.returncode == 0:
            return "Online"
        else:
            # To be more specific, we can check if the service exists at all.
            # 'systemctl status' returns 4 if the unit is not found.
            existence_check = subprocess.run(
                ['systemctl', 'status', target],
                capture_output=False, # We don't need to see this output
                check=False
            )
            if existence_check.returncode == 4:
                return "not found"
            else:
                return "Offline" # Covers 'inactive', 'failed', etc.

    except FileNotFoundError:
        # This error occurs if the 'systemctl' command itself is not found.
        print("Error: 'systemctl' command not found. This script must be run on a systemd-based OS.")
        return "unknown"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "unknown"