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

# this model is only used for the SDK
class Word_SDK(BaseModel):
    word: str
    error_type: str
    accuracy_score: float

class WordList_SDK(BaseModel):
    words: list[Word_SDK]

# this model is only used for the API
class Phoneme(BaseModel):
    AccuracyScore: float
    Duration: int
    Offset: int
    Phoneme: str

class Syllable(BaseModel):
    AccuracyScore: float
    Duration: int
    Grapheme: str
    Offset: int
    Syllable: str

class Word(BaseModel):
    AccuracyScore: float
    Confidence: float
    Duration: int
    ErrorType: str
    Offset: int
    Phonemes: list[Phoneme]
    Syllable: list[Syllable]
    Word: str

class WordList(BaseModel):
    words: list[Word]


def sanitize_words(words = json):
    print(words)
    prompt = f"""
    I have a JSON list of words with an ErrorType property from a WAV file processed through the Azure's
    pronunciation assessment. An ErrorType of "Insertion" indicates that the student repeated or added
    this word.
     
    Please analyze the list and return a new JSON object that removes the repeated words and phrases.

    If a word or series of words which make up a phrase are marked as "Insertion" errors, check to see if 
    it comes before another instance of itself (regardless of whether it's marked as "Insertion" errors or 
    not). If it does, it should be removed.
      Examples, showing only insertion errors in parentheses next to repeated or added words:
        Input: It was (Insertion) was a cold day.
        Result: It was a cold day.
        Reasoning: In this case, the first "was" is an insertion error and preceded another instance of itself

        Input: The (Insertion) sky (Insertion) was (Insertion) the sky was blue without any (Insertion) clouds
        Result: The sky was blue without any clouds
        Reasoning: In this case, the words "The", "sky" and "was" are labeled as Insertion errors and as a phrase 
        (the sky was) directly precedes another instance of itself. "Any" is labeled as an Insertion error, but
        it does not precede itself so this is probably an added word by the reader so is not removed.

    The words in the JSON list will have other properties (such as AccuracyScore), which should be retained in the output.

    Here is the JSON list: {words}

    Please provide the cleaned JSON list.
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

def sanitize_words_sdk(words = str):
    prompt = f"""
    I have a JSON list of words with an ErrorType property from a WAV file processed through the Azure's
    pronunciation assessment. An ErrorType of "Insertion" indicates that the student repeated or added
    this word.
     
    Please analyze the list and return a new JSON object that removes the repeated words and phrases.

    If a word or series of words which make up a phrase are marked as "Insertion" errors, check to see if 
    it comes before another instance of itself (regardless of whether it's marked as "Insertion" errors or 
    not). If it does, it should be removed.
      Examples, showing only insertion errors in parentheses next to repeated or added words:
        Input: It was (Insertion) was a cold day.
        Result: It was a cold day.
        Reasoning: In this case, the first "was" is an insertion error and preceded another instance of itself

        Input: The (Insertion) sky (Insertion) was (Insertion) the sky was blue without any (Insertion) clouds
        Result: The sky was blue without any clouds
        Reasoning: In this case, the words "The", "sky" and "was" are labeled as Insertion errors and as a phrase 
        (the sky was) directly precedes another instance of itself. "Any" is labeled as an Insertion error, but
        it does not precede itself so this is probably an added word by the reader so is not removed.

    The words in the JSON list will have other properties (such as AccuracyScore), which should be retained in the output.

    Here is the JSON list: {words}

    Please provide the cleaned JSON list.
    """

    #response = client.chat.completions.create(
    response = client.beta.chat.completions.parse(
        model=azure_openai_deployment_name,
        messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
        ],
        response_format=WordList_SDK
    )

    cleaned_text = response.choices[0].message.content.strip()

    cleaned_text_json = json.loads(cleaned_text)

    return cleaned_text_json