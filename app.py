import streamlit as st
import requests
import base64

st.title("OpenAI GPT-Image-1 文字生成圖片 Demo")

prompt = st.text_area("請輸入圖片描述（prompt）")
api_key = st.text_input("請輸入 OpenAI API Key", type="password")

if st.button("產生圖片") and prompt and api_key:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "model": "gpt-image-1",
        "output_format": "png",
        "size": "1024x1024",
    }
    with st.spinner("圖片生成中..."):
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
        )
    if response.status_code == 200:
        img_b64 = response.json()["data"][0]["b64_json"]
        img_bytes = base64.b64decode(img_b64)
        st.image(img_bytes, caption="產生的圖片", use_column_width=True)
    else:
        st.error(f"API 錯誤: {response.text}")
