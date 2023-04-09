import json

#import boto3
from awsX9 import *

S3_BUCKET_NAME="lambdax9"
S3_REGION_NAME=REGION_US_WEST_1
S3_BUCKET_NAME_BAK="lambdax9bak"

class lambdaX9_ctx(pythonX9):
	def release(self):
		self.is_quit = 1

	def __init__(self, **kwargs):
		if ( isPYTHON(PYTHON_V3) ):
			super().__init__(**kwargs)
		else:
			super(lambdaX9, self).__init__(**kwargs)

	def start(self, event, context):
		DBG_IF_LN(self, "start")
		s3 = awsX9_ctx(aws_service=AWS_SERVICE_S3, region=S3_REGION_NAME, dbg_more=DBG_LVL_DEBUG)
		if (  0 != s3.s3_check_bucket(S3_BUCKET_NAME) ):
			s3_bucket = s3.s3_create_bucket(S3_BUCKET_NAME)

		if (  0 != s3.s3_check_bucket(S3_BUCKET_NAME_BAK) ):
			s3_bucket = s3.s3_create_bucket(S3_BUCKET_NAME_BAK)

		s3.s3_copy_object(S3_BUCKET_NAME, "out.yml", S3_BUCKET_NAME_BAK, "out.yml")
		# to pull a object
		#s3.s3_pull_object(S3_BUCKET_NAME, "out.yml", "1234")

		# to get the object
		#response = s3.s3_get_object(S3_BUCKET_NAME, "out.yml")
		#DBG_IF_LN(self, "(s3_bucket_name: {}, response: {})".format( S3_BUCKET_NAME, response ))

		#s3_bucket_location = s3.s3_get_bucket_location(S3_BUCKET_NAME)
		#DBG_IF_LN(self, "(s3_bucket_name: {}, {})".format( S3_BUCKET_NAME, s3_bucket_location ))

		self.result ={
			'statusCode': 200,
			'body': 'Hello from Lambda!',
			'key1': event['key1'],
			'key2': event['key2'],
			'key3': event['key3']
		}

		DBG_IF_LN(self, "(self: {})".format( self.result ))
		return self.result

