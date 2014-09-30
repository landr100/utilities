#!/usr/bin/python

# generic log checking program
# check.py --logtype=%r [--date=YYYY-MM-DD] [-v] [-nomail] [-debug] [--start=SSSS]
# e.g. check.py --logtype=myip # test case
# uses reusable class for log scraping

import glob # glob.glob()
import os, sys # os.stat(), sys.argv[], sys.stderr.write(), os.system(), os.pid()
import re # re.sub()

from utils import *
# defines a number of things including:
# My_host
# def log(str)
# def logerr(str)
# def run_cmd(cmd, echo=False)

from checklogs import * # MyLogScraper
from datetime import * # strptime

# this class has a scraper, but is not a scraper
class MyLogMain(object):
	"""main program to call reusable class to scrape a log"""
	def __init__(self):
		self._pid = os.getpid()
		self._bin = '/Users/Robin/bin'
		self._monitoring_text = "%s/monitoring.txt" % self._bin

		if not File('a').exists(self._monitoring_text):
			logerr("Error: monitoring definitions file %r not found, exiting" % self._monitoring_text)
			exit(1)

		# define class constants and other variables

		# TODO: get list of log types from xml file and/or from monitoring_text file

		# get valid types from the monitoring definitions file
		logtypes = run_cmd("grep '^[a-z]' %s | cut -d, -f1 |uniq|tr '\\n' ' '" % self._monitoring_text)
		if len(logtypes) == 0:
			log("Error: host %r not supported; exiting" % My_host)
			exit(2)

		default_types = 'test1 selftest storage'
		self._logtypes = (logtypes + default_types).split() # array version

		# ref: https://docs.python.org/2/howto/argparse.html
		# ref: https://docs.python.org/dev/library/argparse.html
		# see also http://stackoverflow.com/questions/20063/whats-the-best-way-to-grab-parse-command-line-arguments-passed-to-a-python-scri
		# TODO: allow an xml config file with similar command line parameters

		# parse the command line arguments
		import argparse
		parser = argparse.ArgumentParser(description="check log file and send email")
		group1 = parser.add_mutually_exclusive_group()
		group1.add_argument("-v", "--verbose", action="store_true", default=false)
		group1.add_argument("-q", "--quiet", action="store_true", default=true)
		group2 = parser.add_mutually_exclusive_group()
		group2.add_argument("-m", "--send_mail", action="store_true", default=true)
		group2.add_argument("-n", "--no_mail", action="store_true", default=false)

		parser.add_argument('-D', '--debug', action="store_true", dest="debug", help="enable low level debugging", default=false)
		parser.add_argument('-s', '--send_to', action="store_true", dest="send_to", help="email addresses to send mail to", default='') # by default we use a default distribution list
		parser.add_argument('-d', '--date', action="store", dest="date", help="specific date for scraping log", default='') # by default we use a default date
		parser.add_argument('-S', '--start', action="store", dest="start", help="specific line to start scraping", default='') # by default we start scraping with the first line
		parser.add_argument('-t', '--logtype', action="store", dest="logtype", help="log type", required=true) # a 'required option', generally considered bad form
		parser.add_argument('-f', '--logfile', action="store", dest="logfile", help="log filename", default='') # by default we ...
		# 'date' is the date to start scraping e.g. 2014-09-01, whereas 'start' is the starting line e.g. 'abc'

		args = parser.parse_args()

		# set up convenience variables
		self._parser = parser
		self._debug = args.debug
		self._send_mail = args.send_mail # by default we send mail after checking the logs
		self._no_mail = args.no_mail # by default we send mail after checking the logs
		self._verbose = args.verbose
		self._silent = args.quiet # by default, be silent aka not verbose
		self._send_mail = (false if self._verbose else self._send_mail) # make it easier to do -v -nomail
		self._send_to = args.send_to # optionally send this email to a wider distribution list
		# e.g. --send_to='myname@company.com,user1@company.com,user2@company.com'

		# validate a few command-line options
		# validate the 'date' option or take a default value
		# log("args.date is %r" % args.date)
		if len(args.date) > 0:
			if not re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', args.date):
				self.usage("--date must match YYYY-MM-DD, exiting", 10)

			# My_date = Time.parse(args.date)
			self._date = datetime.strptime(args.date, '%Y-%m-%d')
		else:
			self._date = datetime.strptime(My_today, '%Y-%m-%d') # the default is today (could be yesterday)

		if self._debug:
			log("%r : opts is %r, silent is .%r., verbose is .%r., send_mail is .%r." % (My_script, args, self._silent, self._verbose, self._send_mail))

		# log("date is %r" % self._date)

		self._hyphen_date = self._date.strftime("%F") # e.g. 2012-05-23 # has hyphens
		self._slash_date = self._date.strftime("%m/%d/%y") # e.g. 05/23/12 # has slashes

		self._my_type = args.logtype
		# confirm that this is a known type
		found = false
		for known_type in self._logtypes:
			if self._my_type == known_type:
				found = true
				break

		if not found: self.usage("logtype %r is unknown" % self._my_type, 12)

		# define the starting line
		self._start_line = (args.start if len(args.start) > 0 else self._hyphen_date) # e.g. 2012-05-23

		self._logfile_type = My_script + '.' + self._my_type # e.g. check.py.runlog

		# special case allowing to specify a file name on the command line, which over-rides the file name from the definitions file
		if len(args.logfile) > 0:
			# allow over-ride file name on cmd line
			self._logfile_name = args.logfile
			if self._debug: log("over-riding logfile name to be %r" % self._logfile_name)
		else:
			# discover the filename for this log type
			loc = (self._my_type, self._monitoring_text)
			logfile_name = chomp(run_cmd("grep '^%s,filename' %s -m 1|cut -d, -f3" % loc))
			if len(logfile_name) <= 3:
				log("Error: cannot find '^%s,filename,' in %s ; exiting" % loc)
				exit(4)

			my_logdir = self.get_logdir()
			if self._debug: log("my_logdir is %s" % my_logdir) # if @debug

			if find('\*', logfile_name):
				# make a special case for file 'globs':
				# self._logfile_name = Dir.glob(self._logfile_name).sort.reverse.first if self._logfile_name['*']
				filelist = glob.glob(self._logfile_name); filelist.sort()
				self._logfile_name = filelist[-1] # store the last name
			elif find('^/', logfile_name):
				# self._logfile_name = "#{my_logdir}/#{self._logfile_name}" unless self._logfile_name['/'] # look in a standard location by default
				self._logfile_name = logfile_name # use the filename as given, assume its path is relative
			else:
				log("did not find '^/' in %r" % logfile_name)
				self._logfile_name = "%s/%s" % (my_logdir, logfile_name)

		if self._debug: log("logfile name is %s" % self._logfile_name)

		if not (self._logfile_name == '/buffer' or File('a').exists(self._logfile_name)):
			log("Error: log file %s not found, exiting" % self._logfile_name)
			exit(5)

	def __repr__(self):
		# build up a string that represents this instance; select the most significant data members
		return "MyLogMain(filename %r, filetype %r, debug %r,  pid %r)" % (self._logfile_name, self._logfile_type, self._debug, self._pid)

	# get a log file location from the monitoring file
	def get_location(self, heading):
		found_it = run_cmd("grep -m 1 '^%s,env,' %r | cut -d, -f3" % (heading, self._monitoring_text))
		return (found_it.split('=')[1] if len(found_it) > 0 else nil)

	# find out the location of the log file for this type of log
	def get_logdir(self):
		# first try to get this specific log type from the monitoring definitions file
		first_try = self.get_location(self._my_type)
		if first_try: return first_try

		# now see if this host has a default location
		host_type = re.sub('[0-9]+', '', My_host)
		second_try = self.get_location(host_type)
		if second_try: return second_try

		if self._debug: log("Warning: can't find default location of log files for type %s and host %s" % (self._my_type, host_type))
		# exit(3)

		# third try: can we find filename for this logtype?
		# grep '^myip,filename' /Users/Robin/bin/monitoring.txt -c
		# 1
		if int(run_cmd("grep '^%s,filename' %s -c -m 1" % (self._my_type, self._monitoring_text))) == 1:
			logdir = chomp(run_cmd("dirname $(grep '^%s,filename' %s -m 1|cut -d, -f3)" % (self._my_type, self._monitoring_text)))
			return logdir
			# robin@Macintosh-109add5916f4:~/mydocs/development$ dirname $(grep '^myip,filename' /Users/Robin/bin/monitoring.txt -m 1|cut -d, -f3)
			# /Users/Robin/bin
		else:
			log("Error: can't find location of log files for type %s and host %s" % (self._my_type, host_type))
			exit(3)

	def usage(self, msg, exit_code):
		# logtype_msg = re.sub(self._logtypes_str, ' ', '|') # .gsub(/[",]/,'') # pretty-print the list of logtypes
		logtype_msg = '|'.join(self._logtypes)
		# logtype_msg = re.sub(logtype_msg, '[",]', '') # pretty-print the list of logtypes
		# TODO: get the list from the array and pretty print it
		# log("usage: #{@my_script_name} --logtype=#{logtype_msg} [--date=YYYY-MM-DD] [-v] [-nomail] [-debug] [--start=SSSS]"
		if self._debug: self._parser.print_usage()
		log("usage: %s --logtype=%r [--date=YYYY-MM-DD] [-v] [-nomail] [-debug] [--start=SSSS]" % (My_script, logtype_msg))
		if msg: log(msg) # the second message is optional
		exit(exit_code)

	def __print_list(self, my_str, my_list):
		print my_list
		my_list_str = ','.join(my_list)
		if len(my_list_str) > 0:
			dlog(my_str + ':' + my_list_str)
		else:
			dlog(my_str + ':' + ' empty list')

	def __print_lists(self, success_list, errors_list, warnings_list):
		self.__print_list('success', success_list)
		self.__print_list('errors', errors_list)
		self.__print_list('warnings', warnings_list)

	# read the appropriate lists from a file and instantiate the scraper based on those lists
	def read_lists(self):
		# read in each list one at a time; note, python split is different than ruby with handling of final delimiter
		# success_list = run_cmd("grep '^#{@my_type},success' #{self._monitoring_text} | cut -d, -f3").split(/\n/).uniq
		# errors_list = run_cmd("grep '^#{@my_type},error' #{self._monitoring_text} | cut -d, -f3").split(/\n/).uniq
		# warnings_list = run_cmd("grep '^#{@my_type},warning' #{self._monitoring_text} | cut -d, -f3").split(/\n/).uniq
		success_list = chomp(run_cmd("grep '^%s,success' %s | cut -d, -f3 | uniq" % (self._my_type, self._monitoring_text))).split('\n')
		errors_list = chomp(run_cmd("grep '^%s,error' %s | cut -d, -f3 | uniq" % (self._my_type, self._monitoring_text))).split('\n')
		warnings_list = chomp(run_cmd("grep '^%s,warning' %s | cut -d, -f3 | uniq" % (self._my_type, self._monitoring_text))).split('\n')
		if self._debug: self.__print_lists(success_list, errors_list, warnings_list)

		tempfile = "/tmp/%s.%s.tmp" % (self._my_type, os.environ['USER'])

		# handle special cases for starting lines:; not currently implemented

		self._my_buffer = []

		# special case for scraping a buffer
		if self._logfile_name == '/buffer':
			# reset a few variables
			self._logfile_name = nil # reading from a buffer, not from a file
			# if len(args.start) == 0: self._start_line = '' # unless @opts['start'] # start scraping at the beginning of the buffer, unless specified on cmd line # seems redundant; TODO

			# read each line from stdin into a buffer
			# ref: http://stackoverflow.com/questions/1450393/how-do-you-read-from-stdin-in-python
			self._my_buffer = sys.stdin.readlines()
			dlog(self._my_buffer)

			# no input ==> nothing to check
			if len(self._my_buffer) == 0: exit(0)

		# template is:
		# def __init__(logfile_name, logfile_type=nil, start_line='', end_line=nil, warnings_list=[], errors_list=[], success_list=[],
		# error_if_unknown=false, debug=false, tempfile=nil, retain_if_success=false, my_buffer=[], ignore_dupes=false)
		# default values: end_line=nil, error_if_unknown=true, retain_if_success=false, ignore_dupes=false
		self._scraper = MyLogScraper(self._logfile_name, self._logfile_type, self._start_line, nil, warnings_list, errors_list, success_list,
			true, self._debug, tempfile, false, self._my_buffer, true)

		if self._debug: log("scraper is %s" % self._scraper)

	# scrape either a file or a buffer
	def scrape_log(self, send_mail=false):
		if len(self._my_buffer) == 0:
			self._scraper.scrape(send_mail, silent=self._silent)
		else:
			self._scraper.buffer_scrape(send_mail, silent=self._silent)

		if self._debug: log("results of scraping log file %s are : %s" % (self._logfile_name, self._scraper))

	# process optional "exact match" monitoring
	def process_exact_matches(self):
		# read in each list one at a time, for example, look for lines like these:
		# applog,count,exact=1,about to copy files .buyer.*201.*.csv.gz. to ftp server,match exactly 1 such line
		# applog,count,exact=11,about to copy file buyer.*csv.gz$,match exactly 11 such lines
		# exact_list = run_cmd("grep '^#{@my_type},count' #{self._monitoring_text} | cut -d, -f3,4").split(/\n/).uniq # => ["exact=1,about to.*", "exact=11,about to.*"]
		# return unless exact_list.length > 0
		exact_list = chomp(run_cmd("grep '^%s,count' %s | cut -d, -f3,4 | uniq" % (self._my_type, self._monitoring_text))).split('\n') # => ["exact=1,about to.*", "exact=11,about to.*"]
		if len(exact_list) == 0: return

		dlog(exact_list)

		errors_list = []
		warnings_list = []

		exact_num = 0
		# exact_list.each do |my_list|
		for my_list in exact_list:
			# parse each item in the list
			strings = my_list.split(',') # => ["exact=1", "about to.*"]
			num_exact_matches = int(strings[0].split('=')[1]) # => 1
			success_list = [strings[1]] # => ["about to.*"]

			exact_num += 1
			# tempfile = "/tmp/#{@my_type}.#{ENV['USER']}.exact#{exact_num}.tmp"
			tempfile = "/tmp/%s.%s.exact%d.tmp" % (self._my_type, os.environ['USER'], exact_num)

			# this_scraper = MyLogScraper.new(@logfile_name, @logfile_type, start_line=@start_line, end_line=nil, warnings_list, errors_list, success_list,
				# error_if_unknown=false, debug=@debug, tempfile, retain_if_success=true, my_buffer=@my_buffer, ignore_dupes=false)
			# template is:
			# def __init__(logfile_name, logfile_type=nil, start_line='', end_line=nil, warnings_list=[], errors_list=[], success_list=[],
			# error_if_unknown=false, debug=false, tempfile=nil, retain_if_success=false, my_buffer=[], ignore_dupes=false)
			# default values: end_line=nil, ignore_dupes=false
			self._scraper = MyLogScraper(self._logfile_name, self._logfile_type, self._start_line, nil, warnings_list, errors_list, success_list,
				false, self._debug, tempfile, false, self._my_buffer, false)

			# scrape the log
			# this_scraper.scrape_log(mail=false, silent=self._silent)
			self.scrape_log(false) # send_mail=false
			# if self._debug: log("results of scraping log file %s for exact match .%r. are : %r" % (self._logfile_name, my_list, this_scraper)) # or str(this_scraper)

			# see if we matched the number needed
			# msg = "#{num_exact_matches} line(s) like #{success_list.inspect}"
			msg = "%d line(s) like %r" % (num_exact_matches, success_list)
			if num_exact_matches == len(self._scraper._saved_lines):
				msg = "found " + msg
				self._scraper.num_success = num_exact_matches # redundant?
			else:
				msg = "did not find %r; found %d line(s) instead" % (msg, len(self._scraper._saved_lines))
				self._scraper.num_errors = 1

			# log msg if self._debug || !self._silent
			if self._debug or not self._silent: log(msg)

			if self._send_mail:
				# build the appropriate command line: success if found the expected number of matches, error if not
				self._scraper._saved_lines = [[msg, 1]] # reset the list
				cmd_line = self._scraper.build_cmd_line(self._silent)
				run_cmd(cmd_line, self._debug)

# end of class definition

# main program:

# process command line options, set up standard variables
my_main = MyLogMain()
print my_main

# read in the success, warning, error lists for this type of monitoring
my_main.read_lists()

# scrape the log
send_mail = my_main._send_mail
my_main.scrape_log(send_mail)
log("results of scraping log file %s are : %s" % (my_main._logfile_name, my_main._scraper))

# process 'exact matches' (i.e. looking for a specific number of lines matching a string), if any
# TODO: if searching for exact matches, should we also search for non-exact matches?
my_main.process_exact_matches()

# email results if requested on the command line (the default is to send email)
if send_mail:
	cmd_line = my_main._scraper.build_cmd_line(my_main._silent)
	# cmd_line looks like "cm_mail.py --subject='check-dlp-daily.py monitoring:status=green' --body='...'" ; add the network id to the subject line if applicable

	if my_main._send_to: cmd_line += " --send_to=%s" % my_main._send_to
	# e.g. --send_to='myname@company.com,user1@company.com,user2@company.com'

	if my_main._debug: log(cmd_line)

	# TODO: if the file is too big, don't send it - or send only the first N lines
	run_cmd(cmd_line)

exit(0)

# end of file

