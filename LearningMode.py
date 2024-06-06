import random

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QProgressBar

from Word import Word
from Style import setColours

class LearningMode(QDialog):
    def __init__(self, words: list[Word]):
        super().__init__()
        self.setWindowTitle("Learning Mode")
        self.words = words.copy()
        self.current_word_index = -1
        self.correct_answer = ""
        self.correct_answers = 0
        self.total_questions = 0

        self.layout = QVBoxLayout()

        self.prompt_label = QLabel()
        self.layout.addWidget(self.prompt_label)

        self.answer_input = QLineEdit()
        self.layout.addWidget(self.answer_input)

        self.check_button = QPushButton("Check Answer")
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                        text-align: center;
                        font-size: 12pt;
                    }
                    QProgressBar::chunk {
                        background-color: #05B8CC;
                        width: 20px;
                    }
                """)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
        self.new_session()

        setColours(self)

    def new_session(self):
        self.correct_answers = 0
        self.total_questions = 0
        for word in self.words:
            word.result = 0
        self.progress_bar.setMaximum(len(self.words))
        self.progress_bar.setValue(0)
        self.new_word()

    def new_word(self):
        if not self.words:
            self.end_learning()
            return

        self.current_word_index = random.randint(0, len(self.words) - 1)
        word = self.words[self.current_word_index]
        if word.result < 4:
            self.prompt_label.setText(f"Define: {word.term}")
            self.correct_answer = word.definition
        else:
            self.prompt_label.setText(f"What is the term for: {word.definition}")
            self.correct_answer = word.term

        self.answer_input.clear()
        self.total_questions += 1

    def check_answer(self):
        user_answer = self.answer_input.text()
        if user_answer.strip().lower() in [ans.strip().lower() for ans in self.correct_answer.split(", ")]:
            self.correct_response()
        else:
            self.incorrect_response()

    def correct_response(self):
        self.correct_answers += 1
        word = self.words[self.current_word_index]
        word.result += 1 if word.result % 4 != 0 else 4
        if word.result == 8:
            self.words.pop(self.current_word_index)
            self.update_progress()
        self.new_word()

    def incorrect_response(self):
        word = self.words[self.current_word_index]
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Incorrect Answer")
        msg_box.setText(
            f"{self.prompt_label.text()}\nCorrect answer: {self.correct_answer}\nYour answer: {self.answer_input.text()}\n"
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Ignore)
        ret = msg_box.exec()

        if ret == QMessageBox.StandardButton.Ignore:
            self.correct_response()
        else:
            if word.result % 4 == 0:
                word.result += 1
            elif word.result % 4 != 1:
                word.result -= 1
            self.new_word()

    def update_progress(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def end_learning(self):
        accuracy = self.correct_answers / self.total_questions if self.total_questions > 0 else 0
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Session Statistics")
        msg_box.setText(
            f"Session Statistics:\nCorrect Answers: {self.correct_answers}\nTotal Questions: {self.total_questions}\nAccuracy: {accuracy:.2%}"
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        self.accept()

