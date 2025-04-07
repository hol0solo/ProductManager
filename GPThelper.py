import asyncio
from openai import OpenAI
from CONFIG.config import GPT_API_KEY


client = OpenAI(api_key=GPT_API_KEY)


async def articles_translation(data: dict[int]) -> dict:
    """Асинхронная функция для перевода артиклей из немецкого в английский."""
    # Извлекаем артикли сразу в список
    articles_list = [data[dict_index]["article"] for dict_index in data]

    # Формируем запрос без лишних переносов строк для экономии
    text_input = f"Translate these German articles to English: {','.join(articles_list)}. Return only the translations in one string, separated by commas, no extra words."

    # Асинхронный вызов API
    response = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.responses.create(
            model="gpt-4o",
            tools=[{"type": "web_search_preview"}],
            input=text_input
        )
    )

    # Получаем переводы и разбиваем их
    articles_list_translated = response.output_text.split(",")

    # Обновляем исходный словарь напрямую
    for idx, translated_article in enumerate(articles_list_translated):
        data[idx]["article"] = translated_article.strip()

    return data