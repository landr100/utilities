#!/usr/bin/python

# utils.py
# general purpose utilities

import glob # glob.glob()
import os, sys # os.stat(), sys.argv[], sys.stderr.write(), os.system(), os.path.basename(), os.environ, os.getcwd()
import datetime
now = datetime.datetime.now

Time_format = "%D %T"

def log(str):
    print("%s : %s" % (time.strftime(Time_format), str))
    sys.stdout.flush() # ref: http://stackoverflow.com/questions/230751/how-to-flush-output-of-python-print

def logerr(str):
    sys.stderr.write("%s : %s\n" % (time.strftime(Time_format), str))

def print_files(files="*.py"):
    print(os.listdir('.'))

    # interesting iterators
    filelist = glob.glob(files)
    numfiles = len(filelist)
    if numfiles > 0:
        # get the name and size of each file
        file_stats = [(filename, os.stat(filename).st_size) for filename in filelist]

        # sort by size
        file_stats.sort(lambda a, b: cmp (a[1], b[1]))

        print(file_stats)

# aliases
# alias echo log
echo = log
# puts = print # fails
# echo('test')
false = False
true = True
none = nil = None
argv = sys.argv

import time # time.strftime(), time.sleep()
My_now = time.strftime('%F %T') # 2014-09-14 16:16:16
My_today = time.strftime('%F') # 2014-09-14
My_year = int(time.strftime('%Y')) # 2017
from datetime import date, timedelta
My_yesterday = (date.today() - timedelta(1)).strftime('%F')

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
Is_mac = (True if find('[mM]ac|C02NW1MMG3QT', My_host) or Is_home_mac or ('COMMAND_MODE' in os.environ and find('unix', os.environ['COMMAND_MODE'])) else False)

My_home = os.environ['HOME'] # '/Users/rgowin' on mac, '/home/rgowin' on dev/qa
My_data = My_home + '/data' # user's data directory
# /Users/robin on local mac
# hostname mac on local mac
Rgowin = ('/Users/rgowin' if Is_mac else '/home/rgowin')
Rgowin = ('/Users/robin' if My_host.startswith('mac') else Rgowin)
Rgowin_data = Rgowin + '/data'
Rgowin_config = Rgowin + '/config'
My_user = (os.environ['USER'] if 'USER' in os.environ else 'cron') # usually 'rgowin'
Local_dev = '%s/%s' % (My_home, ('local-dev' if Is_mac else 'src'))

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
    result = ''.join([line for line in child_stdout])
    child_stdout.close()
    p.stdout.close()

    if echo and len(result) > 0:
        log("result is .%s." % chomp(result))

    return result

# this is like an alias
def sleep(delay):
    time.sleep(delay)

# ref: http://code.activestate.com/lists/python-list/259063/
# implement a version of perl and ruby 'chomp'
def chomp(s):
    if s[-1:]=='\n' or s[-1:] == '\r': return chomp(s[:-1])
    else: return s

# simulate File.exists?()
class File(str):
    def exists(self):
        return os.path.exists(self._str)
    def exists(self, this_file):
        return os.path.exists(this_file)
    def exist(self):
        return os.path.exists(self._str)
    def exist(self, this_file):
        return os.path.exists(this_file)
    def delete(self, this_file):
        os.remove(this_file)
    def mtime(self, this_file):
        return os.path.getmtime(this_file)
    def size(self, this_file):
        return os.stat(this_file).st_size
    def basename(self, this_file):
        return os.path.basename(this_file)
    def exists_or_exit(self, this_file, msg, status_code):
        if not self.exists(this_file):
            logerr(msg)
            exit(status_code)

# mnmenonic / alias
def pwd():
    return os.getcwd()

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

# rename a file to '.old'
def rename_file(filename):
    if File('a').exists(filename):
        from os import rename
        os.rename(filename, filename+'.old')
        return true
    else:
        return false

Is_interactive = ('PS1' in os.environ) and sys.stdout.isatty()
Is_cron = not Is_interactive

def confirm_host_is(host):
    if not find(host, My_host):
        log("run %s from %s, not %s" % (My_script, host, My_host))
        exit(1)


def confirm_host_is_not(host):
    if find(host, My_host):
        logerr("Run %s from mac, not %s" % (My_script, My_host))
        exit(2)


# print a time duration in human readable format
def format_timedelta(duration):
    if duration.seconds >= 0:
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return '%d hours, %d minutes, %d seconds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%d minutes, %d seconds' % (minutes, seconds)
        elif seconds == 0:
            micro = duration.microseconds
            if micro > 1000:
                return '%r milliseconds' % (micro / 1000)
            else:
                return '%r microseconds' % micro
        else:
            return '%d seconds' % seconds
    else:
        return str(duration)


def get_dirname(dirname):
    return (os.environ[dirname] if dirname in os.environ else os.environ['HOME']+'/%s' % dirname)


if __name__ == "__main__":
    start_time = now()

    log("in utils.py; to test it, run test-utils.py; took %s" % format_timedelta(now() - start_time))


# end of file
