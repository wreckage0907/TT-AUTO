from telegram import Bot
import os 
from dotenv import load_dotenv
import requests
import json
import datetime
import schedule
import time

load_dotenv()
id = os.getenv('TELE_ID')
bot_token = os.getenv('TELE_TOK')


def send_message(message_text):
    app = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={id}&text={message_text}'
    response = requests.get(app)

def check_classes():
    with open('wwi.json') as f:
        schedule_data = json.load(f)

    current_day = datetime.datetime.today().strftime('%a').upper()
    current_time = datetime.datetime.now().strftime('%H:%M')

    for class_slot in schedule_data.get(current_day, []):
        for class_details in class_slot:
            class_start_time = class_details["Start"]
            class_location = class_details["Location"]
            class_title = class_details["Title"]
            class_description = class_details["Description"]
            class_start_datetime = datetime.datetime.strptime(class_start_time, '%H:%M')
            time_difference = class_start_datetime - datetime.datetime.strptime(current_time, '%H:%M')
            if 0 < time_difference.total_seconds() <= 300:
                message_text = f"Reminder: You have a class starting in 5 minutes!\nClass Title: {class_title}\nLocation: {class_location}\nDescription: {class_description}"
                send_message(message_text)

schedule.every(1).minutes.do(check_classes)

while True:
    schedule.run_pending()
    time.sleep(1)
