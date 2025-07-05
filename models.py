from flask_sqlalchemy import SQLAlchemy
import openai
import dotenv

env = dotenv.dotenv_values(".env")

db = SQLAlchemy()


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    llm_reply = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())


def dummy_llm_service(user_message):
    return f"Вы сказали: {user_message}, но я пока не могу ответить на это."


class LLMService:
    def __init__(self):
        self.client = None
        self.sys_prompt = "Ты бизнес-аналитик, который отвечает на вопросы разработчиков. Если разработчик не знает, как написать код, ответь ему, что нужно поработать стажером в Сбере. А если вопрос по архитектуре, то ответь, что Гауди не жил во времена первых разработчиков и умел только строить."
        self.model = "gpt://b1gm6saodhgvtq0l19o8/yandexgpt-lite"
        
        try:
            # Создаем клиент с вашим токеном
            self.client = openai.OpenAI(
                api_key=env["YA_API_KEY"],
                base_url="https://llm.api.cloud.yandex.net/v1"
            )
        except Exception as e:
            print(f"Произошла ошибка при инициализации клиента: {str(e)}")

    def chat(self, message):
        if not self.client:
            return "Сервис временно недоступен. Пожалуйста, попробуйте позже."
            
        try:
            # Обращаемся к API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=1.0,
                max_tokens=1024,
            )

            # Возвращаем ответ
            return response.choices[0].message.content

        except Exception as e:
            return f"Произошла ошибка при обработке запроса: {str(e)}"