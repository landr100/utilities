#!/usr/bin/python

# utils.py
# general purpose utilities

import glob # glob.glob()
import os, sys # os.stat(), sys.argv[], sys.stderr.write(), os.system()

class Name1(object):
	def __init__(self):
		self._var0 = None
		self._var1 = 0
	def Method1(self, to_print=True):
		if to_print:
			print "in Method1, var1 is %r" % self._var1
	def Method2(self, to_print=True):
		self._var1 += 1
		self.Method1(to_print)

def print_files(files="*.py"):
	filelist = glob.glob(files)
	numfiles = len(filelist)
	if numfiles > 0:
		# get the name and size of each file
		file_stats = [(filename, os.stat(filename).st_size) for filename in filelist]

		# sort by size
		file_stats.sort(lambda a, b: cmp (a[1], b[1]))

		print file_stats

import time # print time.time() # => 1378323705.22
My_now = time.strftime('%F %T') # 2014-09-14 16:16:16
My_today = time.strftime('%F') # 2014-09-14

# mimic the ruby notion of global variables in python
One_minute = 60
One_hour = 60 * One_minute
One_day = One_hour * 24

import socket
My_host = socket.gethostname()

# My_script should be the name of the script that imports this one
My_script = os.path.basename(sys.argv[0]) # ref: http://stackoverflow.com/questions/4152963/get-the-name-of-current-script-with-python

# example of using string match with regex
import re
# simple method to search for a regex in a string
def find(regex, string):
	return re.search(regex, string) is not None

# customize if running on a mac
Is_home_mac = (True if find('iMac|[mM]acintosh|macintodd', My_host) else False)
Is_mac = (True if find('[mM]ac', My_host) or Is_home_mac else False)

import time # time.strftime()

def now():
	return time.strftime('%F %T') # => 2013-12-10 11:18:44

Time_format = "%D %T"

def log(str):
	print "%s : %s" % (time.strftime(Time_format), str)
	sys.stdout.flush() # ref: http://stackoverflow.com/questions/230751/how-to-flush-output-of-python-print

# echo is an alias for log
echo = log

# lower case versions of constants
false = False
true = True
nil = None
argv = sys.argv

def logerr(str):
	sys.stderr.write("%s : %s\n" % (time.strftime(Time_format), str))

# run a command but do not return the output
def run_cmd_no_output(cmd, echo=False):
	if echo:
		log("about to run %s" % cmd.rstrip())

	return os.system(cmd)

import subprocess
def run_cmd(cmd, echo=False):
	if echo:
		log("about to run %s" % cmd.rstrip())

	p = subprocess.Popen([cmd], shell=True, bufsize=3000006, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
	(child_stdout, child_stdin) = (p.stdout, p.stdin)
	# >>> print child_stdout.readlines()
	# ['atest.py\n', 'atest.pyc\n', ..., 'x.rb\n']
	result = ''.join([line for line in child_stdout]) # this one does chomp but we need the newlines
	child_stdout.close()
	p.stdout.close()

	if echo and len(result) > 0:
		log("result is .%s." % chomp(result))

	return result

import time
# this is like an alias
def sleep(delay):
	time.sleep(delay)

# ref: http://code.activestate.com/lists/python-list/259063/
# implement a version of perl and ruby 'chomp'
def chomp(s):
	if s[-1:]=='\n': return s[:-1]
	else: return s

# simulate File.exists?()
class File(str):
	def exists(self):
		return os.path.exists(self._str)
	def exists(self, file):
		return os.path.exists(file)
	def exist(self):
		return os.path.exists(self._str)
	def exist(self, file):
		return os.path.exists(file)

# return true or false if a command exists
def is_cmd(str):
	result = run_cmd("which %s 2>/dev/null | grep -c %s" % (str, str))
	return int(chomp(result)) == 1

# hour minute second
def hms(input_sec):
	sec = float(input_sec)
	d = int(sec / One_day);    sec = sec % One_day
	h = int(sec / One_hour);   sec = sec % One_hour
	m = int(sec / One_minute); sec = sec % One_minute

	rv  = (("%3dd " % d) if d > 0 else "")
	rv += (("%2dh " % h) if h > 0 else "")
	rv += (("%2dm " % m) if m > 0 else "")
	rv += ("0s" if input_sec == 0 else (("%.2fs" % sec) if sec != int(sec) else (("%ds" % sec) if sec <= One_minute and sec > 0 else "")))
	return re.sub('  ', ' ', rv).strip()

# append a line to a file
def append_line(filename, line):
	with open(filename, "ab") as fp:
		fp.write(line + '\n')

# return a string with the current run-time stack
def print_stack():
	import traceback
	my_str = ''.join(traceback.format_stack())
	return re.sub('  ', ' ', re.sub('\n', ';', my_str))

def dlog(msg):
	my_stack = print_stack()
	if len(msg) > 0:
		log("%s from %s" % (msg, my_stack))
	else:
		log("dlog with no msg from %s" % my_stack)

# ref: http://stackoverflow.com/questions/2197451/why-are-empty-strings-returned-in-split-results
# modified implementation of split which returns an empty list if the input is empty
def mysplit(s, delim=None):
	return [x for x in s.split(delim) if x]

if __name__ == "__main__":
	myvar = Name1()
	myvar.Method2()
	myvar.Method2()

	# try again
	Name1().Method2(False)
	Name1().Method2(False)

	log("in utils.py; to test it, run test-utils.py")

# end of file

