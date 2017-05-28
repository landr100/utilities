#!/usr/bin/python

# print os versions

from utils import *

Lsb = '/etc/lsb-release'

def print_file(my_file):
    if File('a').exists(my_file):
        print(run_cmd("cat %s" % my_file))

print_file("/etc/issue") # e.g. => Ubuntu 10.04.4 LTS \n \l
print(run_cmd("uname -a")) # e.g. on home mac: 'Darwin Macintosh-109add5916f4.local 13.4.0 Darwin Kernel Version 13.4.0: date; root:xnu-2422.115.4~1/RELEASE_X86_64 x86_64'
print_file(Lsb)

