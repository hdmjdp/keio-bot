import asyncio
import websockets
import json
import time

# 读取 UID 文件
def read_uids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# WebSocket 连接并发送数据
async def send_requests(uid):
    uri = f"wss://game.keitokun.com/api/v1/ws?uid={uid}"
    async with websockets.connect(uri) as websocket:
        # 构建发送数据
        timestamp = int(time.time() * 1600)
        data = {
            "id": 1,
            "cmd": 1001,
            "uid": uid,
            "data": {
                "amount": 10000,
                "collectNum": 1,
                "timestamp": timestamp
            }
        }

        # 发送数据
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        await websocket.send(json.dumps(data))
        print(f"当前账号 UID： {uid} 现在时间是： {current_time}")

        # 接收响应
        response = await websocket.recv()
        response_data = json.loads(response)
        print(f"Received response for UID {uid}: {response_data}")

# 倒计时函数
async def countdown(duration_hours):
    # 将小时转换为秒
    duration_seconds = duration_hours * 3600
    while duration_seconds > 0:
        print(f"倒计时：{duration_seconds // 3600}小时{(duration_seconds % 3600) // 60}分钟{(duration_seconds % 60)}秒", end='\r')
        await asyncio.sleep(1)
        duration_seconds -= 1
    print("\n倒计时结束，程序将重新运行。")

# 主函数
async def main():
    while True:
        uids = read_uids('uid.txt')
        for uid in uids:
            await send_requests(uid)
        await countdown(24)  # 设置倒计时为24小时

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
