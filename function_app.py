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

            speech_config = speechsdk.SpeechConfig(subscription=ai_service_key, region=ai_service_region)
            audio_config = speechsdk.audio.AudioConfig(filename="")
            speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, \
            audio_config=audio_config)

            topic = "the season of the fall"
            pronunciation_config = speechsdk.PronunciationAssessmentConfig(
                grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
                granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
                enable_miscue=False)
            
            pronunciation_config.enable_prosody_assessment()
            pronunciation_config.enable_content_assessment_with_topic(topic)

            # Create a speech recognizer using a file as audio input.
            language = 'en-US'
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)
            
            # Apply pronunciation assessment config to speech recognizer
            pronunciation_config.apply_to(speech_recognizer)

            speech_recognition_result = speech_recognizer.recognize_once()
            # The pronunciation assessment result as a Speech SDK object
            pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(speech_recognition_result)

            # The pronunciation assessment result as a JSON string
            pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)

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