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
![接線圖示意](https://github.com/Eason09053360/AIOT-SecureSight/blob/main/%E6%8E%A5%E7%B7%9A%E5%9C%96.jpg)
### 接腳對照表

| 元件 | 樹莓派接腳 (BCM編碼) | 備註 |
| --- | --- | --- |
| LED 燈 (正極) | GPIO 17 | 需串聯電阻 |
| LED 燈 (負極) | GND | |
| 蜂鳴器 (正極) | GPIO 27 | 有源蜂鳴器 |
| 蜂鳴器 (負極) | GND | |
| 相機模組 | CSI 介面 | 使用專用排線15轉22pin |

## 🚀 安裝與執行說明

### 1. 安裝套件
請確認已安裝 Python 3，並執行以下指令安裝必要套件：
```bash
pip3 install -r requirements.txt
```
### 2. 設定參數
請下載 main.py，並填入您自己的 AWS 與 LINE 金鑰：
AWS_ACCESS_KEY = '你的 Access Key'
AWS_SECRET_KEY = '你的 Secret Key'
### ... 其他設定請參考程式碼註解

### 3. 執行程式
python3 main.py

📝 專題成員
陳永承
