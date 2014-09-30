#!/usr/bin/python

# test-utils.py
# similar in purpose to utilities.rb; general purpose utilities
# test utils.y

from utils import *
# defines a number of things including:
# class Name1(object):
# def print_files()
# One_minute = 60
# One_hour = 60 * One_minute
# One_day = One_hour * 24
# My_host = socket.gethostname() # => 'Robins-MacBook-Pro.local' # ref: http://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
# def now()
# def log(str)
# alias echo log
# def logerr(str)
# def run_cmd_no_output(cmd, echo=False)
# def run_cmd(cmd, echo=False)
# def parse_opts()

# create a class instance and call its methods
# # myvar = utils.Name1()
myvar = Name1()
myvar.Method2()
myvar.Method2()

# try again without saving state
# # utils.Name1().Method2(False)
# # utils.Name1().Method2(False)
Name1().Method2(False)
Name1().Method2(False)

# set up some "aliases"
# # log = utils.log
# # logerr = utils.logerr
# # run_cmd = utils.run_cmd
# # run_cmd_no_output = utils.run_cmd_no_output
# # One_hour = utils.One_hour
# # My_host = utils.My_host
# # My_script = utils.My_script
# # print_files = utils.print_files
# # ruby_subs = utils.ruby_subs

# print "an hour has %d seconds" % One_hour
log("an hour has %d seconds" % One_hour)
logerr("this is a test log to stderr")

# print "current time is: %r" % now()

log(chomp(run_cmd('ls -m', True)))

# print *.py files
print_files("*.py")

# run_cmd_no_output('ls -lt', echo=True)

# opts = utils.parse_opts
# print opts

log("My_host is %r, My_script is %r" % (My_host, My_script))

# test File.exists
j = File('a')
print j.exists('test-utils.py')
print File('a').exists('test-utils.py')

if is_cmd("mvn"):
  log("mvn found")
elif is_cmd("ruby"):
  log("ruby found")
else:
  logerr("neither mvn nor ruby found")

import time
log("now is %r" % My_now)

# python equivalent, sort of, of ruby %w:
# >>> k = 'test1 selftest storage'.split()
# >>> print k
# ['test1', 'selftest', 'storage']

# test new dlog()
dlog("testing dlog()")

