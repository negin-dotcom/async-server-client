import asyncio
import json 

HOST = "127.0.0.1"
PORT = 5022


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    try:
        request = {
            "action": "ping",
            "request_id": 1,
        }

        message = json.dumps(request).encode() + b"\n"
        writer.write(message)
        await writer.drain()

        response_line = await reader.readline()
        response = json.loads(response_line.decode("utf-8"))

        print("Server response:", response)

    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())