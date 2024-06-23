import boto3


def upload_file_to_s3(file_path, bucket_name, object_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the file to S3
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
    print("File successfully uploaded to S3")
    return True


# Example usage of the function to upload a file
file_path = 'demofile'
bucket_name = 'alexey--demo'
object_name = 'demofile'  # This will be the file name in your S3 bucket

upload_file_to_s3(file_path, bucket_name, object_name)
