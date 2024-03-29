from typing import Any, Tuple
from .config import gpt3_max_tokens, gpt3_model, gpt3_key, gpt3_proxy
import httpx

def remove_punctuation(text):
    import string
    for i in range(len(text)):
        if text[i] not in string.punctuation:
            return text[i:]
    return ""

async def get_chat_response(preset: str, conversation: list, msg: str, max_token: int, temperature : float) -> Tuple[Any, bool]:
    if gpt3_proxy:
        proxies = {
            "http://": gpt3_proxy,
            "https://": gpt3_proxy,
        }
    else:
        proxies = {}
    system = [
        {"role": "system", "content": preset}
    ]
    prompt = {"role": "user", "content": msg}
    conversation.append(prompt)
    client = httpx.AsyncClient(proxies = gpt3_proxy, timeout=None)
    try:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {gpt3_key}"},
            json={
                "model": gpt3_model,
                "messages": system + conversation,
                "max_tokens": max_token,
                "temperature": temperature,
            },
        )
        response = response.json()
    except httpx.RequestError as e:
        return "网络炸了，我知道你很急，但你别急，等会再试", False
    except Exception as e:
        return f"发生未知错误: {e}", False
    try:
        res: str = remove_punctuation(response['choices'][0]['message']['content'].strip())
        conversation.append({"role": "assistant", "content": res})
        return response, True
    except Exception as e:
        return f"无效的返回消息: {response}", False