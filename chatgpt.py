import openai


async def get_answer(history: list) -> str:
    """
    This method does a request to ChatGPT
    """
    answer = await openai.ChatCompletion.acreate(
        model='gpt-3.5-turbo',
        messages=history,
    )
    return answer['choices'][0]['message']['content']
