import requests
import json

api_key = 'DIFY_API_KEY'  # APIキーを設定してください
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

    response = requests.post('http://localhost/v1/chat-messages', headers=headers, json=data)

    # JSON文字列をPython辞書に変換
    res_text = json.loads(response.text)
    answer = res_text["answer"]
    # 'answer'キーの値を取得して表示
    print(answer)
    return answer