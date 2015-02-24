#!/usr/bin/env python

from __future__ import print_function

import requests
import prettytable
import memoizer

import argparse
import json
import os

try:
    import ConfigParser
except:
    from configparser import ConfigParser


from . import __version__


config_file_path = "~/.redmine-cli"

api_key = None
root_url = None
debug_mode = False
user_id = None
verify_ssl = True

global config_obj
config_obj = None

def get_config():
    global config_obj
    if not config_obj :
        file_path = os.path.expanduser(config_file_path)
        config_obj = ConfigParser.ConfigParser()
        if os.path.exists(file_path):
            config_obj.read(file_path)
    return config_obj

def get_config_instance(instance_url):
    get_config()
    # assert isinstance(config_obj, ConfigParser.ConfigParser)
    if not config_obj.has_section(instance_url):
        return {}
    return dict(config_obj.items(instance_url))

@memoizer.memoize
def get_log_file_path():
    import os
    return os.path.join(os.getcwd(),"debug.json")

def build_url(path):
    global root_url
    root_url = get_config_instance("default").get("root_url", root_url)
    if root_url is None:
        raise Exception("Missing Root URL")
    return root_url + path

def get_json(url, params=None):
    global debug_mode
    key = get_config_instance("default").get("key", api_key)
    ssl = (get_config_instance("default").get("verify_ssl", verify_ssl) == "True")
    if key is None:
        raise Exception("Missing API key : please provide one in config file or with the command line")

    url = build_url(url)
    data = None
    try :
        data = requests.get(url,verify=ssl,params=params,auth=(key,"")).json()
    except :
        print("url called : {} params={} api_key={}".format(url, params, api_key))
        raise
    if debug_mode: open(get_log_file_path(),'w').write(json.dumps(data,indent=True))
    return data

def print_issues(data):
    n = ["id","priority","status","title"]

    n = [ i.upper() for i in n ]

    table = prettytable.PrettyTable(n)

    for issue in data["issues"]:
        table.add_row([issue["id"],issue["priority"]["name"],issue["status"]["name"], issue["subject"]])

    print(table)

def cmd_issues(args):
    global user_id
    user_id = get_config_instance("default").get("my_id", user_id)
    data = get_json("/issues.json",{"assigned_to_id":user_id, })

    print_issues(data)

def cmd_issue(args):
    data = get_json("/issues/{issue}.json".format(issue=args.issue_id))

    print(data["issue"]["subject"])

def cmd_query(args):
    data = get_json("/projects/{project}/issues.json".format(project=args.project),
                    {"query_id":args.query_id },
                    )

    print_issues(data)

def cmd_open(args):
    import webbrowser
    webbrowser.open(build_url("/issues/{}".format(args.issue_id)))

def main():
    global debug_mode, api_key, root_url, user_id, verify_ssl

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument("--key", metavar="APIKEY", default=None, help="set API key")
    parser.add_argument("--debug", action="store_true", default=False, help="write received data in debug.json")
    parser.add_argument("--root-url", help="root url of Redmine instance")
    parser.add_argument("--user-id", help="your Redmine user id")

    parser.add_argument('--version', action='version', version='{0}.{1}.{2}'.format(*__version__))

    parser_query = subparsers.add_parser('query', help="run a saved query by id")
    parser_query.add_argument("project")
    parser_query.add_argument("query_id", type=int)
    parser_query.set_defaults(func=cmd_query)

    parser_issues = subparsers.add_parser('issues', help="show my issues")
    # parser_issues.add_argument("query_id")
    parser_issues.set_defaults(func=cmd_issues)

    parser_open = subparsers.add_parser('open', help="open an issue in default browser")
    parser_open.add_argument("issue_id", type=int)
    parser_open.set_defaults(func=cmd_open)

    parser_issue = subparsers.add_parser('issue', help="show details on an issue")
    parser_issue.add_argument("issue_id")
    parser_issue.set_defaults(func=cmd_issue)

    args = parser.parse_args()

    debug_mode = args.debug
    api_key = args.key
    root_url = args.root_url
    user_id = args.user_id

    args.func(args)
