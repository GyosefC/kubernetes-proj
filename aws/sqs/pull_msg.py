import boto3

# SQS queue name
QUEUE_NAME = 'Alexey-demo-sqs'

# Create an SQS client
sqs = boto3.client('sqs', region_name="ca-central-1")

# Get the queue URL by its name
queue_url = 'https://sqs.ca-central-1.amazonaws.com/933060838752/Alexey-demo-sqs'


# Receive a message from the SQS queue
def receive_message_from_sqs():
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=3,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )
        # If there is a message in the queue, print it
        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            print("Received message from SQS:", message['Body'])

            # Delete the message from the SQS queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print("Message deleted from SQS.")
        else:
            print("No messages in the queue.")
    except Exception as e:
        print("Error receiving message from SQS:", e)


# Example usage of the function to receive and print a message
receive_message_from_sqs()
