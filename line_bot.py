import os
import time
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
#from linebot.v3.messaging import MessagingApi
#from linebot.v3.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from apscheduler.schedulers.background import BackgroundScheduler
from Shinichi_Yamamoto_bot import chat

app = Flask(__name__)

#line_bot_api = MessagingApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
history = []
scheduler = BackgroundScheduler()

@app.route("/")
def callback():
    # X-Line-Signatureヘッダーから署名を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディをテキストとして取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、イベントを処理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global history

    # ユーザーからのメッセージテキストを取得
    user_message = event.message.text
    
    # ユーザーIDを取得してコンソールに出力
    user_id = event.source.user_id
    print(f"User {user_id}:", user_message)

    existing_data = next((item for item in history if item["user"] == user_id), {"user": "crhnf549", "id": "", "num": 0})
    
    answer, conversation_id = chat(user_message, user_id, existing_data["id"])
    print(f"Bot:{answer}\n", f"Conversation ID:{conversation_id}")
    
    history, new_conversation = update_history(history, user_id, conversation_id)
    
    if new_conversation:
        # LINEに応答メッセージを送信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = answer + "\n\nそろそろ新しい話題について話しましょう！")
        )
    else:
        # LINEに応答メッセージを送信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = answer)
        )
        

def update_history(history, user_id, conversation_id):
    new_conversation = False
    
    # 既存のデータを検索
    existing_data = next((item for item in history if item["user"] == user_id), None)
    
    # 既存のデータがある場合は更新
    if existing_data:
        for entry in history:
            if entry["user"] == user_id:
                entry["num"] += 1
                
                if entry["num"] > 30:
                    print("new conversation")
                    entry["num"] = 1
                    entry["id"] = ""
                    new_conversation = True
                else:
                    entry["id"] = conversation_id
                break
    # 既存のデータがない場合は新規追加
    else:
        history.append({"user": user_id, "id": conversation_id, "num": 1})
        
    return history, new_conversation
    
# 毎日特定の時間に実行されるジョブ
def send_message():
    answer, id = chat("応援、励まし、激励、名言、思い出の一言をお願いします。", "crhnf549", "")
    everyday_words = "---今日の励ましの一言---\n" + answer + "\n\n※毎日自動配信しています。"
    print(everyday_words)
    line_bot_api.broadcast(TextSendMessage(text=everyday_words))
    
def every_minites_task():
    current_time = time.time()
    local_time = time.ctime(current_time)
    print("現在時刻 ", local_time)
    
if __name__ == "__main__":
    # ジョブをスケジュールする
    #scheduler.add_job(send_message, 'cron', minute='*')
    scheduler.add_job(every_minites_task, 'cron', minute='*')
    scheduler.add_job(send_message, 'cron', hour=9)

    # スケジューラーを開始
    scheduler.start()
    
    #app.run()
