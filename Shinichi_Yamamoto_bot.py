import requests
import json
import os

api_key = os.getenv('DIFY_API_KEY') 
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

def chat(query, user_id, conversation_id):
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": user_id,
        "files": [
            {
                "type": "",
                "transfer_method": "",
                "url": ""
            }
        ]
    }

    response = requests.post('https://api.dify.ai/v1/chat-messages', headers=headers, json=data, timeout=10)

    try:
        # 成功したレスポンスのステータスコードは200から299の間です
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # HTTPエラーが発生した場合、ここで処理します
        print(f'HTTP error occurred: {http_err}')  # Python 3.6以上が必要
        answer = "チャットボットに接続できませんでした。申し訳ありませんが対応をお待ちください。"
    except Exception as err:
        # その他のエラーが発生した場合、ここで処理します
        print(f'Other error occurred: {err}')
        answer = "サーバーエラーが発生しました。申し訳ありませんが対応をお待ちください。"
    else:
        # レスポンスが成功した場合の処理をここに書きます
      
        # JSON文字列をPython辞書に変換
        res_text = json.loads(response.text)
        conversation_id = res_text["conversation_id"]
        answer = res_text["answer"]
    return answer, conversation_id
