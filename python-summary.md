# summary of my python experience

Note: all examples and names have been anonymized and generalized, to eliminate any proprietary information, while still illustrating actual programming completed while at other employers.

Developed 20+ scripts to automate tasks, perform data validation, facilitate production support

## automation

* utils.py		basic utilities

* ps.py		customize output of ps aux; also loop

* dig-test.py	confirm connectivity to hosts

* versions.py	show versions of various installed components

* organize.py	organize structure of file systems between laptop and home mac

* sync.py	synchronize work mac and home mac; get local backups of source

* NNN-sync.py	synchronize automation scripts for ias project between hosts

* myscp.py	copy files between hosts; symbolically linked to get hostname

* get-os.py	print info about hosts's OS

* myip.py	print info about host's IP address

* utc.py		print time and date in UTC time zone

## data validation

* NNN-validate.py	data validation of new Third Party daily log files (60 million lines)

* count-ctrla.py	count number of delimiters in Third Party data files

* dt-gs-hourly.py	download an hourly DT imps file from google storage and parse it to get time, application id1, and application id2

## database queries

* query-NNN-status.py	query status table in postgres database

## data analysis and aggregation

* segment-look.py	ported from ruby to improve performance; count uniques in a segment file (up to 30GB)

## production support

* check-NNN.py	check status of hourly and daily download, log processing, and file transfer jobs that run on Hadoop and produce files for Netezza

* APP-query.py	 	 monitor status of job or jobs running in APP as part of workflow

* check-APP.py		 check status of "APP" application by scanning app log files

* oozie-status.py	 print status of workflow job in oozie (Hadoop scheduler)

* get-activity-types.py	 count activity types for building up monitoring for reporting subsystem

## at Google

* 3 production programs part of Data Transfer port from DoubleClick to Google infrastructure; part of a pipeline to create hourly "DT" files, organize files, keep track of files, and copy from Google stack back to DoubleClick stack for subsequent delivery to customers

## for personal use

* developed generic and reusable programs to monitor text and send automated email with subject line allowing to filter normal results and only view mails with warnings or errors

