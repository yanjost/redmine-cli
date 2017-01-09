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

def get_api_key():
    key = get_config_instance("default").get("key", api_key)
    if key is None:
        raise Exception(
            "Missing API key : please provide one in config file or" +
            "with the command line"
        )
    return key

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

def put_json(url, payload):
    global debug_mode
    key = get_api_key()
    ssl = (get_config_instance("default").get("verify_ssl", verify_ssl) == "True")

    url = build_url(url)
    data = None
    try :
        response = requests.put(
            url,
            verify=ssl,
            data=json.dumps(payload),
            auth=(key,""),
            headers = {'content-type': 'application/json'}
        )

    except :
        print("url called : %s %s" % (url, api_key))
        raise
    if debug_mode: open(get_log_file_path(),'w').write(json.dumps(data,indent=True))
    return response


def get_json(url, params=None):
    global debug_mode
    key = get_api_key()
    ssl = (get_config_instance("default").get("verify_ssl", verify_ssl) == "True")

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

def cmd_status(args):
    issue_id = args.issue_id
    new_status = args.new_status.lower()
    data = get_json("/issue_statuses.json")

    #Note: it does not work in the silly case were you have 2+ statuses
    # with same .lower() representation
    possible_statuses = dict((status['name'].lower(), status['id']) for status in data['issue_statuses'])

    if new_status not in possible_statuses:
        raise Exception("No such status : {status}".format(status= new_status))

    new_status_id = possible_statuses[new_status]
    payload = {"issue" : {"status_id": str(new_status_id) }}
    response = put_json(
        "/issues/{issue}.json".format(issue=issue_id),
        payload
    )

    http_status = response.status_code
    if http_status == 200:
        print("updated")
    elif http_status == 404:
        print("no such issue")
    else:
        print("an error has occured: %d" % http_status)

def cmd_issue(args):
    data = get_json("/issues/{issue}.json".format(issue=args.issue_id))
    is_verbose = args.verbose

    if is_verbose:
        print("Title: %s" % data["issue"]["subject"])
        print("Status: %s" % data["issue"]["status"]["name"])
        print("Author: %s" % data["issue"]["author"]["name"])
        print("description:")
        #TODO: description can be html/markdown etc.
        print(data["issue"]["description"])
    else:
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


    parser_open = subparsers.add_parser('status', help="update an issue's status")
    parser_open.add_argument("issue_id", type=int)
    parser_open.add_argument("new_status", type=str)
    parser_open.set_defaults(func=cmd_status)

    parser_issue = subparsers.add_parser('issue', help="show details on an issue")
    parser_issue.add_argument("issue_id")
    parser_issue.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False
    )

    parser_issue.set_defaults(func=cmd_issue)

    args = parser.parse_args()

    debug_mode = args.debug
    api_key = args.key
    root_url = args.root_url
    user_id = args.user_id

    args.func(args)
