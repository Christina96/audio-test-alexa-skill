import logging
import random

from flask import Flask, json
from flask_ask import Ask, question, audio, logger

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.INFO)

playlist = ["https://archive.org/download/1999-04-16.paf.sbd.unknown.10169.sbeok.flacf/pf99-04-16d2t06.mp3",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169.sbeok.flacf/pf99-04-16d2t04.mp3",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169.sbeok.flacf/pf99-04-16d3t01.ogg",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169.sbeok.flacf/pf99-04-16d2t01.ogg",
            "https://archive.org/download/FemaleVoiceSample/Female_VoiceTalent_demo.mp4"]


def random_song():
    x = random.randrange(0, 5)
    stream_url = playlist[x]
    return stream_url


@ask.launch
def launch():
    card_title = 'Testing Audio'
    text = 'Welcome to a testing audio example. You can ask to play a random song.'
    prompt = 'You can ask to play a random song.'
    _infodump(text)
    return question(text).reprompt(prompt).simple_card(card_title, text)


@ask.intent('RandomIntent')
def random_song_intent():
    speech = 'Here is a random song from the playlist.'
    _infodump("random")
    x = random.randrange(0, 5)
    stream_url = random_song()
    _infodump(stream_url)
    return audio(speech).play(stream_url)


@ask.intent('AMAZON.ResumeIntent')
def resume_audio():
    text = 'Resuming.'
    _infodump(text)
    return audio('Resuming.').resume()


@ask.intent('AMAZON.PauseIntent')
def pause_audio():
    text = 'Pause the audio.'
    _infodump(text)
    return audio('Pause the audio.').stop()


@ask.session_ended
def session_ended():
    return "", 200


def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)


if __name__ == '__main__':
    app.run(debug=True)
