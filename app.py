import ollama
import gradio as gr

MODEL = "qwen2.5-coder:3b"

SYSTEM = """You are an assistant specialized ONLY in programming, data analysis, and defensive cybersecurity.
If a question is outside these fields, politely say your specialty is programming and cybersecurity.
Put code inside code blocks and explain briefly. Reply in the same language the user writes in."""

def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": message})

    partial = ""
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True):
        partial += chunk["message"]["content"]
        yield partial

gr.ChatInterface(chat, title="مساعد البرمجة والأمن السيبراني").launch()
