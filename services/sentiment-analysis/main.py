from fastapi import FastAPI
import openai
import tweepy
from pydantic import BaseModel

app = FastAPI()

# Configuración de la API de OpenAI
openai.api_key = "your_openai_api_key"

# Configuración de la API de Twitter
twitter_api = tweepy.Client(bearer_token="your_twitter_bearer_token")

# Modelo para analizar texto
class SentimentRequest(BaseModel):
    keywords: str
    limit: int = 10

@app.post("/analyze-sentiment")
async def analyze_sentiment(request: SentimentRequest):
    # Extraer tweets relacionados
    tweets = twitter_api.search_recent_tweets(
        query=request.keywords, max_results=request.limit
    )

    # Analizar sentimiento con OpenAI
    sentiments = []
    for tweet in tweets.data:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"¿Este texto es positivo, neutral o negativo? {tweet.text}",
            max_tokens=10
        )
        sentiments.append(response["choices"][0]["text"].strip())

    return {"keywords": request.keywords, "sentiments": sentiments}
