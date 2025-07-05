import openai
import dotenv
env = dotenv.dotenv_values('.env')

client = openai.OpenAI(
    api_key=env["YA_API_KEY"],
    base_url="https://llm.api.cloud.yandex.net/v1"
)

response = client.chat.completions.create(
    model="gpt://b1gm6saodhgvtq0l19o8/yandexgpt-lite",
    messages=[
        {"role": "system", "content": "Ты очень умный ассистент."},
        {"role": "user", "content": "Что умеют большие языковые модели?"}
    ],
    max_tokens=2000,
    temperature=0.3,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")