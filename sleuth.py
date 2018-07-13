#!/usr/bin/python
import sys
import argparse
from tools import s3


#Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

#Console Colors print s3.s3_bucket_acl_ptable()
if is_windows:
        G = Y = B = R = W = G = Y = B = R = W = '' #use no terminal colors on windows else:
        G = '\033[92m' #green
        Y = '\033[93m' #yellow
        B = '\033[94m' #blue
        R = '\033[91m' #red
        W = '\033[0m'  #white

def handle_error():
        print 'Ooops.!! Something went error , please try again' 

def banner():
        print '''%s
                       ^    ^    ^    ^    ^    ^     
                      /S\  /L\  /E\  /U\  /T\  /H\    
                     <___><___><___><___><___><___> v0.1
                  %s%s
        # Coded By ToRk @mohtork Version 0.1%s
        '''%(R,W,Y,W) 

def parser_error(errmsg):
        print 'Usage: python '+sys.argv[0]+' [Options] use -h for help'
        print R+'Error: '+errmsg+W
        sys.exit() 

def msg(name=None):
    	return ''' python sleuth.py option
                example: python cairo.py s3
           '''

def parse_args():
        parser = argparse.ArgumentParser(prog='Sleuth', description='AWS Tools', usage=msg())
        parser.error = parser_error
        parser._optionals.title = 'OPTIONS'
        parser.add_argument('service', nargs='?', help='Type -h')
        parser.add_argument('command', help='Command')
	return parser.parse_args()


def Main():
	args=parse_args()
        if args.service == 's3':
        	if args.command == 'list-permissions':
              		print s3.s3_bucket_acl_ptable()
	elif args.service == 's3':
		if args.command == 'list-buckets':
			print s3.s3_list_buckets_ptable()
	else:
		print "ToRk Didn't Add any other options yet"

if __name__ == '__main__':
        Main()
