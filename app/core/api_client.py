import logging
logging.basicConfig(level=logging.INFO)

class OpenRouterClient:
    @staticmethod
    def generate_summary(text: str, summary_type: str) -> str:
        try:
            # ... существующий код ...
            response.raise_for_status()  # Проверка HTTP ошибок
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise