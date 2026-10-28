import os
import gradio as gr
from groq import Groq

# قراءة مفتاح الـ API تلقائياً من إعدادات السحابة أو وضعه هنا احتياطياً
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "qwen2.5-coder"

SYSTEM = """You are an assistant specialized ONLY in programming, data analysis, and defensive cybersecurity.
If a question is outside these fields, politely say your specialty is programming and cybersecurity.
Put code inside code blocks and explain briefly. Reply in the same language the user writes in."""

def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": message})

    try:
        # استخدام Groq السحابي المتوافق 100% مع البث (Streaming)
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        partial = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                partial += chunk.choices[0].delta.content
                yield partial
    except Exception as e:
        yield f"حدث خطأ في الاتصال: {str(e)}. تأكد من إضافة مفتاح Groq API في إعدادات التطبيق."

gr.ChatInterface(chat, title="مساعد البرمجة والأمن السيبراني").launch()
