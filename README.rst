Redmine Cli
======================================

This is a small command-line utility to interact with Redmine

Usage
-----

You have to configure the application by getting a REST API key for your Redmine user

Then edit the configuration file in your home directory


    [default]
    key=YOUR_REDMINE_REST_API_KEY
    my_id=YOUR_REDMINE_USER_ID
    root_url=YOUR_REDMINE_ROOT_URL_WITH_PROTOCOL


Example values


    [default]
    key=c7461a8ed1e4c27b76ce3bec0c0f06f4
    my_id=44
    root_url=https://redmine.mycompany.com


Command-line syntax
--------------------

    usage: redmine [-h] [--key APIKEY] [--debug] {query,issues,open,issue} ...

    positional arguments:
      {query,issues,open,issue}
        query               run a saved query by id
        issues              show my issues
        open                open an issue in default browser
        issue               show details on an issue

    optional arguments:
      -h, --help            show this help message and exit
      --key APIKEY          set API key
      --debug               write received data in debug.json