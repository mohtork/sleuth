import boto3
import ast
import itertools
from prettytable import PrettyTable
from blessings import Terminal
from cloudwatsh import cw_s3_size as s3size
from botocore.exceptions import ClientError, ParamValidationError

s3client= boto3.client('s3')
s3resource = boto3.resource('s3')

def s3_list_buckets():
	bucket_list = []
	s3 = boto3.resource('s3')
	for bucket in s3.buckets.all():
		bucket_list.append(bucket.name)
	return bucket_list

def s3_put_private_acl(bucket_name):
	t = Terminal()
        bucket=s3resource.Bucket(bucket_name)
        bucket.Acl().put(ACL='private')
	print t.green(bucket_name) + " public acl removed from Everyone group"

def s3_get_region(bucket_name):
	region= s3client.head_bucket(Bucket=bucket_name)['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']	
	return region

def get_s3_keys(bucket):
        keys = []
        response = s3client.list_objects_v2(Bucket=bucket)
        for object in response['Contents']:
                keys.append(object['Key'])
        return len(keys)

def s3_bucket_acl():
        bucket_list = s3_list_buckets()
	dict={}
	dict1={}
        for name in bucket_list:
		bucket_acl = s3client.get_bucket_acl(Bucket=name)
                list =  bucket_acl.values()[1]
        	for n in range(len(list)):
        		index_number= n
                	list_of_permissions = list[n]['Grantee']
                	permissions = list[n]['Permission']
                        URL = str(list_of_permissions.get('URI'))
			Type = list_of_permissions.get('Type')
			aws_id = list_of_permissions.get('DisplayName')
			buckets = {'account': aws_id, 'name': name, 'url': URL, 'permission': permissions}
			dict1.setdefault('result', []).append(buckets)
			dict.update(dict1)
	return dict

def s3_get_policy(bucket_name):
        s3_policy_list=[]
        try:
                response = s3client.get_bucket_policy(
                  Bucket=bucket_name
                )


                response_dict=ast.literal_eval(response[u'Policy'])
                action=response_dict['Statement'][0]['Action']
                princible=response_dict['Statement'][0]['Principal']
                resource=response_dict['Statement'][0]['Resource']
                effect=response_dict['Statement'][0]['Effect']
                sid=response_dict['Statement'][0]['Sid']
                s3_policy_list.extend([princible['AWS'], effect, sid])

        except ClientError as e:
		raise
                #if "NoSuchBucketPolicy" in e.message:
                #        print "No policy attached"
        return s3_policy_list

			

def find(key, dictionary):
	for k, v in dictionary.iteritems():
        	if k == key:
            		yield v
        	elif isinstance(v, dict):
            		for result in find(key, v):
                		yield result
        	elif isinstance(v, list):
            		for d in v:
                		for result in find(key, d):
                    			yield result


def s3_bucket_acl_check():
	acl= s3_bucket_acl()
	find_url= list(find('url', acl))
	l = []
	permissions_dict={}
	for index in range(len(find_url)):
		Permission= acl['result'][index]['permission']
        	Name= acl['result'][index]['name']
        	Account= acl['result'][index]['account']
		if "global/AllUsers" in find_url[index]:
			permissions_dict.setdefault(Name, []).append(Permission)
		elif "s3/LogDelivery" in find_url[index]:
			Permission= Permission+'_LOG'
			permissions_dict.setdefault(Name, []).append(Permission)
		else:
			Permission= Permission+'_'+str(Account)
			permissions_dict.setdefault(Name, []).append(Permission)
	return permissions_dict
	

def s3_bucket_acl_ptable():
	x = PrettyTable(["Bucket Name", "Owner Permissions", "Admin Permissions", "S3 Log", "Public"])
        x.align["Bucket"] = "l"
        x.padding_width = 1
	acl_result= s3_bucket_acl_check()
	t = Terminal()
	print t.red('any permissions in Public column need your attention')
	for bucket_name, bucket_permissions in acl_result.iteritems():
		OWNER=filter(lambda y: '_aws' in y, acl_result[bucket_name])
		OWNER=[w.replace('_aws', '') for w in OWNER]
		ADMIN=filter(lambda y: '_admin' in y, acl_result[bucket_name])
		ADMIN=[w.replace('_admin', '') for w in ADMIN]
		S3LOG=filter(lambda y: '_LOG' in y, acl_result[bucket_name])
		S3LOG=[w.replace('_LOG', '') for w in S3LOG]
		PERMISSIONS=["READ", "WRITE", "READ_ACP", "WRITE_ACP", "FULL_CONTROL"]
		PUBLIC=[i for i in PERMISSIONS if i in acl_result[bucket_name]]
		x.add_row([bucket_name, str(OWNER)[1:-1], str(ADMIN)[1:-1], str(S3LOG)[1:-1], str(PUBLIC)[1:-1] ])
	return x.get_string()

def s3_list_buckets_ptable():
	x = PrettyTable(["S3 Buckets"])
        x.align["S3 Buckets"] = "l"
        x.padding_width = 1
	bucket_names= s3_list_buckets()
	for bucket in bucket_names:
		x.add_row([bucket])
        return x.get_string()

def s3_size_ptable():
	x = PrettyTable(["Bucket Name", "Size in MB"])
        x.align["Bucket Name"] = "l"
        x.padding_width = 1
	bucket_list=s3_list_buckets()
	for bucket in bucket_list:
		region= s3_get_region(bucket)
		size= s3size(bucket, region)
		if size == None:
			size=0
		x.add_row([bucket,size])
        return x.get_string(sortby='Size in MB', reversesort=True)	

def s3_object_count_ptable():
	bucket_list=s3_list_buckets()
	x = PrettyTable(["Bucket Name", "Number of Files"])
        x.align["Bucket Name"] = "l"
        x.padding_width = 1
	for bucket in bucket_list:
		try:
			count=get_s3_keys(bucket)
		except KeyError:
			count=0
		x.add_row([bucket,count])
	return x.get_string(sortby='Number of Files', reversesort=True)

def s3_check_policy():
	t = Terminal()
	public_access=['*', 'Allow', 'AllowPublicRead']
	bucket_list=s3_list_buckets()
	for bucket in bucket_list:
		try:
			bucket_policy=s3_get_policy(bucket)
			if bucket_policy==public_access:
				print t.red("Attention! ")+ " Bucket "+ t.yellow(bucket) + " has public access"
			elif bucket_policy!=public_access:
				print t.green("Congratulation! ")+ "Bucket "+ t.yellow(bucket) + " has no public access"
		except ClientError as e:
			if "NoSuchBucketPolicy" in e.message:
                        	print "No Policy attached for "+ t.yellow(bucket)  

def s3_fix_acl_permission():
	bucket_list=s3_list_buckets()
        for bucket in bucket_list:
		s3_put_private_acl(bucket)


