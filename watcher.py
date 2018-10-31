#!/usr/bin/python3

import os
import sys
import time

import task

import pprint

# connect to github project
api = task.github.GitHub(repo='att/ast')

for pull in api.pulls(state='open'):
    pp = pprint.PrettyPrinter(indent=4)

    # Clone this url
    pp.pprint(pull["head"]["repo"]["git_url"])
    git_url = pull["head"]["repo"]["git_url"]
    # And checkout this sha
    pp.pprint(pull["head"]["sha"])

    sha = pull["head"]["sha"]

    statuses = api.statuses(sha)
    if statuses and statuses['FreeBSD'] and statuses['FreeBSD']['state'] != 'pending':
        print(statuses['FreeBSD']['state'])
        print("This commit has been already tested.")
        continue

    # Url to update status on github
    pp.pprint(pull["statuses_url"])

    statuses_url=pull["statuses_url"]

    # pp.pprint(pull)

    os.system("git_url=%s sha=%s statuses_url=%s ./run_freebsd_build.sh" % (git_url, sha, statuses_url))
