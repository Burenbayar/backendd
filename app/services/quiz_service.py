import json
from openai import OpenAI
from app.core.config import settings
from app.services.prompt_levels import build_level_hint

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def _extract_json_array(text: str):
    # codeblock тайрах
    t = text.strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        t = "\n".join(lines).strip()

    start = t.find("[")
    end = t.rfind("]")
    if start == -1 or end == -1:
        return None

    try:
        data = json.loads(t[start:end+1])
        return data if isinstance(data, list) else None
    except Exception:
        return None

async def generate_quiz_service(grade: int, subject: str):
    level_hint = build_level_hint(grade, subject)

    prompt = f"""
Намайг Монгол Улсын {grade}-р ангийн сурагч гэж төсөөл.
"{subject}" хичээлд зориулан 20 тестийн асуулт гарга.

=== ТҮВШНИЙ ЗААВАР ===
{level_hint}

=== ФОРМАТ ===
- Нийт 20 асуулт байна.
- Асуулт бүр 4 сонголттой байна.
- "answer" талбарт зөвхөн options доторх нэг сонголтын ТЕКСТ-ийг яг адилхан бич.

ЗӨВХӨН JSON массив буцаа:

[
  {{
    "question": "Асуултын текст",
    "options": ["сонголт1","сонголт2","сонголт3","сонголт4"],
    "answer": "сонголтN"
  }}
]

JSON-оос өөр ямар ч тайлбар, текст, markdown битгий.
"""

    # 1) Эхний оролдлого
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Та тест үүсгэдэг туслах. "
                    "Хэрэглэгчээс нэмэлт материал/текст нэхэхгүй. "
                    "Зөвхөн 20 асуулттай JSON массив буцаана. "
                    "Тайлбар текст БИЧИХГҮЙ."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    text = completion.choices[0].message.content or ""
    data = _extract_json_array(text)

    # 2) Хэрвээ JSON биш ирвэл “засварлагч” дуудлага
    if data is None:
        fix = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON array. No text. No markdown."},
                {"role": "user", "content": f"Convert to the required JSON array формат ONLY:\n\n{text}"},
            ],
            temperature=0,
        )
        text2 = fix.choices[0].message.content or ""
        data = _extract_json_array(text2)

    if data is None:
        # энд 500 биш 502 болгож ойлгомжтой алдаа өгье
        raise ValueError(f"JSON массив болгож чадсангүй. Model output: {text[:500]}")

    # optional: 20 биш бол тайрч/нэмэх (хамгаалалт)
    if len(data) > 20:
        data = data[:20]

    return data
