from openai import OpenAI
import os
import re

client = OpenAI(
    api_key=os.getenv("SEALION_API_KEY"),
    base_url="https://api.sea-lion.ai/v1"
)

def gloss_to_subtitle(glosses, language="english"):
    system_prompt = (
        f"You are a sign language subtitle generator. "
        f"ONLY output the subtitle in {language}, no explanations, no reasoning. "
        f"Example: ['Want'] → 'ចង់' (Khmer). ['Thank_You'] → 'Cảm ơn' (Vietnamese). "
        f"Output should be short, natural subtitles only."
    )

    user_prompt = " ".join(glosses)

    response = client.chat.completions.create(
        model="aisingapore/Llama-SEA-LION-v3.5-70B-R",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=50
    )

    # Raw output
    raw_output = response.choices[0].message.content.strip()

    # Clean it: remove quotes, take first line only, cut off explanations
    cleaned = raw_output.split("\n")[0].strip().strip('"').strip("'")

    # Extra: if model still outputs "Okay, ..." → remove everything before Khmer/Viet script
    cleaned = re.sub(r"^Okay.*?:", "", cleaned).strip()

    return cleaned
