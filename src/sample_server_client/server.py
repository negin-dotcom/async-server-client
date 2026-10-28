import asyncio
import json 

HOST = "127.0.0.1"
PORT = 5022


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
):
    address = writer.get_extra_info("peername")
    print(f"Client connected: {address}")

    try:
        while True:
            line = await reader.readline()

            if not line:
                break 

            try:
                request = json.loads(line.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                response = {
                    "status": "error",
                    "message": "Invalid json",
                }
            else:
                action = request.get("action")
                if action == "ping":
                    response = {
                        "status": "ok",
                        "request_id": request.get("request_id"),
                        "message": "pong",
                    }
                else:
                    response = {
                        "status": "error",
                        "request_id": request.get("request_id"),
                        "message": f"Unknown action: {action}",
                    }

            message = json.dumps(response).encode("utf-8") + b"\n"
            writer.write(message)
            await writer.drain()

    except (ConnectionError, asyncio.CancelledError):
        raise 
    finally:
        print(f"Client disconnected: {address}")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        HOST,
        PORT
    )

    addresses = ", ".join(
        str(sock.getsockname()) for sock in server.sockets
    )

    print(f"Server listening on {addresses}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")