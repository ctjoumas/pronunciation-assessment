import json
import os

from pydantic import BaseModel
from openai import AzureOpenAI

azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment_name= os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key=azure_openai_api_key,  
    api_version=azure_openai_api_version,
    azure_endpoint=azure_endpoint
)

class Word(BaseModel):
    word: str
    error_type: str
    accuracy_score: float

class WordList(BaseModel):
    words: list[Word]


def sanitize_words(final_words = str, reference_text = str):
    final_words_example = [{'word': 'the', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'little', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'green', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'man', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'the', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'little', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'green', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'man', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'the', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'little', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'green', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'man', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'answered', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'of', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'course', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'its', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'me', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': "i've", 'error_type': 'Mispronunciation', 'accuracy_score': '90.0'}, {'word': 'come', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': "i've", 'error_type': 'Mispronunciation', 'accuracy_score': '90.0'}, {'word': 'come', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'to', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'see', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'if', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': "you're", 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'happy', 'error_type': 'None', 'accuracy_score': '90.0'}]
    words_example_result = [{'word': 'the', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'little', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'green', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'man', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'answered', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'of', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'course', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'its', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'me', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': "i've", 'error_type': 'Mispronunciation', 'accuracy_score': '90.0'}, {'word': 'come', 'error_type': 'Insertion', 'accuracy_score': '90.0'}, {'word': 'to', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'see', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'if', 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': "you're", 'error_type': 'None', 'accuracy_score': '90.0'}, {'word': 'happy', 'error_type': 'None', 'accuracy_score': '90.0'}]
    final_words_example_str = str(final_words_example)

    prompt = f"""
    You are a helpful assistant who will remove repeated words from a string of text. The words
    come from a student reading a passage which is converted to text, as described in Final Words.
    The Reference Text is the transcript of the actual passage, so this may differ from Final Words
    depending on how the student reads the passage.
    The final words are very important as they are used to assess the pronunciation of these words
    by the student.
    Each word will have an error type and you are only concerned with "Insertion" errors, which means
    the word was either repeated by the student or added by the student. We only want to remove
    repeated words as added words are valid and will still have pronunciation scores.

    You must compare Final Words to Reference text and determine which "Insertion" error words are
    repeated and remove these in your final cleaned-up version. These same words may appear later
    in Final words but may not be repeated words. As an example:

    Final Words: {final_words_example_str} 
    Reference Text: The little green man answered, Of course its me. I've come to see if you're happy. 
    Result: {words_example_result}

    If there are other insertion errors, you must use your judgement to determine if these are added or repeated words.
    
    Final Words: {final_words}
    
    Reference Text: {reference_text}
    
    Only return a list of the final words, using the Result example above as reference. Do not add any additional text or commentary or characters to the result.
    """

    #response = client.chat.completions.create(
    response = client.beta.chat.completions.parse(
        model=azure_openai_deployment_name,
        messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
        ],
        response_format=WordList
    )

    cleaned_text = response.choices[0].message.content.strip()

    cleaned_text_json = json.loads(cleaned_text)

    return cleaned_text_json

# Example usage
#final_words = "the little green man the little green man"
#reference_text = "the little green"

#cleaned_text = sanitize_words(final_words, reference_text)
#print(cleaned_text)