import flask
from flask import request
import os
import boto3
import json
from bot import ObjectDetectionBot, Bot
from botocore.exceptions import ClientError

# Create a Flask application
app = flask.Flask(__name__)

# Retrieve secrets from AWS Secret Manager
def get_secrets():
    secret_name = "Token_key_for_YHY_Projects"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exception
        print("Error retrieving secrets:", e)
        return None

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Get secrets from AWS Secret Manager
secrets = get_secrets()

# Get TELEGRAM_TOKEN and TELEGRAM_APP_URL
TELEGRAM_TOKEN = secrets['TELEGRAM_TOKEN']
TELEGRAM_APP_URL = secrets['TELEGRAM_APP_URL']
s3_bucket_name = secrets['s3_bucket_name']  # Assuming it's also stored in the same secret

# Initialize the bot with ObjectDetectionBot subclass
bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL, s3_bucket_name)

# Define route for index page
@app.route('/', methods=['GET'])
def index():
    return 'Ok'

# Define webhook route for Telegram messages
@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    req = request.get_json()
    if req and 'message' in req:
        # Handle the message using the bot's handle_message method
        bot.handle_message(req['message'])
        # Request predictions after handling the message
        bot.send_prediction_request()
    return 'Ok'

# Entry point of the script
if __name__ == "__main__":
    # Run the Flask application
    app.run(host='0.0.0.0', port=8443, debug=True)