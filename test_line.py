import requests
import json

# 請填入你的 LINE 設定
LINE_ACCESS_TOKEN = '請填入你的_Access_Token'
LINE_USER_ID = '請填入你的_User_ID'

def test_line():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + LINE_ACCESS_TOKEN
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {"type": "text", "text": "🎉 測試成功！這是來自 GitHub 專案的測試訊息！"}
        ]
    }
    print("🚀 發送測試訊息...")
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            print("✅ 成功！")
        else:
            print(f"❌ 失敗: {r.text}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    test_line()