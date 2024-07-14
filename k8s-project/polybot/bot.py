import json
import uuid

import boto3
import telebot
from botocore.exceptions import NoCredentialsError
from loguru import logger
import os
import time
from telebot.types import InputFile

images_bucket = "youssefs-bucket"


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)
        #self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', certificate=open('YOURPUBLIC.pem', 'r'))
        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        logger.info(f'Sending text to chat_id: {chat_id}, text {text}\n')
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class ObjectDetectionBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        # for testing only to send back the message
        # self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')

        if self.is_current_msg_photo(msg):
            photo_path = self.download_user_photo(msg)

            # TODO upload the photo to S3
            logger.info(f'Photo uploaded to S3. S3 URL started : s3://{images_bucket}/{photo_path}')
            image_id = self.upload_to_s3(photo_path, images_bucket)

            # TODO send a job to the SQS queue
            message = {
                'image': image_id,
                'chat_id': msg['chat']['id']
            }
            message = json.dumps(message)
            queue_name = 'youssefandyoussef'
            sqs_client = boto3.client('sqs', region_name='us-east-1')
            response = sqs_client.send_message(QueueUrl=queue_name, MessageBody=message)
            logger.info(f'Sending to SQS ://{queue_name}/{response}')


            # TODO send message to the Telegram end-user (e.g. Your image is being processed. Please wait...)
            self.send_text(msg['chat']['id'], f'Your image is being processed. Please wait...')

    def upload_to_s3(self, local_path, images_bucket):
        s3 = boto3.client('s3')
        image_id = str(uuid.uuid4())
        image_id = f'{image_id}.jpeg'
        try:
            s3.upload_file(local_path, images_bucket, image_id)
            logger.info(f'Photo uploaded to S3. S3 URL: s3://{images_bucket}/{image_id}')

            return image_id
        except NoCredentialsError:
            logger.error("AWS credentials not available.")
            return None
        except Exception as e:
            logger.error(f"Error uploading photo to S3: {e}")
            return None
