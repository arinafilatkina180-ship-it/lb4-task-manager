
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)
from PyQt6.QtCore import pyqtSignal


class TaskInputWidget(QWidget):
    """Власний віджет для введення нового завдання."""

    taskAdded = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(
            "Введіть назву нового завдання..."
        )

        self.add_button = QPushButton("＋ Додати")
        self.add_button.setObjectName("addTaskButton")

        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_task)
        self.input_field.returnPressed.connect(self.add_task)

    def add_task(self):
        """Перевіряє назву та надсилає сигнал."""
        title = self.input_field.text().strip()

        if title:
            self.taskAdded.emit(title)
            self.input_field.clear()


class TaskStatsWidget(QWidget):
    """Власний віджет для відображення статистики."""

    statsChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.total_label = QLabel("Усього завдань: 0")
        self.completed_label = QLabel("Виконано: 0")

        self.total_label.setObjectName("statsLabel")
        self.completed_label.setObjectName("statsLabel")

        layout = QVBoxLayout()
        layout.addWidget(self.total_label)
        layout.addWidget(self.completed_label)

        self.setLayout(layout)

    def update_stats(self, total, completed):
        """Оновлює статистику та надсилає сигнал."""
        self.total_label.setText(
            f"Усього завдань: {total}"
        )
        self.completed_label.setText(
            f"Виконано: {completed}"
        )

        self.statsChanged.emit(total, completed)
