#!/usr/bin/python

# utils.py
# similar in purpose to utilities.rb; general purpose utilities

import glob # glob.glob()
import os, sys # os.stat(), sys.argv[], sys.stderr.write(), os.system()
# from stat import * # stat.ST_SIZE

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
	# interesting iterators
	filelist = glob.glob(files)
	numfiles = len(filelist)
	if numfiles > 0:
		# get the name and size of each file
		file_stats = [(filename, os.stat(filename).st_size) for filename in filelist]

		# sort by size
		file_stats.sort(lambda a, b: cmp (a[1], b[1]))

		print file_stats

## append to a list
#filelist.append('dummy')

#print filelist

## for loop
#for file in filelist:
	#print file

## range builtins
#for i in xrange(10):
	#print i

#print range(11)

#import time
#print "sleeping"
#time.sleep(3)
#print "awake"

#print time.time() # => 1378323705.22
import time
My_now = time.strftime('%F %T') # 2014-09-14 16:16:16
My_today = time.strftime('%F') # 2014-09-14

#os.mkdir('./tmp')
#os.chdir('./tmp')
#print os.getcwd()
#os.chdir('..')
#print os.getcwd()

# mimic the ruby notion of global variables in python
One_minute = 60
One_hour = 60 * One_minute
One_day = One_hour * 24

import socket
My_host = socket.gethostname() # => 'Robins-MacBook-Pro.local' # ref: http://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname

# My_script should be the name of the script that imports this one
My_script = os.path.basename(sys.argv[0]) # ref: http://stackoverflow.com/questions/4152963/get-the-name-of-current-script-with-python

# example of using string match with regex
# if re.search('cdb|ampapp|ampdb', My_host) is not None:
import re
# this is to remember more easily
def find(regex, string):
	return re.search(regex, string) is not None

Is_home_mac = (True if find('iMac|Macintosh', My_host) else False)
Is_mac = (True if 'Mac' in My_host else False)

import time # time.strftime()

def now():
	return time.strftime('%F %T') # => 2013-12-10 11:18:44

Time_format = "%D %T"

def log(str):
	print "%s : %s" % (time.strftime(Time_format), str)
	sys.stdout.flush() # ref: http://stackoverflow.com/questions/230751/how-to-flush-output-of-python-print

# alias echo log
echo = log
# puts = print # fails
# echo('test')
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
	# ['atest.py\n', 'atest.pyc\n', 'combine.csharp\n', 'combine.csharp.source\n', 'combine.java\n', 'combine.java.source\n', 'combine1.rb\n',
	# 'combine2-test.rb\n', 'combine2.rb\n', 'combine3.rb\n', 'combine4.rb\n', 'combine_test.java\n', 'gen-tcs.rb\n', 'junk.notes\n', 'junk.notes.old\n',
	# ..., 'x.rb\n']
	result = ''.join([line for line in child_stdout]) # this one does chomp but probably we need the newlines
	child_stdout.close()
	p.stdout.close()

	if echo and len(result) > 0:
		log("result is .%s." % chomp(result))

	return result

## borrowed from daily.rb which borrowed from lib/config.rb on dlp1 and modified
#def parse_opts
#	if @opts
#		log "in parse_opts: @opts already defined; returning"
#		return
#	end
#
#	@opts = {}
#	ARGV.delete_if do |x|
#		rv = false # tells delete_if whether to delete this arg
#		if x[/^-{1,2}([^\s=]+)=(.*)/] # match simple --name='some value' without the quotes
#			@opts[$1] = $2
#			rv = true
#		elsif x[/^-{1,2}([^\s=]+)/]
#			@opts[$1] = 1
#			rv = true
#		end
#		rv
#	end
#end
import optparse # optparse.OptionParser()
def old_parse_opts():
	return 0

	# note: these are just examples; the approach in python is different from ruby; no global hash

	# ref: http://stackoverflow.com/questions/20063/whats-the-best-way-to-grab-parse-command-line-arguments-passed-to-a-python-scri

	parser = optparse.OptionParser()

	parser.add_option('-q', '--query', action="store", dest="query", help="query string", default="spam")

	options, args = parser.parse_args()

	print 'Query string:', options.query

	echo("to be continued...")

import time
# this is like an alias
def sleep(delay):
	time.sleep(delay)

# ref: http://code.activestate.com/lists/python-list/259063/
def chomp(s):
	if s[-1:]=='\n': return s[:-1]
	else: return s

# ref: comment embedded in web site http://stackoverflow.com/questions/2554185/match-groups-in-python
# "Caveat: Python re.match() specifically matches against the beginning of the target.
# Thus re.match("I love (\w+)", "Oh! How I love thee") would NOT match.
# You either want to use re.search() or explicitly prefix the regex with appropriate wildcard patterns for re.match(".* I love (\w+)", ...)"

# simulate File.exists?()
class File(str):
	#def __init__(self, my_str):
	#  self._str = my_str
	def exists(self):
		return os.path.exists(self._str)
	def exists(self, file):
		return os.path.exists(file)
	def exist(self):
		return os.path.exists(self._str)
	def exist(self, file):
		return os.path.exists(file)

if __name__ == "__main__":
	# main(unused_arg):
	myvar = Name1()
	myvar.Method2()
	myvar.Method2()

	# try again
	Name1().Method2(False)
	Name1().Method2(False)

	log("in utils.py; to test it, run test-utils.py")

# return true or false if a command exists
def is_cmd(str):
	result = run_cmd("which %s 2>/dev/null | grep -c %s" % (str, str))
	return int(chomp(result)) == 1

# from interrogate import *
# def interrogate(item):

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
	# File.open(filename, 'a') { |f| f.puts line }
	with open(filename, "ab") as fp:
		fp.write(line + '\n')

# return a string with the current stack
def print_stack():
	import traceback
	# traceback.print_stack()
	# for line in traceback.format_stack():
	# print line.strip()
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

# end of file

