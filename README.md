# ⚡ 基於 AWS Rekognition 的 AIoT 智慧居家監控系統

這是一個整合 Raspberry Pi、AWS 雲端 AI 服務與 LINE 通訊軟體的物聯網專題。系統能夠即時捕捉畫面，上傳至雲端進行物件辨識（如偵測特定公仔或入侵者），並在偵測到目標時觸發警報、傳送 LINE 通知，並將數據寫入 DynamoDB。

## 📋 功能特色
- **即時影像捕捉**：使用 Raspberry Pi Camera 進行拍攝。
- **雲端 AI 辨識**：整合 AWS Rekognition Custom Labels，辨識特定物件 (如 Pikachu, Squirtle)。
- **即時通訊警報**：透過 LINE Messaging API 發送圖文警告。
- **硬體警報回饋**：控制 LED 閃爍與蜂鳴器鳴叫。
- **雲端數據紀錄**：自動將偵測結果寫入 AWS DynamoDB。

## 🛠️ 硬體需求
- Raspberry Pi 4 或 5
- Camera Module
- LED 燈 x 1
- 蜂鳴器 x 1

## 🚀 安裝與執行說明

### 1. 安裝套件
請確認已安裝 Python 3，並執行以下指令安裝必要套件：
```bash
pip3 install -r requirements.txt
