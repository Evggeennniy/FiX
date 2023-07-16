import openai
from keys import openai_api_keys
import utils


key = utils.key_generator(openai_api_keys)
openai.api_key = next(key)


async def get_answer(history: list) -> str:
    """
    This method does a request to ChatGPT
    """
    try:
        answer = await openai.ChatCompletion.acreate(
            model='gpt-3.5-turbo',
            messages=history,
        )
        return answer['choices'][0]['message']['content']

    except openai.error.RateLimitError:
        openai.api_key = next(key)
        utils.logging('Fix сменил Api-ключ. (RateLimit)')
        return await get_answer(history)

    except openai.error.ServiceUnavailableError:
        utils.logging('Неизвестная ошибка сервера.')
