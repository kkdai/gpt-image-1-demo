import streamlit as st
import requests
import base64
import os

st.title("OpenAI GPT-Image-1 文字生成圖片 Demo")

prompt = st.text_area("請輸入圖片描述（prompt）")
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    st.info("偵測到 OPENAI_API_KEY 環境變數，將自動使用。")
else:
    api_key = st.text_input("請輸入 OpenAI API Key", type="password")

uploaded_image = st.file_uploader(
    "（選填）上傳要編輯的圖片", type=["png", "jpg", "jpeg", "webp"]
)

if st.button("產生圖片") and prompt and api_key:
    if uploaded_image:
        # 呼叫 image edit API
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {
            "image": (uploaded_image.name, uploaded_image, uploaded_image.type),
        }
        data = {
            "prompt": prompt,
            "model": "gpt-image-1",
            "size": "1024x1024",
        }
        with st.spinner("圖片編輯中..."):
            response = requests.post(
                "https://api.openai.com/v1/images/edits",
                headers=headers,
                files=files,
                data=data,
            )
        if response.status_code == 200:
            img_b64 = response.json()["data"][0]["b64_json"]
            img_bytes = base64.b64decode(img_b64)
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_image, caption="原始圖片", use_container_width=True)
            with col2:
                st.image(img_bytes, caption="編輯後的圖片", use_container_width=True)
        else:
            st.error(f"API 錯誤: {response.text}")
    else:
        # 呼叫 image generation API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
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
            st.image(img_bytes, caption="產生的圖片", use_container_width=True)
        else:
            st.error(f"API 錯誤: {response.text}")
