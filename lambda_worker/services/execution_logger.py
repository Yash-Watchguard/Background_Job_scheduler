from datetime import datetime
import io


class ExecutionLogger:
    def __init__(self):
        self._buffer = io.StringIO()

    def log(self, message: str):
        timestamp = datetime.now().isoformat()
        self._buffer.write(f"[{timestamp}] {message}\n")

    def get_logs(self) -> str:
        return self._buffer.getvalue()