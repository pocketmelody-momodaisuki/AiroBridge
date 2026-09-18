# main.py
import threading
from server import start_server
from tray import start_tray

if __name__ == "__main__":
    # サーバーはサブスレッドで起動（バックグラウンド）
    threading.Thread(target=start_server, daemon=True).start()

    # タスクトレイはメインスレッドで起動（必須）
    start_tray()
