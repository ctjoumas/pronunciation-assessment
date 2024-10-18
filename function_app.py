import azure.functions as func # type: ignore
import logging
from pronunciation_assessment_continuous import pronunciation_assessment_continuous_from_file

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="pronunciation_assessment_trigger")
def pronunciation_assessment_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pronunciation_assessment_continuous_from_file()
    return func.HttpResponse(
            "This HTTP triggered function executed successfully, but no pipeline_id was provided.",
            status_code=200
        )