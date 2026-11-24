
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QDialogButtonBox,
    QLabel,
    QMessageBox
)


class TaskDialog(QDialog):
    """Діалогове вікно створення та редагування завдання."""

    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)

        self.setWindowTitle("Інформація про завдання")
        self.setMinimumWidth(420)

        # Поле назви
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Введіть назву завдання"
        )

        # Категорія
        self.category_input = QComboBox()
        self.category_input.addItems([
            "Навчання",
            "Робота",
            "Особисте",
            "Інше"
        ])

        # Пріоритет
        self.priority_input = QComboBox()
        self.priority_input.addItems([
            "Низький",
            "Середній",
            "Високий"
        ])

        # Опис
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Додатковий опис завдання..."
        )
        self.description_input.setMaximumHeight(110)

        # Компонування форми
        form_layout = QFormLayout()
        form_layout.addRow("Назва:", self.title_input)
        form_layout.addRow("Категорія:", self.category_input)
        form_layout.addRow("Пріоритет:", self.priority_input)
        form_layout.addRow("Опис:", self.description_input)

        # Кнопки
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Головне компонування
        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("Заповніть інформацію про завдання")
        )
        layout.addLayout(form_layout)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

        # Завантаження даних для редагування
        if task_data is not None:
            self.load_task_data(task_data)

    def load_task_data(self, task_data):
        """Заповнює поля даними вибраного завдання."""

        self.title_input.setText(
            str(task_data.get("title", ""))
        )

        category = str(
            task_data.get("category", "Навчання")
        )

        category_index = self.category_input.findText(category)

        if category_index >= 0:
            self.category_input.setCurrentIndex(category_index)

        priority = task_data.get("priority", 3)

        # Перетворення пріоритету на відповідний пункт списку
        if isinstance(priority, str):
            priority_map = {
                "Низький": 1,
                "Середній": 3,
                "Високий": 5
            }
            priority = priority_map.get(priority, 3)

        try:
            priority = int(priority)
        except (ValueError, TypeError):
            priority = 3

        if priority <= 2:
            self.priority_input.setCurrentIndex(0)
        elif priority == 3:
            self.priority_input.setCurrentIndex(1)
        else:
            self.priority_input.setCurrentIndex(2)

        self.description_input.setPlainText(
            str(task_data.get("description", ""))
        )

    def get_data(self):
        """Повертає введені дані."""

        priority_values = [1, 3, 5]

        return {
            "title": self.title_input.text().strip(),
            "category": self.category_input.currentText(),
            "priority": priority_values[
                self.priority_input.currentIndex()
            ],
            "description": self.description_input.toPlainText().strip()
        }

    def accept(self):
        """Перевіряє назву перед підтвердженням."""

        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                "Помилка",
                "Назва завдання не може бути порожньою."
            )
            return

        super().accept()
