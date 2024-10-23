import os
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

def sanitize_words(final_words = str, reference_text = str):
    prompt = f"""
    Compare the following text and remove any repeated words or phrases:
    
    Final Words: {final_words}
    
    Reference Text: {reference_text}
    
    Provide the final cleaned-up version without repetitions.
    """

    response = client.chat.completions.create(
    model=azure_openai_deployment_name,
    messages=[
             {"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": prompt}
        ]
    )

    cleaned_text = response.choices[0].message.content.strip()
    return cleaned_text

# Example usage
# final_words = "the little green man the little green man"
# reference_text = "the little green"

# cleaned_text = sanitize_words(final_words, reference_text)
# print(cleaned_text)