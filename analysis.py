import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MAISA_API_KEY = os.getenv("MAISA_API_KEY")


def summary_api(hint, text):
    url = "https://api.maisa.ai/v1/capabilities/summarize"
    payload = {
        "format": "bullet",
        "length": "medium",
        "summary_hint": hint,
        "text": text,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": MAISA_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        topics = response.json()["summary"].split("\n")
        return topics
    else:
        return []


def embedding_api(texts):
    url = "https://api.maisa.ai/v1/models/embeddings"
    # Check if texts is a single string or a list, and adjust accordingly
    payload_texts = texts if isinstance(texts, list) else [texts]
    payload = {"texts": payload_texts}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": MAISA_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    # print(f"embeddings response text: {response.text}")
    # print(f"embeddings status code: {response.status_code}")
    if response.status_code == 202:
        embeddings = response.json()["embeddings"]
        # Return a list of embeddings if multiple texts were provided, or a single embedding if one text was provided
        # print(f"received embeddings: {embeddings}")
        return embeddings if isinstance(texts, list) else embeddings[0]
    else:
        return [] if isinstance(texts, list) else []


def analyze_results(results):
    insights = []
    i = 0
    for key, value in results.items():
        api_text = ""
        for respondent, response in value.items():
            i += 1
            api_text += f"Response {i}: {response} \n"

        insights.append(
            {
                f"question_{i}": {
                    "topics": summary_api(
                        f"The top 5 topics mentioned by the users:", api_text
                    ),
                    "good": summary_api(
                        "The top 5 positive comments mentioned by the users:", api_text
                    ),
                    "bad": summary_api(
                        "The top 5 negative comments mentioned by the users:", api_text
                    ),
                    "embeddings": embedding_api(api_text),
                }
            }
        )

    return insights


def compute_word_relevance(words, questions_embeddings):
    # Fetch embeddings for all words in one request for efficiency
    word_embeddings = embedding_api(words)
    relevance = []
    for word, embedding in zip(words, word_embeddings):
        word_em = np.array(embedding).flatten()
        sum_relevance = 0
        for question_embedding in questions_embeddings:
            question_em = np.array(question_embedding).flatten()
            sum_relevance += np.dot(question_em, word_em) / (
                np.linalg.norm(question_em) * np.linalg.norm(word_em)
            )
        relevance.append(sum_relevance)
    return relevance, words


def top_words(text, n):    
    topics = summary_api(f"The top {n} words mentioned by the users. Only one word per bullet point, dont give multiple words in a line. Only {n} words in total:  ", text)
    return topics
