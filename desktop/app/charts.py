from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PieChartCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        if parent is not None:
            self.setParent(parent)

    def set_distribution(self, distribution: dict[str, int]) -> None:
        self.ax.clear()
        items = sorted(distribution.items(), key=lambda x: (-x[1], x[0]))
        labels = [k for k, _ in items]
        values = [v for _, v in items]
        if not values:
            self.ax.text(0.5, 0.5, "No data", ha="center", va="center")
        else:
            self.ax.pie(values, labels=labels, autopct="%1.0f%%", textprops={"fontsize": 8})
        self.fig.tight_layout()
        self.draw()


class BarChartCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        if parent is not None:
            self.setParent(parent)

    def set_distribution(self, distribution: dict[str, int]) -> None:
        self.ax.clear()
        items = sorted(distribution.items(), key=lambda x: (-x[1], x[0]))
        labels = [k for k, _ in items]
        values = [v for _, v in items]
        if not values:
            self.ax.text(0.5, 0.5, "No data", ha="center", va="center")
        else:
            x = list(range(len(labels)))
            self.ax.bar(x, values, color="#3B82F6")
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
            self.ax.set_ylabel("Count")
        self.fig.tight_layout()
        self.draw()


class LineChartCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        if parent is not None:
            self.setParent(parent)

    def set_metrics(self, labels: list[str], flowrate: list[float | None], pressure: list[float | None], temperature: list[float | None]) -> None:
        self.ax.clear()
        if not labels:
            self.ax.text(0.5, 0.5, "No data", ha="center", va="center")
            self.fig.tight_layout()
            self.draw()
            return

        x = list(range(len(labels)))
        any_vals = any(v is not None for v in flowrate + pressure + temperature)
        if not any_vals:
            self.ax.text(0.5, 0.5, "No numeric metrics found", ha="center", va="center")
            self.fig.tight_layout()
            self.draw()
            return

        self.ax.plot(x, flowrate, label="Flowrate", color="#3B82F6", marker="o", markersize=3)
        self.ax.plot(x, pressure, label="Pressure", color="#22C55E", marker="o", markersize=3)
        self.ax.plot(x, temperature, label="Temperature", color="#F59E0B", marker="o", markersize=3)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
        self.ax.legend(loc="best", fontsize=8)
        self.fig.tight_layout()
        self.draw()
