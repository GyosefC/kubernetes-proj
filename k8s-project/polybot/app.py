import json
import flask
from flask import request
import os
from bot import ObjectDetectionBot
from loguru import logger
import boto3
from botocore.exceptions import ClientError


app = flask.Flask(__name__)

def get_secret():
    secret_name = "Token_key_for_YHY_Projects"
    region_name = "us-east-1"

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
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)

    return secret['TELEGRAM_TOKEN']


# TODO load TELEGRAM_TOKEN value from Secret Manager
TELEGRAM_TOKEN = get_secret()
logger.info(f'yourkey {TELEGRAM_TOKEN}')


TELEGRAM_APP_URL = 'https://youssefs.atech-bot.click'


@app.route('/', methods=['GET'])
def index():
    return 'Ok normal'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route(f'/results/', methods=['GET'])
def results():
    prediction_id = request.args.get('predictionId')
    logger.info(f'prediction: {prediction_id}. start processing')
    # TODO use the prediction_id to retrieve results from DynamoDB and send to the end-user
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('PredictionResults')
    response = table.get_item(
        Key={
            'prediction_id': prediction_id
        }
    )
    logger.info(f'results: {response}. end processing')

    chat_id = response['Item']['chat_id']
    text_results = response['Item']['labels']
    logger.info(f'chat_id :{chat_id}, text_results : {text_results}')

    bot.send_text(chat_id, text_results)
    return 'Ok results'


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    app.run(host='0.0.0.0', port=8443, debug=True)
