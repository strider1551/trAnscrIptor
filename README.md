# TrAnscrIptor
## A python script to transcribe email attachments.

This utalizes OpenAI's Whisper python library and a simple gmail python client to monitor an email address, automatically read the email/download its attachment, and then respond with the transcription of the audio/video file.
This is intended to help transcribe voicemails from PBX systems and other audio files.

<br>

### 1. SETUP

---

#### 1.1 PyTorch

PyTorch can be setup automatically with installation procedure below. In most cases this should be acceptable, as the short length audio files of an email attachment can be processed by Whisper in a reasonable time without GPU acceleration. However if you want to take advantage of your GPU, [consult their documentation](https://pytorch.org/get-started/locally/) and setup PyTorch manually first, especially if you have an AMD graphics card. Note their [verification](https://pytorch.org/get-started/locally/#linux-verification) instructions.

#### 1.2 FFmpeg

[FFmpeg](https://ffmpeg.org/) needs to be installed on your system as a dependency of [Whisper](https://github.com/openai/whisper). It is widely available in most OS package managers. 

<br>

### 2. INSTALLATION

---

```bash
pip install -r requirements.txt
```

> [!IMPORTANT]
> Dependency [jeremyephron/simplegmail](https://github.com/jeremyephron/simplegmail) requires gmail login configuration. See their repository for instructions.

Due to outdated oauth2 libraries in simplegmail and an updated google authentication process, you will need to make an adjustment to the oauth2client library, specifically the oauth2client/client.py file.
Find the line labeled ```OOB_CALLBACK_URN``` and replace its contents with ```http://localhost```

Also, since I'm lazy and don't want to mess around with secrets, create and populate a file in the root directory of this project named __sender_email.txt__ with only the email address you intend to send your transcriptions through. Typically, this will be the email address you authenticate with Google, but there are some worlds where it might be different.

<br>

### 3. TODO

---

- [ ] Add whitelists to only open emails from certain addresses.
 
