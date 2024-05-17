import os
from datetime import datetime, timedelta
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from apscheduler.schedulers.background import BackgroundScheduler
#from dify import chat
from gemini import chat

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
history = []
scheduler = BackgroundScheduler()
last_execution_date = datetime.now().date() + timedelta(days=1)

from queue import Queue
import time

# リクエストを保持するキューを作成
request_queue = Queue()

def process_request():
    # キューからリクエストを取得（キューが空の場合は待機）
    body, signature = request_queue.get()
    try:
        # リクエストを処理
        handler.handle(body, signature)
        print(f"Processed request. Remaining requests in queue: {request_queue.qsize()}")
    except InvalidSignatureError:
        print("Invalid signature")
    finally:
        # タスクが完了したことをキューに通知
        request_queue.task_done()

@app.route("/", methods=['POST', 'HEAD'])
def callback():
    global last_execution_date
    # 現在の日付を取得
    current_date = datetime.now().date()
    # HEADリクエストの場合は何もしない
    if request.method == 'HEAD':
        process_request()
        # 前回の実行日と現在の日付を比較
        if last_execution_date >= current_date:
            print("現在時刻", datetime.now())
            
        elif last_execution_date < current_date:
            # 日付が変わっていたら特定の処理を実行
            send_message()
            # 最後に実行日を更新
            last_execution_date = current_date
        
    else:
        # X-Line-Signatureヘッダーから署名を取得
        signature = request.headers['X-Line-Signature']
    
        # リクエストボディをテキストとして取得
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # リクエストをキューに追加
        request_queue.put((body, signature))

        '''
        # 署名を検証し、イベントを処理
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        '''
        
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global history

    # ユーザーからのメッセージテキストを取得
    user_message = event.message.text
    
    # ユーザーIDを取得してコンソールに出力
    user_id = event.source.user_id
    print(f"User {user_id}: {user_message}")

    #existing_data = next((item for item in history if item["user"] == user_id), {"user": "crhnf549", "id": "", "num": 0})
    
    #answer, conversation_id = chat(user_message, user_id, existing_data["id"])
    answer = chat(user_message)
    print(f"Bot: {answer}")
    #print(f"Bot: {answer}\n", f"Conversation ID: {conversation_id}")
    
    # LINEに応答メッセージを送信
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = answer)
        )
    except:
        line_bot_api.push_message(user_id, TextSendMessage(text = answer))
        print('Pushed message')
        
    '''
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
    '''
        

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
    #answer, id = chat("応援、激励、ためになる偉人の名言、思い出の一言をお願いします。", "crhnf549", "")
    answer = gemini("応援、激励、ためになる偉人の名言、思い出の一言をお願いします。")
    everyday_words = "---今日の励ましの一言---\n" + answer + "\n\n※毎日自動配信しています。"
    print(everyday_words)
    line_bot_api.broadcast(TextSendMessage(text=everyday_words))
    
if __name__ == "__main__":
    pass
    #app.run()
