import random

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from WordList import WordList


class LearningMode(QDialog):
    def __init__(self, word_list: WordList):
        super().__init__()
        self.setWindowTitle("Learning Mode")
        self.word_list = word_list.words.copy()
        self.current_word_index = -1
        self.correct_answer = ""

        self.layout = QVBoxLayout()

        self.prompt_label = QLabel()
        self.layout.addWidget(self.prompt_label)

        self.answer_input = QLineEdit()
        self.layout.addWidget(self.answer_input)

        self.check_button = QPushButton("Check Answer")
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        self.setLayout(self.layout)
        self.new_word()

    def new_word(self):
        if not self.word_list:
            self.end_learning()
            return

        self.current_word_index = random.randint(0, len(self.word_list) - 1)
        word = self.word_list[self.current_word_index]
        if word.result < 4:
            self.prompt_label.setText(f"Define: {word.term}")
            self.correct_answer = word.definition
        else:
            self.prompt_label.setText(f"What is the term for: {word.definition}")
            self.correct_answer = word.term

        self.answer_input.clear()

    def check_answer(self):
        user_answer = self.answer_input.text()
        if user_answer.strip().lower() in [ans.strip().lower() for ans in self.correct_answer.split(", ")]:
            self.correct_response()
        else:
            self.incorrect_response()

    def correct_response(self):
        word = self.word_list[self.current_word_index]
        word.result += 1 if word.result % 4 != 0 else 4
        if word.result % 8 == 0: # zamienić na == 8
            self.word_list.pop(self.current_word_index)
        self.new_word()

    def incorrect_response(self):
        word = self.word_list[self.current_word_index]
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Incorrect Answer")
        msg_box.setText(
            f"{self.prompt_label.text()}\nCorrect answer: {self.correct_answer}\nYour answer: {self.answer_input.text()}\n"
            f"{'' if not word.notes else 'Notes: ' + word.notes}"
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

    def end_learning(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Congratulations!")
        msg_box.setText("You have completed the learning session!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        self.accept()
