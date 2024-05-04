import requests
import json
import os

api_key = os.getenv('DIFY_API_KEY') 
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

def chat(query):
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "crhnf549",
        "files": [
            {
                "type": "",
                "transfer_method": "",
                "url": ""
            }
        ]
    }

    response = requests.post('http://52.195.234.150/v1/chat-messages', headers=headers, json=data)
    print(response)
    # JSON文字列をPython辞書に変換
    res_text = json.loads(response.text)
    answer = res_text["answer"]
    # 'answer'キーの値を取得して表示
    print(answer)
    return answer
