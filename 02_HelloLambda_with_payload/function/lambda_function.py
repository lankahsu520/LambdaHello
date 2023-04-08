import json

def lambda_handler(event, context):
	print('Hello, Lambda!')

	return {
		'statusCode': 200,
		'body': 'Hello from Lambda!',
		'key1': event['key1'],
		'key2': event['key2'],
		'key3': event['key3']
	}

def lambda_helper():
	with open('event.json', 'r') as f:
		event = json.load(f)

	return lambda_handler(event, None)

if __name__ == "__main__":
	"""Demonstrate that this is just a function we can run locally"""
	result = lambda_helper()
	print(result)