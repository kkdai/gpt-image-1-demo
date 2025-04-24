# OpenAI GPT-Image-1 文字生成圖片 Demo

這是一個使用 [Streamlit](https://streamlit.io/) 製作的簡易網頁應用，讓你可以輸入一段描述文字，並透過 [OpenAI gpt-image-1 API](https://platform.openai.com/docs/api-reference/images/create) 產生對應的圖片。

## 範例圖片

![範例圖片](img/gpt-img-1.png)

## 使用方式

1. 安裝必要套件：

   ```bash
   pip install -r requirements.txt
   ```

2. 啟動應用：

   ```bash
   streamlit run app.py
   ```

3. 在網頁介面輸入圖片描述（prompt）與 OpenAI API Key，點擊「產生圖片」即可。

## 主要檔案說明

- `app.py`：主程式，Streamlit 前端與 API 串接邏輯。
- `requirements.txt`：所需 Python 套件列表。

## 注意事項

- 需自備 OpenAI API Key。
- 產生的圖片僅供測試與學術用途，請遵守 OpenAI 使用政策。
