from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .api import ApiClient, build_basic_token
from .charts import BarChartCanvas, LineChartCanvas, PieChartCanvas


class MainWindow(QMainWindow):
    def __init__(self, api: ApiClient):
        super().__init__()
        self.api = api
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.resize(1200, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = self._build_login_page()
        self.app_page = self._build_app_page()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.app_page)
        self.stack.setCurrentWidget(self.login_page)

    def _build_login_page(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setAlignment(Qt.AlignCenter)

        card = QWidget()
        card.setMaximumWidth(420)
        card_layout = QVBoxLayout(card)

        title = QLabel("Sign in")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_error = QLabel("")
        self.login_error.setStyleSheet("color: #b91c1c;")
        self.login_error.setWordWrap(True)
        self.login_error.setVisible(False)

        btn = QPushButton("Sign in")
        btn.clicked.connect(self._handle_login)

        hint = QLabel("Default demo: demo / demo1234")
        hint.setStyleSheet("color: #64748b;")

        card_layout.addWidget(title)
        card_layout.addSpacing(12)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_error)
        card_layout.addSpacing(6)
        card_layout.addWidget(btn)
        card_layout.addSpacing(12)
        card_layout.addWidget(hint)

        layout.addWidget(card)
        return root

    def _build_app_page(self) -> QWidget:
        root = QWidget()
        outer = QVBoxLayout(root)

        top = QHBoxLayout()
        self.user_label = QLabel("")
        self.user_label.setStyleSheet("font-weight: 600;")
        top.addWidget(self.user_label)
        top.addStretch(1)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._refresh_list)

        self.signout_btn = QPushButton("Sign out")
        self.signout_btn.clicked.connect(self._sign_out)

        top.addWidget(self.refresh_btn)
        top.addWidget(self.signout_btn)
        outer.addLayout(top)

        body = QHBoxLayout()
        outer.addLayout(body, 1)

        left = QVBoxLayout()
        body.addLayout(left, 0)

        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self._upload_csv)
        left.addWidget(upload_btn)

        left.addWidget(QLabel("Recent datasets (last 5)"))
        self.dataset_list = QListWidget()
        self.dataset_list.currentItemChanged.connect(self._dataset_changed)
        left.addWidget(self.dataset_list, 1)

        right = QVBoxLayout()
        body.addLayout(right, 1)

        self.status_label = QLabel("Select a dataset")
        right.addWidget(self.status_label)

        self.summary_label = QLabel("")
        self.summary_label.setWordWrap(True)
        right.addWidget(self.summary_label)

        self.chart_tabs = QTabWidget()
        self.pie_chart = PieChartCanvas()
        self.bar_chart = BarChartCanvas()
        self.line_chart = LineChartCanvas()
        self.chart_tabs.addTab(self.pie_chart, "Pie")
        self.chart_tabs.addTab(self.bar_chart, "Bar")
        self.chart_tabs.addTab(self.line_chart, "Line")
        right.addWidget(self.chart_tabs, 0)

        self.table = QTableWidget(0, 0)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        right.addWidget(self.table, 1)

        buttons = QHBoxLayout()
        self.download_btn = QPushButton("Download PDF report")
        self.download_btn.clicked.connect(self._download_pdf)
        self.download_btn.setEnabled(False)
        buttons.addWidget(self.download_btn)
        buttons.addStretch(1)
        right.addLayout(buttons)

        return root

    def _handle_login(self) -> None:
        self.login_error.setVisible(False)
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self._set_login_error("Username and password are required")
            return

        token = build_basic_token(username, password)
        self.api.set_basic_token(token)
        try:
            me = self.api.get_me()
        except Exception as e:
            self.api.clear_auth()
            self._set_login_error(str(e))
            return

        self.user_label.setText(f"Signed in as {me.get('username', username)}")
        self.stack.setCurrentWidget(self.app_page)
        self._refresh_list()

    def _set_login_error(self, msg: str) -> None:
        self.login_error.setText(msg)
        self.login_error.setVisible(True)

    def _sign_out(self) -> None:
        self.api.clear_auth()
        self.username_input.setText("")
        self.password_input.setText("")
        self.dataset_list.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.pie_chart.set_distribution({})
        self.bar_chart.set_distribution({})
        self.line_chart.set_metrics([], [], [], [])
        self.status_label.setText("Select a dataset")
        self.summary_label.setText("")
        self.download_btn.setEnabled(False)
        self.stack.setCurrentWidget(self.login_page)

    def _refresh_list(self) -> None:
        try:
            res = self.api.list_datasets(5)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        items = res.get("items", [])
        self.dataset_list.blockSignals(True)
        self.dataset_list.clear()
        for d in items:
            text = f"{d.get('filename', '-') }  [{d.get('status', '-')}]"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, d.get("id"))
            self.dataset_list.addItem(item)
        self.dataset_list.blockSignals(False)

        if self.dataset_list.count() > 0:
            self.dataset_list.setCurrentRow(0)
        else:
            self._clear_dataset_view()

    def _clear_dataset_view(self) -> None:
        self.status_label.setText("No datasets yet")
        self.summary_label.setText("")
        self.pie_chart.set_distribution({})
        self.bar_chart.set_distribution({})
        self.line_chart.set_metrics([], [], [], [])
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.download_btn.setEnabled(False)

    def _dataset_changed(self, current: QListWidgetItem | None, previous: QListWidgetItem | None) -> None:
        if current is None:
            self._clear_dataset_view()
            return
        dataset_id = current.data(Qt.UserRole)
        if not dataset_id:
            self._clear_dataset_view()
            return

        self._load_dataset(str(dataset_id))

    def _load_dataset(self, dataset_id: str) -> None:
        self.download_btn.setEnabled(False)
        self.status_label.setText("Loading…")

        try:
            s = self.api.get_summary(dataset_id)
            p = self.api.get_preview(dataset_id, limit=50)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_label.setText("Failed")
            return

        dataset = s.get("dataset", {})
        summary = s.get("summary", {})
        dist = summary.get("type_distribution", {}) or {}

        self.status_label.setText(f"{dataset.get('filename', '-')}")
        avg = summary.get("averages", {}) or {}
        self.summary_label.setText(
            "\n".join(
                [
                    f"Total: {summary.get('total_count', '-')}",
                    f"Avg Flowrate: {avg.get('Flowrate', '-')}",
                    f"Avg Pressure: {avg.get('Pressure', '-')}",
                    f"Avg Temperature: {avg.get('Temperature', '-')}",
                ]
            )
        )

        preview = (p.get("preview", {}) or {})
        self.pie_chart.set_distribution({str(k): int(v) for k, v in dist.items()})
        self.bar_chart.set_distribution({str(k): int(v) for k, v in dist.items()})

        rows = preview.get("rows", []) if isinstance(preview, dict) else []
        labels, flow, pressure, temp = self._extract_metrics(rows)
        self.line_chart.set_metrics(labels, flow, pressure, temp)

        self._set_table(preview.get("columns", []), rows)
        self.download_btn.setEnabled(True)
        self.download_btn.setProperty("dataset_id", dataset_id)

    def _extract_metrics(self, rows) -> tuple[list[str], list[float | None], list[float | None], list[float | None]]:
        def to_number(v) -> float | None:
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                try:
                    return float(v)
                except ValueError:
                    return None
            return None

        labels: list[str] = []
        flow: list[float | None] = []
        pressure: list[float | None] = []
        temp: list[float | None] = []

        for idx, row in enumerate(rows if isinstance(rows, list) else []):
            record = row if isinstance(row, dict) else {}
            name = record.get("Equipment Name")
            label = str(name).strip() if isinstance(name, str) and str(name).strip() else f"Row {idx + 1}"
            labels.append(label)
            flow.append(to_number(record.get("Flowrate")))
            pressure.append(to_number(record.get("Pressure")))
            temp.append(to_number(record.get("Temperature")))

        return labels, flow, pressure, temp
    def _set_table(self, columns, rows) -> None:
        cols = [str(c) for c in columns]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(rows))

        for r_idx, row in enumerate(rows):
            record = row if isinstance(row, dict) else {}
            for c_idx, c in enumerate(cols):
                val = record.get(c, "") if isinstance(record, dict) else ""
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r_idx, c_idx, item)

        self.table.resizeColumnsToContents()
    def _upload_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.api.upload_dataset(path)
        except Exception as e:
            QMessageBox.critical(self, "Upload failed", str(e))
            return
        self._refresh_list()
    def _download_pdf(self) -> None:
        dataset_id = self.download_btn.property("dataset_id")
        if not dataset_id:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF Files (*.pdf)")
        if not path:
            return
        try:
            content = self.api.download_report(str(dataset_id))
        except Exception as e:
            QMessageBox.critical(self, "Download failed", str(e))
            return
        with open(path, "wb") as f:
            f.write(content)
        QMessageBox.information(self, "Saved", f"Saved to {path}")
