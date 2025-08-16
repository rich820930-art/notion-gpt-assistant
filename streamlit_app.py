import requests
import streamlit as st
from gpt4all import GPT4All

# ===== Notion 設定 =====
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
PAGE_ID = st.secrets["PAGE_ID"]
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

def get_page_content():
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    res = requests.get(url, headers=headers)
    data = res.json()
    text_content = []
    for block in data.get("results", []):
        if block["type"] == "paragraph":
            texts = block["paragraph"]["text"]
            for t in texts:
                text_content.append(t["plain_text"])
    return "\n".join(text_content)

# ===== GPT4All 設定 =====
# 下載模型後放在本地，例如：gpt4all-lora-quantized.bin
model_path = "gpt4all-lora-quantized.bin"
gpt_model = GPT4All(model_path)

def ask_gpt(question, context):
    prompt = f"以下是 Notion 資料：\n{context}\n\n請回答：{question}"
    try:
        response = gpt_model.generate(prompt)
        return response
    except Exception as e:
        return f"GPT4All 發生錯誤：{e}"

# ===== Streamlit 介面 =====
st.title("夥伴專屬 Notion AI 助理（免費版）")
question = st.text_input("請輸入你的問題：")
if question:
    with st.spinner("AI 正在思考中..."):
        page_content = get_page_content()
        answer = ask_gpt(question, page_content)
        st.write("AI 回答：", answer)
