import time
from linebot.v3.messaging import MessagingApi
from linebot.models import TextSendMessage
from apscheduler.schedulers.background import BackgroundScheduler
from Shinichi_Yamamoto_bot import chat

line_bot_api = MessagingApi('')
scheduler = BackgroundScheduler()

# 毎日特定の時間に実行されるジョブ
def send_message():
    answer, id = chat("大聖人の御書や、御聖訓、偉人の言葉を引用し、あなたの解釈とともに、悩んでいる人、苦しんでいる人へ励ましの言葉を書いて。絶対にすべて日本語で書くこと。", "crhnf549", "")
    everyday_words = "---今日の励ましの一言---\n" + answer + "\n\n※毎日自動配信しています。"
    print(everyday_words)
    #line_bot_api.broadcast(TextSendMessage(text=everyday_words))

def every_minites_task():
    current_time = time.time()
    local_time = time.ctime(current_time)
    print("現在時刻 ", local_time)

if __name__ == "__main__":
    # ジョブをスケジュールする
    scheduler.add_job(send_message, 'cron', minute='*')
    scheduler.add_job(every_minites_task, 'cron', minute='*')
    #scheduler.add_job(send_message, 'cron', hour=9)

    # スケジューラーを開始
    scheduler.start()
    while(True):
        pass
