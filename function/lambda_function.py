import json

def lambda_handler(event, context):
	print('Hello, Lambda!')

	return {
		'statusCode': 200,
		'body': 'Hello from Lambda!'
	}

if __name__ == "__main__":
	"""Demonstrate that this is just a function we can run locally"""
	result = lambda_handler(None, None)
	print(result)