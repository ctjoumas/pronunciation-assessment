from flask import Flask, request, jsonify
import logging
from azure_openai_service import sanitize_words
from pronunciation_assessment_continuous import pronunciation_assessment_continuous_from_file
from pronunciation_assessment_rest import pronunciation_assessment_continuous_rest
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/pronunciation_assessment_trigger', methods=['POST'])
def pronunciation_assessment_trigger():
    logging.info('Python HTTP trigger function processed a request.')

    # Check if the request contains the file and reference text
    if 'file' not in request.files or 'reference_text' not in request.form:
        return jsonify(message="File or reference_text is missing."), 400

    # Get the reference text from the form data
    reference_text = request.form['reference_text']

    # Get the uploaded file
    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify(message="No file selected."), 400

    # Secure the filename and save the file locally (temporary)
    filename = secure_filename(audio_file.filename)
    audio_file.save(filename)

    # Uncomment this to test the SDK implementation
    #result = pronunciation_assessment_continuous_from_file(file_name=filename, reference_text=reference_text)

    # Uncomment this to test the REST implementation
    result = pronunciation_assessment_continuous_rest(reference_text, filename)
    
    # pull out the Words list from the JSON so we can use Azure OpenAI to remove repeated words
    words_json = result['NBest'][0]['Words']
    
    # get the updated words JSON with repeated words removed using Azure OpenAI
    words_json =  sanitize_words(words_json, reference_text)

    # replace the Words node from the original result
    result['NBest'][0]['Words'] = words_json

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)