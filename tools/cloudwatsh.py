import boto3
from datetime import timedelta
from datetime import datetime


def cw_s3_size(bucket, region):

	cw = boto3.client('cloudwatch', region_name=region)
	bucket_name = bucket

	response = cw.get_metric_statistics(
    		Namespace='AWS/S3',MetricName='BucketSizeBytes',
    		StartTime=datetime.utcnow() - timedelta(days=2) ,
    		EndTime=datetime.utcnow(), Period=86400,
    		Statistics=['Average'], Unit='Bytes',
    		Dimensions=[
        	{'Name': 'BucketName', 'Value': bucket_name},
        	{u'Name': 'StorageType', u'Value': 'StandardStorage'}
    		])

	for item in response["Datapoints"]:
		size= item['Average']
		sizeMB = size/1000/1000
		return sizeMB
		
