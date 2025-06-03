import streamlit as st
import requests
import base64
import os
import json


def main():
    st.title("OpenAI GPT-Image-1 文字生成圖片 Demo")

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        st.info("偵測到 OPENAI_API_KEY 環境變數，將自動使用。")
    else:
        api_key = st.text_input("請輸入 OpenAI API Key", type="password")

    uploaded_image = st.file_uploader(
        "（選填）上傳要編輯的圖片", type=["png", "jpg", "jpeg", "webp"]
    )

    HISTORY_FILE = "prompt_history.json"

    # 讀取歷史 prompt
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            prompt_history = json.load(f)
    else:
        prompt_history = []

    # 即時更新歷史紀錄：每次 prompt 輸入後自動加入
    # 讓 prompt 支援 session_state
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = ""

    # 先處理 sidebar 的歷史紀錄點擊事件
    with st.sidebar:
        st.header("Prompt 歷史紀錄")
        if prompt_history:
            for i, p in enumerate(reversed(prompt_history), 1):
                if st.button(f"{i}. {p}", key=f"history_{i}"):
                    st.session_state["prompt"] = p
                    st.rerun()
        else:
            st.write("尚無歷史紀錄")

    # 再產生 text_area，value 來自 session_state
    prompt = st.text_area(
        "請輸入圖片描述( Prompt )", value=st.session_state["prompt"], key="prompt"
    )

    if prompt and (not prompt_history or prompt != prompt_history[-1]):
        prompt_history.append(prompt)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(prompt_history, f, ensure_ascii=False, indent=2)

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
                "size": "1536x1024",
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
                    st.image(
                        uploaded_image, caption="原始圖片", use_container_width=True
                    )
                with col2:
                    st.image(
                        img_bytes, caption="編輯後的圖片", use_container_width=True
                    )
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
                "size": "1536x1024",
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


if __name__ == "__main__":
    main()
