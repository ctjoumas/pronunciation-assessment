import json
import time

from pronunciation_assessment_continuous import pronunciation_assessment_continuous_from_file
from pronunciation_assessment_rest import pronunciation_assessment_continuous_rest


def sdk_word_to_string(word, include_score):
    text = word.word
    if not include_score:
        return text
    accuracy_score = word.accuracy_score
    error_type = word.error_type
    if error_type == 'None':
        return text

    return f"{text}(a:{accuracy_score},e:{error_type[0:1]})"


def word_to_string(word, include_score):
    if 'word' in word:
        text = word['word']
    else:
        text = word['Word']

    if not include_score:
        return text

    if 'PronunciationAssessment' in word:
        accuracy_score = word['PronunciationAssessment']['AccuracyScore']
        error_type = word['PronunciationAssessment']['ErrorType']
    else:
        accuracy_score = word['AccuracyScore']
        error_type = word['ErrorType']

    if error_type == 'None':
        return text

    return f"{text}(a:{accuracy_score},e:{error_type[0:1]})"


# reference_text = "The little green man answered, Of course its me. I've come to see if you're happy. No, I'm not happy, Nancy said. And why not?"
# audio_file_nm = "sample_03.wav"

# reference_text = "If Nancy knew more about very small things, she wouldn't have been so afraid of climbing to high places to find water. Here's the rule. If tiny animals fall from high places, they don't get hurt. If we dropped an ant from a high airplane, the ant would not be hurt at all when it landed on the ground. A mouse wouldn't be hurt either. A squirrel wouldn't be badly hurt. A dog would probably be killed. And you can imagine what would happen to an elephant. Nancy was thirsty, so thirsty that she wanted to yell and scream and"
# audio_file_nm = "sample_02_26J6KN2pkzQijaKAYJWmzUy.wav"

reference_text = "If Nancy knew more about very small things, she wouldn't have been so afraid of climbing to high places to find water. Here's the rule. If tiny animals fall from high places,"
audio_file_nm = "nancy_mispronunciation_sample_04.wav"

result_rest = pronunciation_assessment_continuous_rest(reference_text, audio_file_nm)
result_sdk = pronunciation_assessment_continuous_from_file(file_name=audio_file_nm, reference_text=reference_text)


sdk_words_score = result_sdk['words']
rest_word_score = result_rest['NBest'][0]['Words']

result_sdk_text_score = " ".join(sdk_word_to_string(word, True) for word in sdk_words_score)
result_sdk_text_text = " ".join(sdk_word_to_string(word, False) for word in sdk_words_score)
result_rest_score = " ".join(word_to_string(word, True) for word in rest_word_score)
result_rest_text = " ".join(word_to_string(word, False) for word in rest_word_score)


print(f"############# REFERENCE TEXT File: {audio_file_nm}")
print(reference_text)
print("############# SDK TEXT")
# print(result_sdk_text_text)
print("############# REST TEXT")
print(result_rest_text)

print("############# SDK SCORE")
# print(result_sdk_text_score)

print("############# REST SCORE")
print(result_rest_score)
#
#
# print(json.dumps(result_rest))