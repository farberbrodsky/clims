import argparse
import getpass
import json
from sys import exit
from pathlib import Path
from appdirs import AppDirs
import api

from scans import scans_list_cli

# Read authentication data
auth_file = Path(AppDirs("clims").user_config_dir) / "auth"
auth_data = None
if not auth_file.is_file():
    print("No auth data found.")
    new_username = input("username: ")
    new_id = input("      id: ")
    new_pass = getpass.getpass("password: ")
    auth_data = {"username": new_username, "id": new_id, "password": new_pass}
    auth_file.parent.mkdir(parents=True)
    with open(auth_file, "w") as f:
        json.dump(auth_data, f)
    print("Saved to", auth_file)
else:
    with open(auth_file, "r") as f:
        auth_data = json.load(f)


def fetch_cli(args, auth_data):
    print(api.login_and_fetch_or_exit(args.url, auth_data))

# Parse arguments


my_parser = argparse.ArgumentParser(
    description="An unofficial CLI for ims.tau.ac.il",
    prog="clims")
subparsers = my_parser.add_subparsers(help="sub-command help")

parser_fetch = subparsers.add_parser(
    "fetch", help="Fetch any URL in the IMS with a logged in session.")
parser_fetch.add_argument("url", help="The URL to fetch.")
parser_fetch.set_defaults(function=fetch_cli)

parser_scans_list = subparsers.add_parser(
    "scans-list", help="List your scans.")
parser_scans_list.set_defaults(function=scans_list_cli)

args = my_parser.parse_args()
if "function" in args:
    args.function(args, auth_data)
