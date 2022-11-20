#!python3

import argparse
import subprocess
import platform
from termcolor import colored


def test_status_with_ping(host):
    """
        Returns True if host (str) responds to a ping request.
        Implemented based on subprocess library
        """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def check_websites(filename, color=False):
    """Extracts website from file and run a probe on it.  Results are immediately displayed. """
    # Extract list of sites from file given in parameters
    sites = []
    try:
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                sites.append(line)
    except FileNotFoundError:
        print("Erreur : Fichier introuvable")
        return
    for site in sites:
        if color:
            result = colored("Accessible", "green") if test_status_with_ping(site) else colored("Inaccessible", "red")
        else:
            result = "Accessible" if test_status_with_ping(site) else "Inaccessible"
        print(f"{site} \t\t: \t\t {result}")


if __name__ == '__main__':
    # Use parseargs to get params and options
    parser = argparse.ArgumentParser(description='Easy Websites Monitoring.')
    # File argument
    parser.add_argument('file', metavar='FILE', help="file containing the list of websites to monitor, one per line.", )
    # Activate text coloring
    parser.add_argument("-c","--color", help="display colored test result", action="store_true")
    args = parser.parse_args()
    if args.color:
        check_websites(args.file, color=True)
    else :
        check_websites(args.file)