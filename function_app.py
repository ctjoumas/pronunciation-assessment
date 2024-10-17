import azure.functions as func # type: ignore
import logging
import os
import azure.cognitiveservices.speech as speechsdk

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ai_service_region = os.environ.get('AI_SERVICE_REGION')
    ai_service_key = os.environ.get('AI_SERVICE_KEY')

    name = req.params.get('name')
    if not name:
        try:

            """performs one-shot speech recognition with input from an audio file"""
            # <SpeechRecognitionWithFile>
            speech_config = speechsdk.SpeechConfig(subscription=ai_service_key, region=ai_service_region)
            audio_config = speechsdk.audio.AudioConfig(filename="samples_python_console_pronunciation_assessment_fall.wav")
            # Creates a speech recognizer using a file as audio input, also specify the speech language
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, language="en-us", audio_config=audio_config)

            # Starts speech recognition, and returns after a single utterance is recognized. The end of a
            # single utterance is determined by listening for silence at the end or until a maximum of about 30
            # seconds of audio is processed. It returns the recognition text as result.
            # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
            # shot recognition like command or query.
            # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
            result = speech_recognizer.recognize_once()

            # Check the result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            # </SpeechRecognitionWithFile>

            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )