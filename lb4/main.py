
import sys
import json

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QRadioButton,
    QGroupBox,
    QProgressBar,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QDialog
)

from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt

from widgets import TaskInputWidget, TaskStatsWidget
from dialogs import TaskDialog


class MainWindow(QMainWindow):
    """Головне вікно менеджера завдань."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Менеджер завдань")
        self.setMinimumSize(750, 550)

        self.tasks = []

        self.create_widgets()
        self.create_layout()
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.connect_signals()
        self.apply_styles()

        self.update_statistics()

    # -------------------------------------------------
    # Створення віджетів
    # -------------------------------------------------

    def create_widgets(self):
        self.task_input = TaskInputWidget()

        self.task_list = QListWidget()
        self.task_list.setAlternatingRowColors(True)

        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Навчання",
            "Робота",
            "Особисте",
            "Інше"
        ])

        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(1, 5)
        self.priority_spin.setValue(3)

        self.urgent_checkbox = QCheckBox(
            "Термінове завдання"
        )

        self.study_radio = QRadioButton("Навчання")
        self.personal_radio = QRadioButton("Особисте")
        self.study_radio.setChecked(True)

        self.add_button = QPushButton("Додати завдання")
        self.complete_button = QPushButton(
            "Позначити виконаним"
        )
        self.edit_button = QPushButton("Редагувати")
        self.delete_button = QPushButton("Видалити")
        self.clear_button = QPushButton("Очистити форму")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.stats_widget = TaskStatsWidget()

        self.signal_status = QLabel(
            "Сигнали статистики активні"
        )
        self.signal_status.setObjectName("signalStatus")

    # -------------------------------------------------
    # Компонування інтерфейсу
    # -------------------------------------------------

    def create_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        title_label = QLabel("Менеджер завдань")
        title_label.setObjectName("mainTitle")

        subtitle_label = QLabel(
            "Створюйте, редагуйте та відстежуйте свої завдання"
        )

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(self.task_input)

        content_layout = QHBoxLayout()

        # Ліва частина інтерфейсу
        list_layout = QVBoxLayout()
        list_layout.addWidget(QLabel("Список завдань"))
        list_layout.addWidget(self.task_list)

        list_buttons = QHBoxLayout()
        list_buttons.addWidget(self.complete_button)
        list_buttons.addWidget(self.edit_button)
        list_buttons.addWidget(self.delete_button)

        list_layout.addLayout(list_buttons)

        # Права частина інтерфейсу
        form_group = QGroupBox("Параметри завдання")
        form_layout = QFormLayout()

        form_layout.addRow(
            "Категорія:",
            self.category_combo
        )

        form_layout.addRow(
            "Пріоритет (1–5):",
            self.priority_spin
        )

        form_layout.addRow(self.urgent_checkbox)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.study_radio)
        radio_layout.addWidget(self.personal_radio)

        form_layout.addRow("Тип:", radio_layout)
        form_layout.addRow(self.add_button)
        form_layout.addRow(self.clear_button)

        form_group.setLayout(form_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(form_group)
        right_layout.addWidget(QLabel("Прогрес виконання"))
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.stats_widget)
        right_layout.addWidget(self.signal_status)
        right_layout.addStretch()

        content_layout.addLayout(list_layout, 3)
        content_layout.addLayout(right_layout, 2)

        main_layout.addLayout(content_layout)
        central_widget.setLayout(main_layout)

    # -------------------------------------------------
    # Створення дій
    # -------------------------------------------------

    def create_actions(self):
        self.new_action = QAction("Нове завдання", self)
        self.new_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_action.triggered.connect(
            lambda checked=False: self.open_task_dialog()
        )

        self.export_action = QAction(
            "Експорт завдань",
            self
        )
        self.export_action.setShortcut(QKeySequence("Ctrl+S"))
        self.export_action.triggered.connect(
            lambda checked=False: self.export_tasks()
        )

        self.exit_action = QAction("Вихід", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.exit_action.triggered.connect(self.close)

        self.complete_action = QAction(
            "Позначити виконаним",
            self
        )
        self.complete_action.setShortcut(QKeySequence("Ctrl+D"))
        self.complete_action.triggered.connect(
            lambda checked=False: self.complete_task()
        )

        self.edit_action = QAction(
            "Редагувати завдання",
            self
        )
        self.edit_action.setShortcut(QKeySequence("Ctrl+E"))
        self.edit_action.triggered.connect(
            lambda checked=False: self.edit_task()
        )

        self.delete_action = QAction(
            "Видалити завдання",
            self
        )
        self.delete_action.setShortcut(QKeySequence("Delete"))
        self.delete_action.triggered.connect(
            lambda checked=False: self.delete_task()
        )

        self.block_signals_action = QAction(
            "Заблокувати сигнали статистики",
            self
        )
        self.block_signals_action.setCheckable(True)
        self.block_signals_action.toggled.connect(
            self.toggle_stats_signals
        )

        self.about_action = QAction("Про програму", self)
        self.about_action.triggered.connect(
            lambda checked=False: self.show_about()
        )

    # -------------------------------------------------
    # Меню
    # -------------------------------------------------

    def create_menus(self):
        file_menu = self.menuBar().addMenu("Файл")

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        actions_menu = self.menuBar().addMenu("Дії")

        actions_menu.addAction(self.complete_action)
        actions_menu.addAction(self.edit_action)
        actions_menu.addAction(self.delete_action)

        settings_menu = self.menuBar().addMenu(
            "Налаштування"
        )

        settings_menu.addAction(self.block_signals_action)
        settings_menu.addAction(self.about_action)

    # -------------------------------------------------
    # Панель інструментів
    # -------------------------------------------------

    def create_toolbar(self):
        toolbar = self.addToolBar("Основні дії")

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.export_action)
        toolbar.addSeparator()
        toolbar.addAction(self.complete_action)
        toolbar.addAction(self.edit_action)
        toolbar.addAction(self.delete_action)

    # -------------------------------------------------
    # Рядок стану
    # -------------------------------------------------

    def create_status_bar(self):
        self.statusBar().showMessage("Програму запущено")

    # -------------------------------------------------
    # З'єднання сигналів і слотів
    # -------------------------------------------------

    def connect_signals(self):
        self.task_input.taskAdded.connect(
            self.add_task_from_signal
        )

        self.stats_widget.statsChanged.connect(
            self.show_statistics_message
        )

        self.add_button.clicked.connect(self.add_task)
        self.complete_button.clicked.connect(
            self.complete_task
        )
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.clear_button.clicked.connect(self.clear_form)

        self.task_list.itemDoubleClicked.connect(
            lambda item: self.edit_task()
        )

    # -------------------------------------------------
    # Перевірка даних
    # -------------------------------------------------

    def validate_task(self, task_data):
        title = task_data.get("title", "").strip()

        if not title:
            return False

        priority = task_data.get("priority")

        if not isinstance(priority, int):
            return False

        if priority not in range(1, 6):
            return False

        return True

    # -------------------------------------------------
    # Додавання завдань
    # -------------------------------------------------

    def add_task(self):
        title = self.task_input.input_field.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Помилка",
                "Введіть назву завдання."
            )
            return

        category = self.category_combo.currentText()

        if self.personal_radio.isChecked():
            category = "Особисте"
        elif self.study_radio.isChecked():
            category = "Навчання"

        task_data = {
            "title": title,
            "category": category,
            "priority": self.priority_spin.value(),
            "urgent": self.urgent_checkbox.isChecked(),
            "description": "",
            "completed": False
        }

        if not self.validate_task(task_data):
            QMessageBox.warning(
                self,
                "Помилка",
                "Перевірте введені дані."
            )
            return

        self.tasks.append(task_data)
        self.task_input.input_field.clear()

        self.refresh_task_list()
        self.update_statistics()

        self.statusBar().showMessage(
            "Завдання додано",
            3000
        )

    def add_task_from_signal(self, title):
        """Слот отримує назву через користувацький сигнал."""

        task_data = {
            "title": title.strip(),
            "category": self.category_combo.currentText(),
            "priority": self.priority_spin.value(),
            "urgent": self.urgent_checkbox.isChecked(),
            "description": "",
            "completed": False
        }

        if not self.validate_task(task_data):
            return

        self.tasks.append(task_data)

        self.refresh_task_list()
        self.update_statistics()

        self.statusBar().showMessage(
            "Завдання додано через власний віджет",
            3000
        )

    # -------------------------------------------------
    # Оновлення списку
    # -------------------------------------------------

    def refresh_task_list(self):
        self.task_list.clear()

        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            urgent = (
                " [ТЕРМІНОВО]"
                if task["urgent"]
                else ""
            )

            text = (
                f"{status} {task['title']} "
                f"| {task['category']} "
                f"| Пріоритет: {task['priority']}{urgent}"
            )

            item = QListWidgetItem(text)

            if task["completed"]:
                item.setForeground(
                    Qt.GlobalColor.darkGreen
                )

            self.task_list.addItem(item)

    def selected_task_index(self):
        return self.task_list.currentRow()

    # -------------------------------------------------
    # Виконання завдання
    # -------------------------------------------------

    def complete_task(self):
        index = self.selected_task_index()

        if index < 0:
            QMessageBox.information(
                self,
                "Інформація",
                "Спочатку виберіть завдання зі списку."
            )
            return

        self.tasks[index]["completed"] = (
            not self.tasks[index]["completed"]
        )

        self.refresh_task_list()
        self.task_list.setCurrentRow(index)

        self.update_statistics()

        self.statusBar().showMessage(
            "Статус завдання змінено",
            3000
        )

    # -------------------------------------------------
    # Редагування завдання
    # -------------------------------------------------

    def edit_task(self):
        index = self.selected_task_index()

        if index < 0:
            QMessageBox.information(
                self,
                "Інформація",
                "Виберіть завдання для редагування."
            )
            return

        dialog = TaskDialog(
            self,
            self.tasks[index]
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            if not self.validate_task(data):
                QMessageBox.warning(
                    self,
                    "Помилка",
                    "Перевірте введені дані."
                )
                return

            self.tasks[index]["title"] = data["title"]
            self.tasks[index]["category"] = data["category"]
            self.tasks[index]["priority"] = data["priority"]
            self.tasks[index]["description"] = data["description"]

            self.refresh_task_list()
            self.task_list.setCurrentRow(index)

            self.update_statistics()

            self.statusBar().showMessage(
                "Завдання успішно відредаговано",
                3000
            )

    # -------------------------------------------------
    # Видалення завдання
    # -------------------------------------------------

    def delete_task(self):
        index = self.selected_task_index()

        if index < 0:
            QMessageBox.information(
                self,
                "Інформація",
                "Виберіть завдання для видалення."
            )
            return

        answer = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви дійсно хочете видалити це завдання?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.tasks.pop(index)

            self.refresh_task_list()
            self.update_statistics()

            self.statusBar().showMessage(
                "Завдання видалено",
                3000
            )

    # -------------------------------------------------
    # Очищення форми
    # -------------------------------------------------

    def clear_form(self):
        self.task_input.input_field.clear()
        self.category_combo.setCurrentIndex(0)
        self.priority_spin.setValue(3)
        self.urgent_checkbox.setChecked(False)
        self.study_radio.setChecked(True)

        self.statusBar().showMessage(
            "Форму очищено",
            3000
        )

    # -------------------------------------------------
    # Створення завдання через діалог
    # -------------------------------------------------

    def open_task_dialog(self):
        dialog = TaskDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            task_data = {
                "title": data["title"],
                "category": data["category"],
                "priority": data["priority"],
                "urgent": False,
                "description": data["description"],
                "completed": False
            }

            if self.validate_task(task_data):
                self.tasks.append(task_data)

                self.refresh_task_list()
                self.update_statistics()

                self.statusBar().showMessage(
                    "Нове завдання створено",
                    3000
                )

    # -------------------------------------------------
    # Статистика
    # -------------------------------------------------

    def update_statistics(self):
        total = len(self.tasks)

        completed = sum(
            1 for task in self.tasks
            if task["completed"]
        )

        self.stats_widget.update_stats(
            total,
            completed
        )

        progress = (
            int(completed / total * 100)
            if total > 0
            else 0
        )

        self.progress_bar.setValue(progress)

    def show_statistics_message(self, total, completed):
        """Слот отримує два цілі числа від віджета статистики."""

        self.statusBar().showMessage(
            f"Статистика: виконано {completed} із {total}",
            3000
        )

    def toggle_stats_signals(self, checked):
        """Блокує або відновлює сигнали статистики."""

        self.stats_widget.blockSignals(checked)

        if checked:
            self.signal_status.setText(
                "Сигнали статистики заблоковані"
            )
        else:
            self.signal_status.setText(
                "Сигнали статистики активні"
            )

    # -------------------------------------------------
    # Експорт завдань
    # -------------------------------------------------

    def export_tasks(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти завдання",
            "tasks.json",
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.tasks,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            QMessageBox.information(
                self,
                "Експорт",
                "Завдання успішно збережено."
            )

            self.statusBar().showMessage(
                "Експорт завершено",
                3000
            )

        except OSError as error:
            QMessageBox.critical(
                self,
                "Помилка",
                f"Не вдалося зберегти файл:\n{error}"
            )

    # -------------------------------------------------
    # Додаткові діалогові вікна
    # -------------------------------------------------

    def show_about(self):
        QMessageBox.about(
            self,
            "Про програму",
            "Менеджер завдань\n"
            "Навчальний проєкт із використанням PyQt6."
        )

        note, accepted = QInputDialog.getText(
            self,
            "Нотатка",
            "Введіть коротку нотатку:"
        )

        if accepted and note.strip():
            self.statusBar().showMessage(
                f"Нотатку введено: {note.strip()}",
                5000
            )

    # -------------------------------------------------
    # Стилізація інтерфейсу
    # -------------------------------------------------

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f3f5f8;
            }

            QLabel {
                color: #263445;
                font-size: 13px;
            }

            QLabel#mainTitle {
                font-size: 25px;
                font-weight: bold;
                color: #243b55;
                padding: 8px;
            }

            QLabel#statsLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 4px;
            }

            QLabel#signalStatus {
                color: #52677e;
                font-style: italic;
            }

            QPushButton {
                background-color: #315b83;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }

            QPushButton:hover {
                background-color: #4278a8;
            }

            QPushButton:pressed {
                background-color: #203e5b;
            }

            QPushButton#addTaskButton {
                background-color: #26734d;
                font-weight: bold;
            }

            QPushButton#addTaskButton:hover {
                background-color: #328b60;
            }

            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                background-color: white;
                border: 1px solid #bdc9d5;
                border-radius: 5px;
                padding: 6px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4278a8;
            }

            QListWidget {
                background-color: white;
                border: 1px solid #cbd5df;
                border-radius: 6px;
                padding: 5px;
            }

            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc9d5;
                border-radius: 7px;
                margin-top: 10px;
                padding: 10px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            QProgressBar {
                border: 1px solid #bdc9d5;
                border-radius: 5px;
                text-align: center;
                background-color: white;
            }

            QProgressBar::chunk {
                background-color: #328b60;
                border-radius: 4px;
            }
        """)


# -------------------------------------------------
# Запуск програми
# -------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
