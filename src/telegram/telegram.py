from telethon import TelegramClient, events
import os

# 使用你自己的 API ID 和 API Hash
api_id = '你的 API ID'
api_hash = '你的 API Hash'

# 這裡用你的手機號碼進行驗證
client = TelegramClient('session_name', api_id, api_hash)

# 檔案儲存路徑
DOWNLOAD_FOLDER = 'downloads'

# 創建下載資料夾（如果不存在）
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@client.on(events.NewMessage)
async def handler(event):
    # 只處理來自指定聊天的消息
    if event.chat_id == int('指定的使用者或群組 ID'):
        # 檢查消息是否包含 .zip 或 .rar 檔案
        if event.file and (event.file.name.endswith('.zip') or event.file.name.endswith('.rar')):
            file_path = os.path.join(DOWNLOAD_FOLDER, event.file.name)
            await event.download_media(file_path)
            print(f"檔案 {event.file.name} 已下載到 {file_path}。")

async def main():
    await client.start()
    print("Client is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

# undone
