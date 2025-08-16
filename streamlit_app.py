import requests
import openai
import streamlit as st

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

# ===== GPT 設定（新版 API） =====
openai.api_key = st.secrets["OPENAI_API_KEY"]

def ask_gpt(question, context):
    prompt = f"以下是 Notion 資料：\n{context}\n\n請回答：{question}"
    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個幫助使用者的助理"},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"呼叫 GPT 時發生錯誤：{e}"

# ===== Streamlit 介面 =====
st.title("夥伴專屬 Notion AI 助理")
question = st.text_input("請輸入你的問題：")
if question:
    with st.spinner("AI 正在思考中..."):
        page_content = get_page_content()
        answer = ask_gpt(question, page_content)
        st.write("AI 回答：", answer)
