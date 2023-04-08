import json

def lambda_handler(event, context):
	print('Hello, Lambda!')

	return {
		'statusCode': 200,
		'body': 'Hello from Lambda!'
	}

def lambda_helper():
	return lambda_handler(None, None)

if __name__ == "__main__":
	"""Demonstrate that this is just a function we can run locally"""
	result = lambda_helper()
	print(result)