#!/usr/bin/env python

# ps.py

from utils import *
# defines a number of things including: My_host, log(), logerr(), run_cmd(), Is_mac

import sys # sys.argv[]
import re # re.sub()

# special case for mac : does not support ps uxf, and different headers

class Ps(object):
    def __init__(self, debug=False):
        if debug:
            log("My_host is %r, My_script is %r" % (My_host, My_script))

        num_args = len(sys.argv) - 1 # the command line is always included

        # if the delay is too small, then simply run this program once
        self.delay = 60
        if num_args > 0:
            self.delay = int(sys.argv[1])
        if self.delay < 30:
            self.delay = 0

        logerr("delay set to %r" % self.delay)

        # define login account name on host
        user = os.environ['USER']
        users = ('%s,%s' % (user, 'lrs-core') if 'lrs' in My_host else user)

        self.ps_cmd = ("ps -M|egrep '^%s|USER'|grep -v grep" % user if Is_mac else ("ps uxf -U %s" % users))

        if debug:
            log("cmd is %r" % self.ps_cmd)

        first_result = self.run_ps_once() # get a string with many rows and then convert to an array
        if debug:
            print first_result # ['rgowin  1360 s000    0.0 S    31T   0:00.05   0:00.11 -bash', 'rgowin  7441 s000    0.0 S    31T   0:00.01   0:00.01 docker run -it ubuntu bash',...]

        header = first_result[0] # => "USER    PID   TT   %CPU STAT PRI     STIME     UTIME COMMAND"
        if debug:
            print header

        # string substitution (replace); ref: https://mail.python.org/pipermail/tutor/2004-October/032320.html
        # remove extraneous spaces and then convert to array
        headings = re.sub('  *', ' ', header).split(' ') # => ['USER', 'PID', 'TT', '%CPU', 'STAT', 'PRI', 'STIME', 'UTIME', 'COMMAND']

        # there might be a python shortcut, but...
        my_hash = {}
        for heading in headings:
            my_hash[heading] = len(my_hash)

        if debug:
            print my_hash # {'STAT': 4, 'PID': 1, 'TT': 2, 'PRI': 5, '%CPU': 3, 'COMMAND': 8, 'USER': 0, 'UTIME': 7, 'STIME': 6}

        self.user = my_hash['USER']
        self.time = my_hash[('UTIME' if Is_mac else 'TIME')]
        self.pid = my_hash['PID']
        self.command_index = header.index('COMMAND') # => 65

    def run_ps_once(self):
        return run_cmd(self.ps_cmd).split('\n') # get a string with many rows and then convert to an array
  
    def run_ps(self):
        for row in self.run_ps_once(): # gets a string with many rows, and converts to an array
            k = re.sub('  *', ' ', row).split(' ') # => ['Robin  5749 s000    0.0 S    31T   0:00.02   0:00.05 -bash']
            if len(k) >= max(self.user, self.pid, self.time):
                # some commands, like for example kafka, can have very long output
                command = row[self.command_index:][:200]
                if len(row[self.command_index:]) > 200:
                    command += '...'
                # print "%s %s %s\t%s" % (k[self.user], k[self.pid], k[self.time], row[self.command_index:][:200])
                print "%s %s %s\t%s" % (k[self.user], k[self.pid], k[self.time], command)
                sys.stdout.flush()

    def run_ps_loop(self):
        while True:
            self.run_ps()
            run_cmd("date 1>&2")

            sys.stderr.write("%s\n" % My_host)

            if self.delay == 0:
                break

            sleep(self.delay)

        exit(0)

# main loop
print_debug_stmts = False
Ps(print_debug_stmts).run_ps_loop()

# end of file

