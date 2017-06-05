"""
Audio Test Alexa Skill:
-----------------------------
    Alexa plays a random audio from the playlist.
    Alexa pause the audio.
    Alexa resume the audio.
"""

import logging
import random
import requests
from flask import Flask, json
from flask_ask import Ask, question, audio, logger

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

playlist = ["https://archive.org/download/1999-04-16.paf.sbd.unknown.10169."
            "sbeok.flacf/pf99-04-16d2t06.mp3",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169."
            "sbeok.flacf/pf99-04-16d2t04.mp3",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169."
            "sbeok.flacf/pf99-04-16d3t01.ogg",
            "https://archive.org/download/1999-04-16.paf.sbd.unknown.10169."
            "sbeok.flacf/pf99-04-16d2t01.ogg",
            "https://archive.org/download/FemaleVoiceSample/Female_VoiceTalent"
            "_demo.mp4"]  # playlist with the audio


def random_song():
    """
    Get a random number from the list.
    :return: the stream url.
    """
    x = random.randrange(0, 5)
    stream_url = playlist[x]
    return stream_url


@ask.launch
def launch():
    """
    Starts the skill.
    """
    card_title = 'Testing Audio'
    text = 'Welcome to a testing audio example. You can ask to play a random song.'
    prompt = 'You can ask to play a random song.'
    _infodump(text)
    return question(text).reprompt(prompt).simple_card(card_title, text)


@ask.intent('RandomIntent')
def random_song_intent():
    """
    Alexa plays the random audio from the playlist
    """
    speech = 'Here is a random song from the playlist.'
    _infodump("random")
    x = random.randrange(0, 5)
    stream_url = random_song()
    _infodump(stream_url)
    return audio(speech).play(stream_url)


@ask.intent('AMAZON.PauseIntent')
def pause_audio():
    """
    Alexa pause the random audio from the playlist
    """
    text = 'Pause the audio.'
    _infodump(text)
    return audio('Pause the audio.').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume_audio():
    """
    Alexa resume the random audio from the playlist
    """
    text = 'Resuming.'
    _infodump(text)
    return audio('Resuming.').resume()


@ask.session_ended
def session_ended():
    return "", 200


def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)


if __name__ == '__main__':
    app.run(debug=True)
