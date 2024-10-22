from flask import Flask, request, jsonify
import logging
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

    result = pronunciation_assessment_continuous_from_file(file_name=filename, reference_text=reference_text)

    # Uncomment this to test the REST implementation
    # pronunciation_assessment_continuous_rest(reference_text, filename)

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)