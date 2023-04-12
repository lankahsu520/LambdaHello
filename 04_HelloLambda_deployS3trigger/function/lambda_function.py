from lambdaX9 import *

lambdaX9=lambdaX9_ctx()

def lambda_handler(event, context):
	return lambdaX9.start(event, context)

def lambda_helper():
	with open('event.json', 'r') as f:
		event = json.load(f)

	return lambda_handler(event, None)

if __name__ == "__main__":
	"""Demonstrate that this is just a function we can run locally"""
	result = lambda_helper()

