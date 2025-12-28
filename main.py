import time
import datetime
import sqlite3
import boto3
import os
import requests
import json
from picamera2 import Picamera2
from gpiozero import LED, Buzzer

# ==========================================
# 🔧 系統配置 (Configuration)
# ==========================================
# 1. AWS 設定
# 注意：請勿將真實金鑰上傳至 GitHub，請在本地執行時填入
MODEL_ARN = '請填入你的_Model_ARN' 
AWS_ACCESS_KEY = '請填入你的_Access_Key'
AWS_SECRET_KEY = '請填入你的_Secret_Key'
AWS_SESSION_TOKEN = '請填入你的_Session_Token' # 如果是學生帳號才需要
REGION = 'us-east-1'

BUCKET_NAME = '請填入你的_S3_Bucket_Name'
IMAGE_NAME = 'captured_pokemon.jpg'
DB_NAME = 'pokemon_events.db' 
DYNAMO_TABLE = 'PokemonEvents' 

# 2. LINE Messaging API 設定
LINE_ACCESS_TOKEN = '請填入你的_LINE_Access_Token'
LINE_USER_ID = '請填入你的_User_ID'

# 3. GPIO 硬體腳位設定
LED_PIN = 17
BUZZER_PIN = 27

# 初始化 GPIO
led = LED(LED_PIN)       
buzzer = Buzzer(BUZZER_PIN) 

# ==========================================
# 🛠️ 核心功能函式
# ==========================================

def init_db():
    """初始化本地 SQLite 資料庫"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS events (timestamp TEXT, label TEXT, confidence REAL)')
    conn.commit()
    conn.close()

def log_to_local(label, confidence):
    """寫入本地 SQLite"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO events VALUES (?, ?, ?)", (t, label, confidence))
    conn.commit()
    conn.close()
    print(f"💾 [本地] 已紀錄: {label}")

def log_to_aws_dynamo(table_resource, label, confidence):
    """寫入 AWS DynamoDB 雲端資料庫"""
    try:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table_resource.put_item(
            Item={
                'timestamp': t,
                'label': label,
                'confidence': str(confidence)
            }
        )
        print(f"🚀 [雲端] DynamoDB 上傳成功！")
    except Exception as e:
        print(f"❌ DynamoDB 上傳失敗: {e}")

def trigger_alert():
    """觸發硬體警報 (LED + 蜂鳴器)"""
    print("🚨 觸發警報裝置！")
    led.on()
    buzzer.on()
    time.sleep(0.5) 
    buzzer.off()
    time.sleep(0.5) 
    led.off()

def send_line_msg(msg):
    """發送 LINE 通知"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + LINE_ACCESS_TOKEN
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": msg}]
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            print(f"📱 LINE 通知已發送")
        else:
            print(f"❌ LINE 發送失敗: {r.status_code}")
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

# ==========================================
# 🚀 主程式邏輯
# ==========================================
def main():
    init_db()
    
    print("⚡ 系統啟動中... 連接 AWS 服務...")
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            aws_session_token=AWS_SESSION_TOKEN, 
            region_name=REGION
        )
        s3 = session.client('s3')
        rekognition = session.client('rekognition')
        dynamodb = session.resource('dynamodb')
        db_table = dynamodb.Table(DYNAMO_TABLE)
        print("✅ AWS 連線成功")
    except Exception as e:
        print(f"❌ AWS 連線失敗 (請檢查 Key 是否過期): {e}")
        return

    # 啟動相機
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (1024, 768)})
        picam2.configure(config)
        picam2.start()
        print("📷 相機就緒")
    except Exception as e:
        print(f"❌ 相機啟動失敗: {e}")
        return

    # 主迴圈
    while True:
        try:
            input("\n👉 按 Enter 鍵進行拍照偵測 (按 Ctrl+C 結束)...")
            
            # 1. 拍照與上傳
            print("📸 拍照與上傳...")
            picam2.capture_file(IMAGE_NAME)
            s3.upload_file(IMAGE_NAME, BUCKET_NAME, IMAGE_NAME)

            # 2. 影像辨識
            print("🧠 AI 分析中...")
            response = rekognition.detect_custom_labels(
                ProjectVersionArn=MODEL_ARN,
                Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': IMAGE_NAME}},
                MinConfidence=70 
            )

            # 3. 處理結果
            labels = response['CustomLabels']
            found_target = False
            
            if not labels:
                 print("👀 畫面中沒有發現目標。")

            for label in labels:
                name = label['Name']
                conf = label['Confidence']
                print(f"✨ 發現: {name} (信心度: {conf:.2f}%)")
                
                # 紀錄資料
                log_to_local(name, conf)
                log_to_aws_dynamo(db_table, name, conf)
                
                # 判斷特定目標 (例如 Pikachu 或 Squirtle)
                if "Pikachu" in name or "pikachu" in name or "Squirtle" in name: 
                    trigger_alert()
                    
                    print("準備發送 LINE...")
                    msg = f"⚠️ 警告！發現入侵者！\n偵測目標: {name}\n信心度: {conf:.2f}%"
                    send_line_msg(msg)
                    
                    found_target = True

        except KeyboardInterrupt:
            print("\n👋 程式結束")
            picam2.stop()
            picam2.close()
            break
        except Exception as e:
            print(f"❌ 執行錯誤: {e}")

if __name__ == "__main__":
    main()