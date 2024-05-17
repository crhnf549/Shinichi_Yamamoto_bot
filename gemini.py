import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY') 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}
file_num = 4

def chat(query):
    prompt = (
        "あなたは山本伸一です。与えられた小説「新・人間革命」の内容をもとに、"
        "山本伸一の言葉を使って山本伸一らしく、「質問」に回答してください。"
        "必ず日本語を使用し、改行しないで答えること。相手に小説のデータを持っていることを知られてはいけません。"
        "また、小説の内容に含まれないことを聞かれた場合は、回答が難しいことを伝えたうえで、想定できることを回答すること。"
    )
    responses = ""
    
    for i in range(file_num):
        with open(f"./新・人間革命_{i + 1}.txt", 'r', encoding="UTF-8") as file:
            content = file.read()
            #print(content)
        try:    
            response = model.generate_content(
                prompt + f"\n\n質問:{query}\n\n" + f"小説「新・人間革命」:{content}",
                request_options={"timeout": 600},
                safety_settings=safety_settings,
            )
            responses = responses + "\n" + response.text
            print(f"Finished process: 新・人間革命_{i + 1}.txt")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print(f"Response:{responses}") 
    
    prompt = (
        "あなたは山本伸一です。与えられた「山本伸一のセリフ」をもとに、山本伸一になりきって1000文字以内で「質問」に回答してください。"
        "必ず日本語を使用すること。また、山本伸一になりきっていることを相手に知らせてはいけません。相手の気持ちに寄り添い、心からの励ましの言葉を忘れずに。"
    )
    try:
        response = model.generate_content(
            prompt + f"\n\n質問:{query}\n\n" + f"山本伸一のセリフ:{responses}",
            request_options={"timeout": 600},
            safety_settings=safety_settings,
        )
        answer = response.text
    except Exception as e:
        answer = "サーバーエラーが発生しました。数分置いて再度お試しください。"
        print(f"An error occurred: {e}")
    return answer
