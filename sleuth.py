#!/usr/bin/python
import sys
import argparse
from tools import s3


#Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

#Console Colors
if is_windows:
        G = Y = B = R = W = G = Y = B = R = W = '' #use no terminal colors on windows 
else:
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
    	return ''' python sleuth.py service command
                example: python sleuth s3 list-bucktes
           '''

def parse_args():
        parser = argparse.ArgumentParser(prog='Sleuth', description='AWS Tools', usage=msg())
        parser.error = parser_error
        parser._optionals.title = 'OPTIONS'
        parser.add_argument('service', nargs='?', help='Service , can be EC2, S3 , etc')
        parser.add_argument('command', help='Command')
	parser.add_argument('bucket', help='Provide Bucket Name')
	parser.add_argument('path', help='Provide directory path')
	return parser.parse_args()


def Main():
	args=parse_args()
        if args.service == 's3':
        	if args.command == 'list-permissions':
              		print s3.s3_bucket_acl_ptable()
	if args.service == 's3':
		if args.command == 'list-buckets':
			print s3.s3_list_buckets_ptable()
	if args.service == 's3':
		if args.command == 'bucket-size':
			print s3.s3_size_ptable()
	if args.service == 's3':
		if args.command == 'count-files':
			 print s3.s3_object_count_ptable()
	if args.service == 's3':
		if args.command == 'check-policy':
			s3.s3_check_policy()
	if args.service == 's3':
		if args.command == 'fix-acl-permissions':
			answer=raw_input('Are you sure?: Y/N ')
			if answer=='Y' or answer=='y' or answer=='yes':
				s3.s3_fix_acl_permission()
			elif answer=='N' or answer=='n' or answer=='no':
				print "Wise decision, you may want to change the permissions manually"
			else:
				print "wrong input"							
	if args.service == 's3':
		if args.command == 'download':
			try:
				bucket_name=args.bucket
				tmpdir=args.path
				s3.s3_download_AllFiles_bucket(bucket_name,tmpdir) 
				print "All "+bucket_name+" bucket files has been downloaded to "+tmpdir
			except OSError as e:
				if "File exists" in e:
					print "Directory "+tmpdir+"/"+bucket_name+" already exist" 
if __name__ == '__main__':
	banner()
        Main()
