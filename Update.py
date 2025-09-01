#!python3
from time import sleep
from os import system
import sys


args = sys.argv

print("Sudo is needed, to allow for automated used this is the only time for asking for the password.")
system("sudo echo -e 'Now Given Access!'")

def ShutdownServices():
    print("Shutting down Services...")
    system("sudo systemctl stop lunprojects")
    system("sudo systemctl stop nginx")

def UpdateSystem():
    print("Updating System...")
    sleep(3)
    system("sudo apt update")
    system("sudo apt upgrade -y")

def StartServices():
    print("Starting Services...")
    system("sudo systemctl start lunprojects")
    system("sudo systemctl start nginx")

def UpdateHosts():
    print("Updating Web Hosts...")
    sleep(2)
    system("rm -fr Website")
    system("git clone https://github.com/ChristianHiland/Website.git")

def UpdatingServices():
    print("Updating Services")
    sleep(2)
    system("sudo nginx -t")

if len(args) >= 1:
    if args[1] == "full":
        # Shutdown Services.
        ShutdownServices()
        # Updating System
        UpdateSystem()
        # Update Hosts.
        UpdateHosts()
        # Starting Services back up.
        StartServices()
else:
    # Shutdown Services
    ShutdownServices()
    # Update Hosts.
    UpdateHosts()
    # Start Services
    StartServices()

