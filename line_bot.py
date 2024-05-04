from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from Shinichi_Yamamoto_bot import chat

app = Flask(__name__)

line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')

@app.route("/", methods=['POST'])
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
    # ユーザーからのメッセージテキストを取得
    user_message = event.message.text
    print(user_message)
    # ここで何らかの処理を行う
    # ...

    response = chat(user_message)
    # LINEに応答メッセージを送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = response)
    )

if __name__ == "__main__":
    app.run()
