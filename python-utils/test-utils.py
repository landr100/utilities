#!/usr/bin/python

# test-utils.py
# test code in utils.y

from utils import *
start_time = now()
# defines a number of things including:
# def print_files()
# One_minute = 60
# One_hour = 60 * One_minute
# One_day = One_hour * 24
# My_host = socket.gethostname() # => 'Robins-MacBook-Pro.local' # ref: http://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
# def log(str)
# alias echo log
# def logerr(str)
# def run_cmd_no_output(cmd, echo=False)
# def run_cmd(cmd, echo=False)
# def parse_opts()

log("an hour has %d seconds" % One_hour)
logerr("this is a test log to stderr")

log(chomp(run_cmd('ls -m', True)))

# print *.py files
print_files("*.py")

log("My_host is %r, My_script is %r, Is_mac is %r, My_home is %r, My_user is %r" % (My_host, My_script, Is_mac, My_home, My_user))

# test File.exists
j = File('a')
if j.exists('test-utils.py') != File('a').exists('test-utils.py'):
    logerr("problem with File('a').exists()")

if is_cmd("mvn"):
  log("mvn found")
elif is_cmd("ruby"):
  log("ruby found")
else:
  logerr("neither mvn nor ruby found")

import time
log("now is %r" % My_now)

# test new dlog()
dlog("testing dlog()")

try:
    # confirm "today" and "yesterday" are calculated accurately
    from dateutil import parser
    today_timestamp = parser.parse(My_today)
    yesterday_timestamp = parser.parse(My_yesterday)
    delta_timestamp = today_timestamp - yesterday_timestamp
    if re.sub(',.*$', '', str(delta_timestamp)) != "1 day":
        logerr("expecting 1 day delta but got %r instead" % delta_timestamp)
except:
    logerr("no dateutil.parser, can't check time stamp")

my_full_script = "%s/bin/%s" % (My_home, My_script)
print("my script (%s) last modified at %d and its size is now %d and basename is %r" % \
    (My_script, j.mtime(my_full_script), j.size(my_full_script), j.basename(my_full_script)))

# test interactive vs cron
has_ps1 = 'PS1' in os.environ # '/Users/rgowin' or '/home/rgowin' or False
is_tty = sys.stdout.isatty()

if has_ps1:
    if is_tty:
        log("both ps1 and tty")
    else:
        log("oops, ps1 but not tty")
elif is_tty:
        log("oops, ps1 but not tty")
else:
    log("neither ps1 nor tty")

print(Is_interactive)

has_nl = 'this is a test ending with a newline\n'
if len(chomp(has_nl)) != len(has_nl) - 1:
    logerr("chomp(%r) did not work" % has_nl)

has_crlf = has_nl + '\r'
if len(chomp(has_crlf)) != len(has_crlf) - 2:
    logerr("chomp(%r) did not work" % has_crlf)

# C02NW1MMG3QT
confirm_host_is(My_host)
if My_host == 'C02NW1MMG3QT':
    confirm_host_is_not(Dev_sb)
else:
    confirm_host_is_not('C02NW1MMG3QT')

if j.exist("%s/music/utils/prog-type.sh" % Local_dev):
    # verify this script
    old_expecting = 'mini(also known as tec-mls)'
    expecting = 'mini'
    actual = chomp(run_cmd("%s/music/utils/prog-type.sh corp-llm1" % Local_dev))
    if actual != expecting:
        logerr("warning, getting corp-llm1 prog type, expecting %r but got %r" % (expecting, actual))
elif not Is_mac:
    # on mac these files have been moved
    logerr("warning: script file %s/music/utils/prog-type.sh not found" % Local_dev)

log("running %s took %s" % (My_script, format_timedelta(now() - start_time)))

j.exists_or_exit('%s/%s' % (os.environ['bin'], My_script), "my file %s must exist" % My_script, 99)
j.exists_or_exit('/x/y/z', "normal exit", 0)

# end of file
