#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
#
# Microsoft Cognitive Services (formerly Project Oxford): https://www.microsoft.com/cognitive-services
#
# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
import base64
import json
import time
import os


def pronunciation_assessment_continuous_rest(reference_text, audio_file_nm):
    subscriptionKey = os.environ.get('AI_SERVICE_KEY')
    region = os.environ.get('AI_SERVICE_REGION')

    # build pronunciation assessment parameters
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % reference_text
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-us" % region
    headers = {'Accept': 'application/json;text/xml',
               'Connection': 'Keep-Alive',
               'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
               'Ocp-Apim-Subscription-Key': subscriptionKey,
               'Pronunciation-Assessment': pronAssessmentParams,
               # 'Transfer-Encoding': 'chunked',
               'Expect': '100-continue'}

    audioFile = open(audio_file_nm, 'rb')

    # send request with chunked data
    uploadFinishTime = time.time()
    response = requests.post(url=url, data=audioFile, headers=headers)
    getResponseTime = time.time()
    audioFile.close()

    resultJson = json.loads(response.text)
    print(json.dumps(resultJson, indent=4))

    latency = getResponseTime - uploadFinishTime
    print("Latency = %sms" % int(latency * 1000))
    return response.json()

     # Return the result as a structured dictionary
    return resultJson


# a generator which reads audio data chunk by chunk
# the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
def get_chunk(audio_source, chunk_size=1024):
    # a common wave header, with zero audio length
    # since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
    WaveHeader16K16BitMono = bytes(
        [82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0,
         125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0])

    yield WaveHeader16K16BitMono
    while True:
        time.sleep(chunk_size / 32000)  # to simulate human speaking rate
        chunk = audio_source.read(chunk_size)
        if not chunk:
            global uploadFinishTime
            uploadFinishTime = time.time()
            break
        yield chunk


# This is for testing by directly calling rest endpoint

# reference_text= "If Nancy knew more about very small things, " \
#                 "she wouldn't have been so afraid of climbing to high places to find water"
# audio_file_nm = "sample_01.wav"

# reference_text= "The little green man answered, Of course its me. I've come to see if you're happy. No, I'm not happy, Nancy said. And why not? the green man asked"
# audio_file_nm = "sample_03.wav"
# pronunciation_assessment_continuous_rest(reference_text, audio_file_nm)