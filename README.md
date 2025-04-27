# TrAnscrIptor
## A python script to transcribe email attachments.

This utalizes OpenAI's Whisper python library and a simple gmail python client to monitor an email address, automatically read the email/download its attachment, and then respond with the transcription of the audio/video file.
This is intended to help transcribe voicemails from PBX systems and other audio files.

### Installation

```bash
pip install -r requirements.txt
```

__Note:__ Dependency [jeremyephron/simplegmail](https://github.com/jeremyephron/simplegmail) requires gmail login configuration. See their repository for instructions.

Also, due to outdated oauth2 libraries and an updated google authentication process, you will need to make an adjustment to the oauth2client library, specifically the oauth2client/client.py file.
Find the line labeled ```OOB_CALLBACK_URN``` and replace its contents with ```http://localhost```

Also, since I'm lazy and don't want to mess around with secrets, create and populate a file in the root directory of this project named __sender_email.txt__ with only the email address you intend to send your transcriptions through. Typically, this will be the email address you authenticate with Google, but there are some worlds where it might be different.

### TODO

- [ ] Add whitelists to only open emails from certain addresses.
 
