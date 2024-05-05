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

    response = requests.post('http://13.231.178.162/v1/chat-messages', headers=headers, json=data)
    #print(response.text)
    
    # JSON文字列をPython辞書に変換
    res_text = json.loads(response.text)
    conversation_id = res_text["conversation_id"]
    answer = res_text["answer"]
    #metadata = conversation_id = res_text["metadata"]
    #print(metadata)
    
    # 'answer'キーの値を取得して表示
    print(answer, conversation_id)
    return answer, conversation_id
