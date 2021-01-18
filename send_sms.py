import boto3
from botocore.exceptions import NoCredentialsError
from boto.s3.connection import S3Connection
def send_sms(message, filename):

	print('Sending sms')
	# Create an SNS client
	client = boto3.client(
    		"sns",
    		aws_access_key_id="<AWS-ACCESS-TOKEN>",
    		aws_secret_access_key="<AWS-SECRET-KEY>",
    		region_name="us-east-1"
	)

# Create the topic if it doesn't exist (this is idempotent)
# Send your sms message.
	link = get_link_from_s3(filename)
	
	response = client.publish(
	    PhoneNumber="1234567891011",
	    Message="Alert 🚨 : "+message+" View the captured face by clicking on this link : "+link
  
	)
	if(response):
        	print("Message sent")
	else:
        	print("Message not sent")
		
def get_link_from_s3(filename):
	ACCESS_KEY = '<AWS-ACCESS-TOKEN>'
	SECRET_KEY = '<AWS-SECRET-KEY>'


	aws_connection = S3Connection(ACCESS_KEY, SECRET_KEY)
	bucket = aws_connection.get_bucket('<BUCKET-NAME>')
	for file_key in bucket.list():
		if (file_key.name == filename):
			return "https://<BUCKET-NAME>.s3.amazonaws.com/"+file_key.name
