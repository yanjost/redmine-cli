Redmine Cli
======================================

This is a small command-line utility to interact with Redmine

Installation
-----------------

I suggest you create a `virtualenv <http://www.virtualenv.org>`_

Then just use pip or easy_install.

.. code::

    pip install redmine-cli

or

.. code::

    easy_install redmine-cli


Usage
-----

You have to configure the application by getting a REST API key for your Redmine user

Then edit the configuration file in your home directory ( ~/.redmine-cli )

.. code:: ini

    [default]
    key=YOUR_REDMINE_REST_API_KEY
    my_id=YOUR_REDMINE_USER_ID
    root_url=YOUR_REDMINE_ROOT_URL_WITH_PROTOCOL
    #change to false if you don't want to verify SSL certificates. default is true
    verify_ssl=true


Example values

.. code:: ini

    [default]
    key=c7461a8ed1e4c27b76ce3bec0c0f06f4
    my_id=44
    root_url=https://redmine.mycompany.com


Command-line syntax
--------------------

.. code:: console

    usage: redmine [-h] [--key APIKEY] [--debug] [--root-url ROOT_URL]
                   [--user-id USER_ID] [--version]
                   {query,issues,open,issue} ...

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
      --root-url ROOT_URL   root url of Redmine instance
      --user-id USER_ID     your Redmine user id
      --version             show program's version number and exit


Sample output
--------------

.. code::

    +------+----------+-------------+---------------------------+
    |  ID  | PRIORITY |    STATUS   |    TITLE                  |
    +------+----------+-------------+---------------------------+
    | 6534 |   High   | In Progress | Issue 1                   |
    | 4081 |  Normal  |   Feedback  | Issue 2                   |
    +------+----------+-------------+---------------------------+


Bugs, feature requests, etc...
-------------------------------

Please use Github's issue tracker : https://github.com/yanjost/redmine-cli/issues