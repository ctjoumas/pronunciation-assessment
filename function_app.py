import azure.functions as func # type: ignore
import logging
import os
from pronunciation_assessment_continuous import pronunciation_assessment_continuous_from_file

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

file_name = os.getenv("FILE_NAME")
reference_text = os.getenv("REFERENCE_TEXT")

@app.route(route="pronunciation_assessment_trigger")
def pronunciation_assessment_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # reference text is optional and is only used if you run a scripted assessment, which will compare the speech against
    # the reference text. If teachers will have a known passage/text the students will read, we can use this which will
    # then include the completeness score below. If we are not using the scripted assessment, we will not be calculating
    # the completeness score (see below)

    pronunciation_assessment_continuous_from_file(file_name=file_name, reference_text=reference_text)

    return func.HttpResponse(        
            "This HTTP triggered function executed successfully.",
            status_code=200
        )