import os
import time
from openai import OpenAI
from services.prompt_builder import SYSTEM_PROMPT, build_llm_prompt


class VAPILLM:
    def __init__(self):
        api_key = os.environ.get("VAPI_API_KEY")
        base_url = os.environ.get("VAPI_BASE_URL")
        model = os.environ.get("VAPI_MODEL", "gpt-5.6-sol")

        if not api_key:
            raise ValueError("未找到 VAPI_API_KEY，请检查 .env 或环境变量。")

        if not base_url:
            raise ValueError("未找到 VAPI_BASE_URL，请检查 .env 或环境变量。")

        self.model = model
        self.base_url = base_url

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=2,
        )

    def generate(self, prompt: str, system_prompt: str) -> str:
        last_error = None

        for attempt in range(4):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=1200,
                    stream=False,
                )

                return response.choices[0].message.content

            except Exception as e:
                last_error = e
                time.sleep(2 + attempt * 2)

        raise RuntimeError(f"V-API 调用失败：{last_error}")


def generate_clean_recommendation(
    city: str,
    weather: str,
    start_location: str,
    place_type: str,
    search_results: list,
) -> str:
    llm = VAPILLM()

    prompt = build_llm_prompt(
        city=city,
        weather=weather,
        start_location=start_location,
        place_type=place_type,
        search_results=search_results,
    )

    return llm.generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )