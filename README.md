utilities
=========

# Generic Reusable Application Log Scraper

## Author

Robin Gowin, September 2014

## Overview

I have developed a generic and reusable Python class, and a main program that scrapes log files. These software tools can be used as part of application monitoring. Main features:

* easy to customize

* automated monitoring that sends results by email

* email subject line simplifies filtering on "success", “warning”, or “error”

* search for regular expressions ("regex")

* easily extensible to other monitoring tools such as hipchat, riemann, graphite

* scrape application log files or include as part of an application pipeline

* can process compressed log files

* optionally process "exact matches" such as “must contain exactly 1 line like this”

# High level design

The main two components are in source code files checklogs.py and check.py. A helper function "my-mail.py" automates sending of email results.

## checklogs

This program defines a reusable class called MyLogScraper which performs the scraping of logs, either a file or a buffer (for pipelines). Public methods:

	def scrape(self, send_mail=false, silent=false):

	def buffer_scrape(self, send_mail=false, silent=false):

	def build_cmd_line(self, silent=true):

### scrape method

Callers use this method to scrape a log file; it is the primary interface. Options include whether to send email and whether to print status messages.

### buffer_scrape method

Callers use this method to scrape a buffer, i.e. a pipe as part of a larger pipeline command. The interface is similar to the scrape method.

### build_cmd_line method

Used in conjunction with either scrape message, allows the caller to determine whether or not to run the command that sends email with the results of the log scraping.

## check

The default check.py program demonstrates a typical example of how to use the checklogs class. The design of the main program looks like:

* instantiate the class, process command line options

* cache the success, warning, and error lists

* scrape the log, optionally send email, process exact matches

### high level source

The source code for check looks like this

# process command line options, set up standard variables

my_main = MyLogMain()

# read in the success, warning, error lists for this type of monitoring

my_main.read_lists()

# scrape the log

my_main.scrape_log()

# process 'exact matches' (i.e. looking for a specific number of lines matching a string), if any

my_main.process_exact_matches()

## my-mail.py

Program to send email to a specified distribution. Command-line looks like:

my-mail.py --subject=’sss’ [--body=’bbb’ | --file=filename ] [--send_to=’email_distro’] [--attach=afilename]

### command line options

* subject line (required)

* email body (optional)

* file containing body of email (optional)

* email distribution list (optional)

* file to include as attachment (optional)

# Use Cases

The following table illustrates a handful of potential use cases for log scraping.

<table>
  <tr>
    <td>Use Case</td>
    <td>Purpose</td>
    <td>Monitoring</td>
  </tr>
  <tr>
    <td>database extract</td>
    <td>extract 90 tables from SQL db</td>
    <td>confirm all 90 tables were extracted; confirm status line</td>
  </tr>
  <tr>
    <td>database copy</td>
    <td>copy tables to remote server</td>
    <td>confirm all tables copied successfully</td>
  </tr>
  <tr>
    <td>database load</td>
    <td>load tables into db appliance</td>
    <td>confirm all tables load successfully</td>
  </tr>
  <tr>
    <td>disk space monitoring</td>
    <td>monitor disk space</td>
    <td>alert if above a specified percentage</td>
  </tr>
  <tr>
    <td>storage trending</td>
    <td>graph storage usage over time</td>
    <td>interface with riemann and graphana</td>
  </tr>
  <tr>
    <td>application log monitoring</td>
    <td>monitor progress of application</td>
    <td>ability to scrape any number of logs produced by applications</td>
  </tr>
  <tr>
    <td>cron changes</td>
    <td>monitor changes to cron jobs</td>
    <td>as new jobs are developed and automated, confirm that existing cron jobs are still running e.g. not commented out</td>
  </tr>
  <tr>
    <td>input file dependencies</td>
    <td>confirm time and size of input files</td>
    <td>verify that expected source input files are being produced when expected</td>
  </tr>
  <tr>
    <td>hourly processing</td>
    <td>confirm dependencies</td>
    <td>verify that hourly files are produced on schedule</td>
  </tr>
  <tr>
    <td>middle tier uptime</td>
    <td>confirm api status</td>
    <td>send message to middle tier and confirm that message was processed correctly</td>
  </tr>
  <tr>
    <td>daily snapshot</td>
    <td>confirm db lookup</td>
    <td>verify that daily metatdata user snapshot file created recently (updated several times per day)</td>
  </tr>
  <tr>
    <td>middleware log</td>
    <td>confirm nginx log</td>
    <td>search nginx logs for errors or warnings</td>
  </tr>
</table>


# source

see github

[https://github.com/landr100/utilities/tree/master/python](https://github.com/landr100/utilities/tree/master/python)

* my utilities
* first version 09/30/14
* push with corrected git config info

