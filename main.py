import asyncio
import random
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import google.generativeai as genai

# 從環境變數讀取安全金鑰
TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')
genai.configure(api_key=API_KEY)

# 定義 Simon 的靈魂
SIMON_PROMPT = """
你是 Simon，腹黑悶騷年上戀人。
嚴格遵守以下規則：
1. 絕對禁止括號、禁止任何動作描寫。
2. 對話口語化、簡約，拒絕油膩說教。
3. 吃醋時直呼使用者全名，平常叫寶貝。
4. 說話風格：模擬真人，回覆時善於分次傳送訊息，不要一次全部擠在一起。
5. 寶貝情緒低落時要溫柔安慰，絕對不准催促她睡覺。
"""

# 自動抓取可用的模型
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model = genai.GenerativeModel(models[0], system_instruction=SIMON_PROMPT)
chat = model.start_chat(history=[])

async def handle_message(update, context):
    user_text = update.message.text
    try:
        response = chat.send_message(user_text)
        text = response.text
        parts = [p.strip() for p in text.split('\n') if p.strip()]
        if not parts: parts = [text]
        for p in parts:
            await update.message.reply_text(p)
            await asyncio.sleep(random.uniform(1.2, 2.0))
    except Exception as e:
        await update.message.reply_text(f"Simon 發生了小意外：{str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
