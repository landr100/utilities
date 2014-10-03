#!/usr/bin/python

# generic and reusable "log scraper" to check a log file and return status for monitoring purposes
# the basic idea is to enable automated email filtering of any monitoring email that does not require attention i.e. 'normal'
# but to have the email be flagged if there is an error
# also if done properly, the contents and format of the email can populate a visual monitoring dashboard (which is yet to be built)

from utils import *
# defines a number of things including:
# class Name1(object):
# def print_files()
# One_minute
# One_hour
# One_day
# My_host
# def now()
# def log(str)
# alias echo log
# def logerr(str)
# def run_cmd_no_output(cmd, echo=False)
# def run_cmd(cmd, echo=False)
# def parse_opts()
# Is_mac

import sys # sys.argv[]
import re # re.sub()
import os # os.getpid()

# basic sequence of events / features:
# open a log file name L logtype T # Logfile # Type
# start scraping at line in file L that matches S # Start
# keep scraping until EOF or line that matches E # End
# for each line Line that is scraped:
#	increment num_warnings if Line matches [W1, W2, ..., Wn] # Warnings
#	increment num_errors   if Line matches [E1, E2, ..., En] # Errors
#	increment num_success  if Line matches [S1, S2, ..., Sn] # Success
#	increment num_unknown  if Line does not match any of the above # optionally: increment num_errors
#	increment num_examined
#	save contents and line number if match a warning or an error or an unknown
#
# when done:
# send email with subject = "logtype monitoring:status={green|yellow|red} body=B [numerrs=num_errors] [numwarn=num_warnings]"

# first test case: check-pg.rb

class MyLogScraper(object):
	"""reusable class to scrape a log"""
	def __init__(self, logfile_name, logfile_type=nil, start_line='$', end_line=nil, warnings_list=[], errors_list=[], success_list=[],
		error_if_unknown=false, debug=false, tempfile=nil, retain_if_success=false, my_buffer=[], ignore_dupes=false):
		self._pid = os.getpid()

		# initialize instance variables
		self._num_warnings = 0
		self._num_errors = 0
		self._num_success = 0
		self._num_examined = 0
		self._num_ignored = 0
		self._saved_lines = []
		self._line_num = 0
		self._examined_lines = {} # save what we examined in case we are ignoring dupes

		# copy variables passed in to constructor
		self._logfile_name = logfile_name
		from os.path import basename
		self._logfile_basename = (basename(logfile_name) if logfile_name is not None and File('a').exists(logfile_name) else 'buffer')
		self._logfile_type = (logfile_type if logfile_type is not None else My_script) # default to the name of the script
		self._start_line = start_line
		self._end_line = end_line
		self._warnings_list = warnings_list
		self._errors_list = errors_list
		self._success_list = success_list
		self._error_if_unknown = error_if_unknown
		self._debug = debug
		self._silent = not debug
		from os import environ
		self._tempfile = (tempfile if tempfile is not nil else ('/tmp/' + My_script + '.' + environ['USER'] + '.' + str(self._pid) + '.log'))
		self._retain_if_success = retain_if_success
		self._my_buffer = my_buffer
		self._ignore_dupes = ignore_dupes
		# keep track if scraping has started
		self._started_scraping = false

	def __repr__(self):
		# build up a string that represents this instance; select the most significant data members
		status = (self.__summarize() if self._started_scraping else 'scraping not yet started')

		return "MyLogScraper(filename %r, filetype %r, status %r, pid %r)" % (self._logfile_name, self._logfile_type, status, self._pid)

	def __save_line(self, line):
		# some input might be url encoded, so decode it first
		from urllib import unquote
		self._saved_lines += [[unquote(line), self._line_num]] # an array of arrays
		return true

	def __examine(self, line):
		line = chomp(line)

		found_something = false
		self._num_examined += 1

		# ignore dupes if that's what we're asked to do
		if line in self._examined_lines:
			if self._ignore_dupes: return false # skip this line
		else:
			self._examined_lines[line] = true # we have examined this line

		# examine the line and see if it belongs to any category
		# first look for an error, then a warning, then a success
		# if none of the above then it is 'unknown'
		for errors in self._errors_list:
			if re.search(errors, line) is not None:
				# TODO: make this one method with flag 'error' or 'warning'
				if not self._silent:
					log("error: line number %r : .%r." % (self._line_num, line))

				self._num_errors += 1
				found_something = true
				break

		# TODO: make this one method
		if found_something:
			self.__save_line(line)
			return true

		for warning in self._warnings_list:
			if re.search(warning, line):
				if not self._silent:
					log("warning: line number %r : .%r." % (self._line_num, line))

				self._num_warnings += 1
				found_something = true
				break

		if found_something:
			self.__save_line(line)
			return true

		for success in self._success_list:
			if re.search(success, line):
				self._num_success += 1
				if self._retain_if_success: self.__save_line(line)
				return true # all done for now

		# if we get here, then the line is unknown
		if self._error_if_unknown:
			self._num_errors += 1
			self.__save_line(line)
		else:
			self._num_ignored += 1

		return false # TODO: confirm the default return value is/should be false
		# end of def __examine()

	def __line_is_start(self, line):
		return (re.search(self._start_line, line))

	def __scrape_line(self, line, found_start):
		self._started_scraping = true
		self._line_num += 1
		if found_start:
			self.__examine(line)
		elif self.__line_is_start(line):
			if self._debug: log("found first occurrence of start line at line number %s" % self._line_num)
			found_start = true
			self.__examine(line)
		return found_start

	# build a string which will be the subject part of the email line
	def __subject_line(self):
		# send email with subject = "logtype monitoring:status={green|yellow|red} [numerrs=num_errors] [numwarn=num_warnings]"
		msg = "%s:%s monitoring:status=" % (self._logfile_basename, self._logfile_type)
		if self._num_errors > 0:
			msg += "red numerrs=%d numwarn=%d" % (self._num_errors, self._num_warnings)
		elif self._num_warnings > 0:
			msg += "yellow numwarn=" + str(self._num_warnings)
		else:
			msg += 'green'

		return msg

	# summarize the results of scraping this log
	def __summarize(self, silent=true):
		summary = "examined "
		summary += (str(self._num_examined) if self._num_ignored == 0 else "%d of %d" % (self._num_examined-self._num_ignored, self._num_examined)) + " lines "
		summary += "in %s log file %s, found" % (self._logfile_type, self._logfile_name)
		if self._debug: log("saved_lines is %r" % self._saved_lines)
		if self._num_errors > 0:
			summary += " %d errors (%d:%s) and %d warnings" % (self._num_errors, self._saved_lines[0][1], self._saved_lines[0][0], self._num_warnings)
		elif self._num_warnings > 0:
			summary += " %d (%d:%s) warnings" % (self._num_warnings, self._saved_lines[0][1], self._saved_lines[0][0])
		else:
			summary += " no problems"

		if not silent: log(summary)

		return summary

	# this public method builds a command line for sending email
	def build_cmd_line(self, silent=true):
		# send the most recent status line by email
		# send email with subject = "logtype monitoring:status={green|yellow|red} [numerrs=@num_errors] [numwarn=@num_warnings]"

		cmd_line = "my-mail.py --subject='%s' " % self.__subject_line()

		# put results in a temp file if there is more than 1 error and/or warning
		if self._num_warnings + self._num_errors > 0:
			fp = open(self._tempfile, "w")
			for line in self._saved_lines:
				fp.write("%d: %s\n" % (line[1], line[0]))
			fp.close()

			cmd_line += "--attach " + self._tempfile # attach the temp file to the email message; optionally copy its contents as the body (TODO)
		else:
			cmd_line += "--body='%s'" % self.__summarize(silent)

		return cmd_line + ' 2>&1'

	# finish scraping: build command line, optionally run it, and return it
	def __finish_scraping(self, send_mail, silent):
		cmd_line = self.build_cmd_line(silent)

		if send_mail: run_cmd(cmd_line)
		return cmd_line

	# this public method scrapes from a log file
	def scrape(self, send_mail=false, silent=false):
		self._silent = silent

		# start reading the file and note when we find the first line containing the starting string; from that point forward, examine each line in the file
		# ref: http://stackoverflow.com/questions/12902540/read-from-a-gzip-file-in-python
		import gzip
		in_fp = (gzip.open if find('\.gz', self._logfile_name) else open)(self._logfile_name, 'rb')

		found_start = false
		for line in in_fp:
			found_start = self.__scrape_line(chomp(line), found_start)

		in_fp.close()

		return self.__finish_scraping(send_mail, silent)

	# add to the success list e.g. for special cases
	def __obsolete_append_success(self, my_list):
		self._success_list += my_list # TODO: confirm python += matches ruby concat

	# this public method scrapes from a buffer (array of strings) and it borrows as much logic from the 'scrape()' method above as possible
	def buffer_scrape(self, send_mail=false, silent=false):
		# start reading the buffer and note when we find the first line containing the starting string; from that point forward, examine each line in the buffer
		found_start = false
		for line in self._my_buffer: # 'buffer' is a builtin class in python
			found_start = self.__scrape_line(line, found_start)

		# make the messages more obvious that a log file was not scraped
		self._logfile_name = 'buffer(pipe)'

		return self.__finish_scraping(send_mail, silent)

# end of file

