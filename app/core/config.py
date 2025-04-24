class Config:
    OPENROUTER_API_KEY: str = ""  # Пользователь вводит свой ключ
    DEFAULT_MODEL: str = "openai/gpt-3.5-turbo"
    SUMMARY_TYPES: dict = {
        "short": "Сгенерируй краткий обзор (3-5 пунктов)",
        "detailed": "Создай подробный конспект с примерами",
        "full": "Сделай полный структурированный конспект"
    }