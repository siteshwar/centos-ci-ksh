#
# This script uses the Duffy node management api to get fresh machines to run
# your CI tests on. Once allocated you will be able to ssh into that machine
# as the root user and setup the environ
#
# XXX: You need to add your own api key below, and also set the right cmd= line 
#      needed to run the tests
#
# Please note, this is a basic script, there is no error handling and there are
# no real tests for any exceptions. Patches welcome!

import json, urllib, subprocess, sys, time

url_base="http://admin.ci.centos.org:8080"

# This file was generated on your slave.  See https://wiki.centos.org/QaWiki/CI/GettingStarted
api=open('duffy.key').read().strip()

ver="7"
arch="x86_64"
count=1
git_url="https://example.com/test.git"

get_nodes_url="%s/Node/get?key=%s&ver=%s&arch=%s&count=%s" % (url_base,api,ver,arch,count)

while True:
	dat=urllib.urlopen(get_nodes_url).read()
	try:
		b=json.loads(dat)
	except ValueError:
		print "Failed to load json"
		time.sleep(300)
		continue

	print b
	for h in b['hosts']:
	  cmd="ssh -t -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@%s.ci.centos.org 'yum install -y git centos-release-scl; yum install -y rh-python36; git clone https://github.com/siteshwar/centos-ci-ksh.git; cd centos-ci-ksh; scl enable rh-python36 bash <<< \"GITHUB_USER= GITHUB_API_KEY= python3 watcher.py\"'" % (h)
	  print cmd
	  rtn_code=subprocess.call(cmd, shell=True)
	  
	done_nodes_url="%s/Node/done?key=%s&ssid=%s" % (url_base, api, b['ssid'])
	das=urllib.urlopen(done_nodes_url).read()
	time.sleep(300)

sys.exit(rtn_code)
