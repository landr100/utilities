#!/usr/bin/python

# convert between octal, hex, and decimal(int)

# usage:
# hex.py --from={hex|oct|int|bin} --to={hex|oct|int|bin} NNNN
# for example:
# hex.py --from int --to bin 15 # should output 1111

import glob # glob.glob()
import os, sys # os.stat(), sys.argv[], sys.stderr.write(), os.system(), os.pid()
import re # re.sub()

from utils import * # def logerr(str)

My_map = {'hex' : [hex, 16], 'int' : [int, 10], 'oct' : [oct, 8], 'bin' : [bin, 2]}

# example call: convert('ff', 'hex', 'bin')
# expected outcome: convert 'ff' from hex to binary
def convert(value, my_from, my_to):
    my_from = My_map[my_from]
    my_to = My_map[my_to]
    # treat the input as a string, convert it from one base,
    # and then convert it to another base
    return my_to[0](int(value, my_from[1]))

# confirm the conversion is working properly
# TODO: use a unit test framework

bff = '0b11111111'
bf  = '0b1111'
hf = '0xf'
i15 = 15

should_be_binary = convert('ff', 'hex', 'bin')
if should_be_binary != bff:
    logerr("convert function returned %r but was expecting %r" % (should_be_binary, bff))
    exit(1)

should_be_hex = convert(bf, 'bin', 'hex')
if should_be_hex != hf:
    logerr("convert function returned %r but was expecting %r" % (should_be_hex, hf))
    exit(2)

should_be_int = convert(bf, 'bin', 'int')
if int(should_be_int) != i15:
    logerr("convert function returned %r but was expecting %r" % (should_be_int, i15))
    exit(3)

# parse the command line arguments
import argparse
parser = argparse.ArgumentParser(description="convert between different bases")
my_keys = My_map.keys()
parser.add_argument('-f', '--from', action="store", dest="arg_from", help="base to convert from", choices=my_keys, required=true)
parser.add_argument('-t', '--to', action="store", dest="arg_to", help="base to convert to", choices=my_keys, required=true)
parser.add_argument('value', nargs=1, help="value to convert") # the value to be converted
parser.add_argument("-v", "--verbose", action="store_true", default=false)

args = parser.parse_args()

result = convert(args.value[0], args.arg_from, args.arg_to)
print ("%r converted from %r to %r is %r" % (args.value[0], args.arg_from, args.arg_to, result) if args.verbose else result)

