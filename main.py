from simplegmail import Gmail
import os
import sys
import whisper
from time import sleep
from rich import print

from pathlib import Path

import logging
import transcriptor.custom_logging


# Create logss and terminal output if available
log_level = logging.DEBUG
log_dir = Path(__file__).resolve().parent.joinpath('logs/')
log_file =  log_dir.joinpath('transcriptor.log')
if not log_dir.exists():
    log_file = None
transcriptor.custom_logging.setup_logging(level=log_level, log_file=log_file)
logger = logging.getLogger(__name__)
if log_file is None:
    logger.error(f'Directory for log files does not exist ({log_dir}).')

#Init Gmail
logger.debug(f'Initializing Gmail')
gmail = Gmail()

#Load sender email from file
logger.debug(f'Loading local data')
file = 'sender_email.txt'
with open(file, 'r') as info:
    sender_email = info.read()

#Init whisper...
logger.debug(f'Initializing Whisper')
model = whisper.load_model("turbo")

#Check for messages. Loop this.
logger.debug(f'Begin watching for unread emails')
while(__name__ == "__main__"):
    messages = gmail.get_unread_inbox()

    if messages:
        for message in messages:
            body = []
            return_to = message.sender

            logger.info("To: " + message.recipient)
            logger.info("From: " + message.sender)
            logger.info("Subject: " + message.subject)
            logger.info("Date: " + message.date)
            logger.info("Preview: " + message.snippet)
            logger.info("Message Body: " + message.plain)
            body.append("Hi " + message.sender + ", <br /><br />")
            
            if message.attachments:
                try:
                    for attm in message.attachments:
                        return_subject = attm.filename
                        logger.info("file: " + attm.filename)
                        attm.save(overwrite=True)
                        transcription = model.transcribe(attm.filename)
                        os.remove(attm.filename)
                        body.append("Here's your transcription: <br />")
                        body.append(transcription["text"])
                except Exception as e:
                    body.append("Error: Did you attach an audio file? Forward this to your administrator: <br /><br />")
                    body.append(str(e))
            
            else:
                body.append("No attachment was found. Please try again.")
                body.append("")
                return_subject = "No File Found"


            return_message = {
                "to": return_to,
                "sender": sender_email,
                "subject": return_subject,
                "msg_html": str(body[0] + body[1] + body[2])
            }

            send_message = gmail.send_message(**return_message)
            logger.info('Transcription sent, idling...')

            message.mark_as_read()
            message.trash()

    else:
        print(".")
        sleep(60)