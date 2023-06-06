from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QScrollArea

app = QApplication([])

# Создаем главное окно
window = QWidget()

# Создаем вертикальный макет для главного окна
layout = QVBoxLayout(window)

# Создаем QScrollArea
scroll_area = QScrollArea()

# Создаем QWidget для содержимого
content_widget = QWidget()

# Создаем вертикальный макет для содержимого
content_layout = QVBoxLayout(content_widget)

# Добавляем виджеты в макет содержимого
content_layout.addWidget(QLabel("Label 1"))
content_layout.addWidget(QLabel("Label 2"))
content_layout.addWidget(QLabel("Label 3"))
content_layout.addWidget(QLabel("Label 4"))
content_layout.addWidget(QLabel("Label 5"))

# Устанавливаем содержимое в QScrollArea
scroll_area.setWidget(content_widget)

# Добавляем QScrollArea в главный макет
layout.addWidget(scroll_area)

# Отображаем главное окно
window.show()
app.exec_()
