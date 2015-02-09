#!/usr/bin/python

# ps.py
# python version of ps.rb

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

# special case for mac : does not support ps uxf, different headers

Debug = False

def run_ps_once(cmd):
  return run_cmd(cmd).split('\n') # get a string with many rows and then convert to an array

def init():
  if Debug:
    log("My_host is %r, My_script is %r" % (My_host, My_script))

  num_args = len(sys.argv) - 1 # the command line is always included

  # if the delay is too small, then simply run this program once
  delay = 60
  if num_args > 0:
    delay = int(sys.argv[1])
  if delay < 30:
    delay = 0

  logerr("delay set to %r" % delay)

  # USER=robin on mac
  # LOGNAME=robin on mac
  users = ("Robin" if Is_mac else "rgowin") # TODO: define login account name on host

  # use 'in' keyword for string comparison for regex matching # if 'qa-ampapp1' not in My_host:
  if Debug:
    log("users is %r" % users)

  if Is_mac:
    ps_cmd = "ps -M"
  else:
    ps_cmd = "ps uxf -U " + users

  first_result = run_ps_once(ps_cmd) # run_cmd(ps_cmd).split('\n') # get a string with many rows and then convert to an array
  if Debug:
    print first_result

  header = first_result[0] # => "USER    PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND"
  if Debug:
    print header

  # string substitution (replace); ref: https://mail.python.org/pipermail/tutor/2004-October/032320.html
  # remove extraneous spaces and then convert to array
  headings = re.sub('  *', ' ', header).split(' ') # => ['USER', 'PID', 'TT', '%CPU', 'STAT', 'PRI', 'STIME', 'UTIME', 'COMMAND']

  # there might be a python shortcut, but...
  my_hash = {}
  for heading in headings:
    my_hash[heading] = len(my_hash)

  if Debug:
    print my_hash # {'STAT': 4, 'PID': 1, 'TT': 2, 'PRI': 5, '%CPU': 3, 'COMMAND': 8, 'USER': 0, 'UTIME': 7, 'STIME': 6}

  user = my_hash['USER']
  time_s = ('UTIME' if Is_mac else 'TIME')
  time = my_hash[time_s]
  pid = my_hash['PID']
  cmd = my_hash['COMMAND']
  command_index = header.index('COMMAND') # => 65

  return delay, ps_cmd, user, time, pid, cmd, command_index

# end of init() method

def run_ps(cmd):
  for row in run_ps_once(cmd): # gets a string with many rows, and converts to an array
    k = re.sub('  *', ' ', row).split(' ') # => ['Robin  5749 s000    0.0 S    31T   0:00.02   0:00.05 -bash']
    if len(k) >= max(user, pid, time):
      print "%s %s %s\t%s" % (k[user], k[pid], k[time], row[command_index:])
      sys.stdout.flush()

  return

delay, ps_cmd, user, time, pid, cmd, command_index = init()
if Debug:
  print ps_cmd, delay, user, time, pid, cmd, command_index

# main loop

# do not convert from Central to Eastern if running on a NY7 aa box or on a Mac
Convert = ('' if Is_mac or find('aa[nop]', My_host) else "--date='1 hour'|sed 's/CDT/EDT/;s/CST/EST/'")

while True:
  run_ps(ps_cmd)
  run_cmd("date " + Convert + " 1>&2")

  sys.stderr.write("%s\n" % My_host)

  if delay == 0:
    break

  sleep(delay)

exit(0)

# end of file

