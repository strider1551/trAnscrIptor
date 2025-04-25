from simplegmail import Gmail
import os
import whisper
from time import sleep
from rich import print

#Init Gmail
print(f'initializing Gmail')
gmail = Gmail()

#Load sender email from file
print(f'Loading local data')
file = 'sender_email.txt'
with open(file, 'r') as info:
    sender_email = info.read()

#Init whisper...
print(f'initializing Whisper')
model = whisper.load_model("turbo")
print(f'Done!\n')

#Check for messages. Loop this.
while(__name__ == "__main__"):
    messages = gmail.get_unread_inbox()

    if messages:
        for message in messages:
            body = []
            return_to = message.sender

            print("To: " + message.recipient)
            print("From: " + message.sender)
            print("Subject: " + message.subject)
            print("Date: " + message.date)
            print("Preview: " + message.snippet)
            print("Message Body: " + message.plain)
            body.append("Hi " + message.sender + ", <br /><br />")
            
            if message.attachments:
                try:
                    for attm in message.attachments:
                        return_subject = attm.filename
                        print("file: " + attm.filename)
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
            print('Transcription sent, idling...')

            message.mark_as_read()
            message.trash()

    else:
        print(".")
        sleep(60)