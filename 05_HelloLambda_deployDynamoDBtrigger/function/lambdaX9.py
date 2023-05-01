import json

#import boto3
from awsp9 import *

class lambdaX9_ctx(pythonX9):
	def release(self):
		self.is_quit = 1

	def __init__(self, **kwargs):
		if ( isPYTHON(PYTHON_V3) ):
			super().__init__(**kwargs)
		else:
			super(lambdaX9, self).__init__(**kwargs)

	def awsp9_connect(self):
		self.TableName="Music"
		self.TableNameBak="MusicBak"
		self.awsp9 = awsp9(aws_service=[AWS_SERVICE_DYNAMODB], region=self.awsRegion, dbg_more=DBG_LVL_DEBUG)

	def event2MODIFY2NEW_AND_OLD_IMAGES(self, event, context):
		KEY_LIST=list(event["Records"][0]["dynamodb"]["Keys"].keys())
		self.PK = KEY_LIST[0]
		self.SK = KEY_LIST[1]
		self.PK_VAL = event["Records"][0]["dynamodb"]["Keys"][self.PK]["S"]
		self.SK_VAL = event["Records"][0]["dynamodb"]["Keys"][self.SK]["S"]

		DBG_IF_LN(self, "(awsRegion: {}, eventSourceARN: {})".format(self.awsRegion, self.eventSourceARN))
		DBG_IF_LN(self, "(TableName: {}, PK: {}, SK: {})".format(self.TableName, self.PK, self.SK))

		self.NewImage = event["Records"][0]["dynamodb"]["NewImage"]
		DBG_IF_LN(self, "(NewImage: {})".format(self.NewImage))
		self.OldImage = event["Records"][0]["dynamodb"]["OldImage"]
		DBG_IF_LN(self, "(OldImage: {})".format(self.OldImage))

		#self.awsp9.dydb_attrX_free()
		#self.awsp9.dydb_attrX_addS(key=self.PK, value=self.PK_VAL)
		#self.awsp9.dydb_attrX_addS(key=self.SK, value=self.SK_VAL)
		#self.awsp9.dydb_attrX_addS(key="AlbumTitle", value="Somewhat Famous")
		#self.awsp9.dydb_attrX_addN(key="Price", value=10)
		#self.awsp9.dydb_attrX_addBoolean(key="OutOfPrint ", value=True)
		#self.awsp9.dydb_put_item(TableName=TableName)
		self.awsp9.dydb_attrX_update( self.NewImage )
		self.awsp9.dydb_put_item(TableName=self.TableNameBak)
		
		response = {'statusCode': 200, 'eventName': self.eventName, 'StreamViewType': self.StreamViewType}
		return response

	def event2MODIFY(self, event, context):
		self.StreamViewType = event["Records"][0]["dynamodb"]["StreamViewType"]
		if ( self.StreamViewType == "NEW_AND_OLD_IMAGES" ):
			response = self.event2MODIFY2NEW_AND_OLD_IMAGES(event, context)
		else:
			response = {'statusCode': 200}
		return response

	def event_helper(self, event, context):
		DBG_DB_LN(self, "(event:{})".format(event))
		#DBG_IF_LN(self, "(context:{})".format(context))

		self.awsRegion=event["Records"][0]["awsRegion"]
		self.eventSourceARN=event["Records"][0]["eventSourceARN"]

		self.awsp9_connect()

		self.eventName = event["Records"][0]["eventName"]
		if ( self.eventName == "MODIFY" ):
			response = self.event2MODIFY(event, context)
		else:
			response = {'statusCode': 200}
		return response

	def start(self, event, context):
		DBG_IF_LN(self, "start")

		self.result = self.event_helper(event, context)

		DBG_IF_LN(self, "(self: {})".format( self.result ))
		return self.result

