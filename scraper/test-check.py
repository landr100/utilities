#!/usr/bin/python

# test for the generic log checking program
# clear;echo 'one line only' | ./check.py --logtype=buffer_example

from utils import *
# defines a number of things including:
# def log(str)
# def run_cmd(cmd, echo=False)

print(run_cmd("clear"))

print(run_cmd("echo 'successful log entry' | ./check.py --logtype=buffer_example -v --start=''"))
print(run_cmd("echo 'one line only' | ./check.py --logtype=exact_buffer_example -v --start=''"))

'''
here is what is in the log type buffer_example:

grep buffer_example monitoring.txt
buffer_example,error,app is not available,example of what an app might log as an error message
buffer_example,filename,/buffer,/buffer indicates to read from a buffer (pipe)
buffer_example,success,one line only,simple example where there is only 1 success line
exact_buffer_example,count,exact=1,one line only,match exactly 1 such lines
exact_buffer_example,error,app is not available
exact_buffer_example,filename,/buffer,/buffer indicates to read from a buffer (pipe)
exact_buffer_example,success,one line only

'''
