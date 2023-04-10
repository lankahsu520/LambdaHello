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

	def awsx9_s3_connect(self):
		self.awsx9 = awsX9_ctx(aws_service=AWS_SERVICE_S3, region=S3_REGION_NAME, dbg_more=DBG_LVL_DEBUG)
		if (  0 != self.awsx9.s3_check_bucket(S3_BUCKET_NAME) ):
			s3_bucket =  self.awsx9.s3_create_bucket(S3_BUCKET_NAME)

		if (  0 !=  self.awsx9.s3_check_bucket(S3_BUCKET_NAME_BAK) ):
			s3_bucket =  self.awsx9.s3_create_bucket(S3_BUCKET_NAME_BAK)

	def event_s3_delete(self, event, context):
		s3_bucket_name = S3_BUCKET_NAME_BAK
		s3_object_name =self.s3_object_name
		self.awsx9.s3_delete_object(S3_BUCKET_NAME_BAK, s3_object_name )
		response = {'statusCode': 200, 'eventName': self.s3_object_eventName, 'bucket': self.s3_object_bucket, 'object': self.s3_object_name}
		return response

	def event_s3_put(self, event, context):
		self.s3_object_size = event["Records"][0]["s3"]["object"]["size"]
		s3_bucket_from = self.s3_object_bucket
		s3_object_from = self.s3_object_name
		s3_bucket_to = S3_BUCKET_NAME_BAK
		s3_object_to = self.s3_object_name
		self.awsx9.s3_copy_object(s3_bucket_from, s3_object_from, s3_bucket_to, s3_object_to )
		response = {'statusCode': 200, 'eventName': self.s3_object_eventName, 'bucket': self.s3_object_bucket, 'object': self.s3_object_name}
		return response

	def event_s3_others(self, event, context):
		DBG_IF_LN(self, "(s3_object_eventName: {})".format( self.s3_object_eventName ))
		response = {'statusCode': 200, 'eventName': self.s3_object_eventName}
		return response

	def event_s3_helper(self, event, context):
		self.s3_object_name = event["Records"][0]["s3"]["object"]["key"]
		self.s3_object_bucket = event["Records"][0]["s3"]["bucket"]["name"]
		self.s3_object_eventTime= event["Records"][0]["eventTime"]
		self.s3_object_eventName = event["Records"][0]["eventName"]

		DBG_IF_LN(self, "(s3_object_eventName: {})".format( self.s3_object_eventName ))
		if ( self.s3_object_eventName == "ObjectCreated:Put" ):
			response = self.event_s3_put(event, context)
		elif ( self.s3_object_eventName == "ObjectRemoved:Delete" ):
			response = self.event_s3_delete(event, context)
		else:
			response = self.event_s3_others(event, context)
		return response

	def start(self, event, context):
		DBG_IF_LN(self, "start")

		self.awsx9_s3_connect()

		self.result = self.event_s3_helper(event, context)

		# to pull a object
		#s3.s3_pull_object(S3_BUCKET_NAME, "out.yml", "1234")

		# to get the object
		#response = s3.s3_get_object(S3_BUCKET_NAME, "out.yml")
		#DBG_IF_LN(self, "(s3_bucket_name: {}, response: {})".format( S3_BUCKET_NAME, response ))

		#s3_bucket_location = s3.s3_get_bucket_location(S3_BUCKET_NAME)
		#DBG_IF_LN(self, "(s3_bucket_name: {}, {})".format( S3_BUCKET_NAME, s3_bucket_location ))

		DBG_IF_LN(self, "(self: {})".format( self.result ))
		return self.result

