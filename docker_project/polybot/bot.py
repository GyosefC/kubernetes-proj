import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import boto3
from botocore.exceptions import NoCredentialsError
import requests
import json


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

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    @staticmethod
    def is_current_msg_photo(msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that are sent to the Bot to the current working directory
        :param msg: The message object containing the photo
        :return: The path to the downloaded photo
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        file_extension = os.path.splitext(file_info.file_path)[1]  # Get the file extension
        # file_extension = "." + file_info.file_path.split(".")[-1]  # Get the file extension
        file_name = f"{msg['message_id']}{file_extension}"  # Create a custom file name
        file_path = os.path.join(os.getcwd(), file_name)  # Save the photo in the current working directory

        with open(file_path, 'wb') as photo:
            photo.write(data)

        return file_path

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
        # Check if the message contains text
        if 'text' in msg:
            original_message = msg['text']
        else:
            original_message = "This message doesn't contain any text."
        self.send_text(msg['chat']['id'], f'Your original message: {original_message}')

class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ObjectDetectionBot(Bot):
    def __init__(self, token, telegram_chat_url, s3_bucket_name):
        super().__init__(token, telegram_chat_url)
        self.s3 = boto3.client('s3')
        self.s3_bucket_name = s3_bucket_name
        self.file_name = ''
        self.msg = ''
        self.file_path = ''

    def upload_to_s3(self):
        try:
            self.s3.upload_file(self.file_path, self.s3_bucket_name, self.file_name)
            return True
        except FileNotFoundError:
            logger.error("The file was not found")
            return False
        except NoCredentialsError:
            logger.error("Credentials not available")
            return False


    def handle_message(self, msg):
        self.msg = msg  # update the message every time
        if not msg:
            return
        logger.info(msg)
        logger.info(f'Incoming message: {msg}')
        if self.is_current_msg_photo(msg):
            try:
                # Download the user photo
                self.file_path = self.download_user_photo(msg)
                # Extract file name
                self.file_name = os.path.basename(self.file_path)
                # Upload the photo to S3
                if self.upload_to_s3():  # Ensure self.file_path is assigned before calling upload_to_s3()
                    self.send_text(msg['chat']['id'], "Photo uploaded to S3 successfully!")
                else:
                    self.send_text(msg['chat']['id'], "Failed to upload photo to S3.")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                self.send_text(msg['chat']['id'], "An error occurred while processing the photo.")

    def send_prediction_request(self):
        if not self.msg:
            return
        yolo_api_url = "http://yolo5:8081/predict"  # Update with the correct YOLO API URL
        params = {'imgName': self.file_name}  # Pass the image URL as a query parameter
        logger.info("----------------------------------------")
        try:
            response = requests.post(yolo_api_url, params=params)
            print(response, response.content)
            if response.status_code == 200:
                prediction_results = response.json()
                prediction_results = self.get_detected_objects_count(prediction_results)
                self.send_text(self.msg['chat']['id'], f" {prediction_results}")
            else:
                self.send_text(self.msg['chat']['id'], "Failed to get object detection results")
        except Exception as e:
            logger.error(f"Error sending prediction request: {e}")
            self.send_text(self.msg['chat']['id'], "An error occurred while processing object detection")

    def get_detected_objects_count(self, detection_results):
        # Initialize a dictionary to store the count of each detected object class
        detected_objects_count = {}

        # Iterate through the labels in the detection results and count each object class
        for label in detection_results['labels']:
            object_class = label['class']
            if object_class in detected_objects_count:
                detected_objects_count[object_class] += 1
            else:
                detected_objects_count[object_class] = 1

        # Generate the response string
        response = "Objects detected:\n"
        for obj_class, count in detected_objects_count.items():
            response += f"{obj_class} = {count}\n"

        return response