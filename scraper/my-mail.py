#!/usr/bin/python

# python script to send email

# usage: my-mail.py {filename='my_filename'|--body='b'} [--subject='s'] [--send_to='name@a.com,name2@b.com'] [--attach=filename]

from utils import *

# ref: http://stackoverflow.com/questions/6270782/sending-email-with-python

# Import the email modules we'll need
from email.mime.text import MIMEText # MIMEText()
from email.MIMEMultipart import MIMEMultipart # MIMEMultipart()
from email.MIMEBase import MIMEBase # MIMEBase()
# from email.MIMEText import MIMEText
# from email.Utils import COMMASPACE, formatdate
from email import Encoders # Encoders.encode_base64()

def parse_opts():
    # parse the command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="send email")
    contents = parser.add_mutually_exclusive_group()
    contents.add_argument('-b', '--body', action="store", dest="body", help="body (contents) of email to send", default='')
    contents.add_argument('-f', '--filename', action="store", dest="filename", help="file with contents of email to send", default='')
    parser.add_argument('-S', '--subject', action="store", dest="subject", help="subject line of email message", default='') # pick some app specific default; TODO
    parser.add_argument('-s', '--send_to', action="store", dest="send_to", help="email addresses to send mail to", default='') # by default we use a default distribution list
    parser.add_argument('-a', '--attach', action="store", dest="attach", help="file to send as attachment", default='')

    return parser

def build_msg(body, filename, attach):
    # get the body (contents) of the email message into a string
    if len(body) == 0:
        # read contents from a file
        if File('a').exist(filename):
            fp = open(filename, 'rb')

            my_body = fp.read()
            fp.close()
        else:
            logerr("file %s not found, cannot send by email" % filename)
            exit(2)
    else:
        my_body = body

    # handle attachments, if any (changes the mime type of the msg)
    if len(attach) == 0:
        # Create a plain email message with contents
        msg = MIMEText(my_body)
    else:
        # Create an email message with contents and attachment
        # ref: http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python
        msg = MIMEMultipart()
        msg.attach(MIMEText(attach)) # attach the name
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attach, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    return msg

def build_email(subject, sender_email, receiver_email, attach):
    msg = build_msg(body, filename, attach)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email # could be a comma-separated email list
    return msg

# internal method that does the work
def internal_send_mail(sender_email, receiver_email, msg):
    # Import smtplib for the actual sending function
    import smtplib

    # Send the message via our own SMTP server, but don't include the envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender_email, [receiver_email], msg.as_string())
    s.quit()

# external method that handles exceptions
def send_mail(msg):
    sender_email = msg['From']
    receiver_email = msg['To']
    try:
        internal_send_mail(sender_email, receiver_email, msg)
        return true
    except: # catch *all* exceptions
        # alternatively, use form {except Exception, e:} if you know the Exception name
        # look for a specific type of exception
        e = sys.exc_info()[0]
        if hasattr(e, '__class__'):
            if(e.__class__.__name__ == 'type' and repr(e) == "<class 'socket.error'>"):
                log("socket error, attempted to send %r (%s)" % (msg, str(msg)))
            else:
                print e
                log("exception: class is %r, id is %r, type is %r, repr is %r" % (e.__class__, id(e), type(e), repr(e)))
    return false

# main () {

parser = parse_opts()
args = parser.parse_args()

# set up convenience variables (aliases)
body = args.body
filename = args.filename
subject = (args.subject if len(args.subject) > 0 else "monitoring email from %s" % My_script)
distrib = args.send_to
attach = args.attach

# need a file or a body but not both
if len(body) + len(filename) == 0:
    logerr("need filename or body, missing from %r" % args)
    parser.print_usage()
    exit(1)

if len(attach) > 0:
    if not File('a').exist(attach):
        logerr("cannot send file %s as attachment, file not found" % attach)
        exit(3)

# sender_email == the sender's email address
# receiver_email == the recipient's email address # TODO: confirm send_to looks like a valid list of email addresses
sender_email = 'landr100@gmail.com'
receiver_email = (sender_email if len(distrib) == 0 else distrib) # by default, send email to myself

msg = build_email(subject, sender_email, receiver_email, attach)

if not send_mail(msg):
    # until real email is working, simulate it
    Mail_log = '/Users/robin/bin/outgoing-email.log'
    append_line(Mail_log, "%s : sent msg %r via email" % (time.strftime(Time_format), str(msg)))

    log("updated mail log file %s" % Mail_log)

# }

