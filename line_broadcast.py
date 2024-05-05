import time
import os
#from linebot.v3.messaging import MessagingApi
from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException
from linebot.models import TextSendMessage
from apscheduler.schedulers.background import BackgroundScheduler
from Shinichi_Yamamoto_bot import chat
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

USER_ID = "U812711723bfbfcd7047ba3d7bd89e717"
line_bot_api = MessagingApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
configuration = Configuration(access_token = os.getenv('CHANNEL_ACCESS_TOKEN'))
scheduler = BackgroundScheduler()

# 毎日特定の時間に実行されるジョブ
def send_message():
    answer, id = chat("大聖人の御書や、御聖訓、偉人の言葉を一つだけ引用し、あなたの解釈とともに、励ましの言葉を書いて。絶対にすべて日本語で書くこと。", "crhnf549", "")
    everyday_words = "---今日の励ましの一言---\n" + answer + "\n\n※毎日自動配信しています。"
    print(everyday_words)
    message_dict = {
        #'to': USER_ID,
        'messages': [
            {
                'type': 'text',
                'text': everyday_words
            },
        ]
    }
    #line_bot_api.broadcast(TextSendMessage(text=everyday_words))
    #line_bot_api.push_message("U812711723bfbfcd7047ba3d7bd89e717", TextSendMessage(text="テスト中"))
    '''
    with ApiClient(configuration) as api_client:
        # Create an instance of the API class
        line_bot_api = MessagingApi(api_client)
        push_message_request = PushMessageRequest.from_dict(message_dict)
        try:
            push_message_result = line_bot_api.push_message_with_http_info(push_message_request, _return_http_data_only=False)
            print(f'The response of MessagingApi->push_message status code => {push_message_result.status_code}')
        except ApiException as e:
            print('Exception when calling MessagingApi->push_message: %s\n' % e)
    '''
    with ApiClient(configuration) as api_client:
        # Create an instance of the API class
        line_bot_api = MessagingApi(api_client)
        broadcast_message_request = BroadcastMessageRequest.from_dict(message_dict)
        try:
            broadcast_message_result = line_bot_api.broadcast_message_with_http_info(broadcast_message_request, _return_http_data_only=False)
            print(f'The response of MessagingApi->broadcast_message status code => {broadcast_message_result.status_code}')
        except ApiException as e:
            print('Exception when calling MessagingApi->broadcast_message: %s\n' % e)


def every_minites_task():
    current_time = time.time()
    local_time = time.ctime(current_time)
    print("現在時刻 ", local_time)

if __name__ == "__main__":
    # ジョブをスケジュールする
    #scheduler.add_job(send_message, 'cron', minute='*')
    scheduler.add_job(every_minites_task, 'cron', minute='*')
    scheduler.add_job(send_message, 'cron', hour=0)

    # スケジューラーを開始
    scheduler.start()
    while(True):
        pass
