# summary of my python experience

at Collective

developed 20+ scripts to automate tasks, perform data validation, facilitate production support

automation

* utils.py		basic utilities

* ps.py		customize output of ps aux; also loop

* dig-test.py	confirm connectivity to hosts

* versions.py	show versions of various installed components

* organize.py	organize structure of file systems between laptop and home mac

* sync.py	synchronize work mac and home mac; get local backups of source

* ias-sync.py	synchronize automation scripts for ias project between hosts

* myscp.py	copy files between hosts; symbolically linked to get hostname

* get-os.py	print info about hosts's OS

* myip.py	print info about host's IP address

* utc.py		print time and date in UTC time zone

data validation

* ias-validate.py		data validation of new IAS daily log files (60 million lines)

* count-ctrla.py		count number of delimiters in IAS files

* dt-gs-hourly.py	download an hourly DT imps file from google storage and parse it

to get time, creative id, and transaction id

database queries

* query-amp-status.py	  query status table in pg db

data analysis and aggregation

* segment-look.py	ported from ruby to improve performance; count uniques in a segment 			file (up to 30GB)

production support

* check-xfp.py		  check status of hourly and daily download, log processing,

file transfer jobs that run on Hadoop and produce

files for Netezza

* celos-query.py	  monitor status of job or jobs running in celos as part of workflow

* check-dmp.py		  check status of "dmp" application by scanning app log files

* oozie-status.py	  print status of workflow job in oozie

* get-activity-types.py	  count activity types for building up monitoring for reporting subsystem

at Google

* 3 production programs part of Data Transfer port from DoubleClick to Google infrastructure; part of a pipeline to create hourly "DT" files, organize files, keep track of files, and copy from Google stack back to DoubleClick stack for subsequent delivery to customers

for personal use

* developed generic and reusable programs to monitor text and send automated email with subject line allowing to filter normal results and only view mails with warnings or errors

## sample program, anonymized

**`#!/usr/bin/pytho**n`

**`# sample python program developed; internal details have been removed or anonymize**d`

**`# myapp-query.p**y`

**`# query myapp for workflows running ther**e`

**`from utils import ***`

**`# defines a number of things including: def log(str), def run_cmd(cmd, echo=False**)`

**`# parse the output of this command: (real names have been anonymized**)`

**`# curl 'http://hostname.fqdn.company.org:8080/appname/workflow-list' **{`

**`# "ids" : [ "log-processor-dc1", "log-processor-dc2", "appname-download1"**,`

**`# "appname-download2", "appname-download3" ]**}`

**`import jso**n`

**`my_url = 'http://myapp001.fqdn.company.org:8080/myapp/workflow**'`

**`results = ''.join(run_cmd("curl '" + my_url + "-list' 2>/dev/null").split('\n')**)`

**`# convert to a dic**t`

**`wf_list = json.loads(results**)`

**`# examine part of the status of a given workflow (there is usually a lot of output**)`

**`def examine_status(wf)**:`

**`	cmd = "curl '" + my_url + "?id=" + wf + "' 2>/dev/null**"`

**`	log("running " + cmd**)`

**`	results = run_cmd(cmd**)`

**`	mydict = json.loads(results**)`

**`	mykeys = sorted(mydict.iterkeys(), reverse=True**)`

**`	for mykey in mykeys**:`

**`		myitem = mydict[mykey**]`

**`		mystatus = myitem['status'**]`

**`		myid = myitem['externalID'**]`

**`		if mystatus == 'WAITING'**:`

**`			# see if it looks to be a legitimate workflo**w`

**`			if myid is not None**:`

**`				log("wf id %s is waiting" % myid**)`

**`				# otherwise silently ignore it for no**w`

**`		else**:`

**`			# lots of messages like this**:`

**`			# wf id None is in this state: READ**Y`

**`			if myid is not None**:`

**`				log("wf id %s is in this state: %s" % (myid, mystatus)**)`

**`			if mystatus == 'SUCCESS'**:`

**`				# stop looking once we find the 1st w**f`

**`				# that has already succeede**d`

**`				retur**n`

**`# simply print each element in the jso**n`

**`for i in wf_list['ids']**:`

**`	examine_status(i**)`

**`exit(0**)`

