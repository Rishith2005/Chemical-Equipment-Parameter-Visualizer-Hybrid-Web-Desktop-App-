import os
import sys

from PyQt5.QtWidgets import QApplication

from .api import ApiClient, ApiConfig
from .main_window import MainWindow


def main() -> int:
    base_url = os.environ.get("CHEMVIZ_API_BASE_URL", "http://127.0.0.1:8000/api")
    api = ApiClient(ApiConfig(base_url=base_url))

    app = QApplication(sys.argv)
    win = MainWindow(api)
    win.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
