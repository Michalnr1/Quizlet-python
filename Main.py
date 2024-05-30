import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, \
    QPushButton, QDialog, QLineEdit, QCheckBox

from LearningMode import LearningMode
from Word import Word
from WordList import WordList


class EditWordListDialog(QDialog):
    def __init__(self, word_list: WordList, tree_item: QTreeWidgetItem):
        super().__init__()
        self.setWindowTitle("Edit Word List Title")
        self.word_list = word_list
        self.tree_item = tree_item

        self.layout = QVBoxLayout()

        self.title_edit = QLineEdit(self.word_list.title)
        self.layout.addWidget(self.title_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save(self):
        self.word_list.title = self.title_edit.text()
        self.tree_item.setText(0, self.word_list.title)
        self.accept()


class EditWordDialog(QDialog):
    def __init__(self, word: Word, tree_item: QTreeWidgetItem):
        super().__init__()
        self.setWindowTitle("Edit Word")
        self.word = word
        self.tree_item = tree_item

        self.layout = QVBoxLayout()

        self.term_edit = QLineEdit(self.word.term)
        self.definition_edit = QLineEdit(self.word.definition)
        self.notes_edit = QLineEdit(self.word.notes)

        self.layout.addWidget(QLabel("Term"))
        self.layout.addWidget(self.term_edit)
        self.layout.addWidget(QLabel("Definition"))
        self.layout.addWidget(self.definition_edit)
        self.layout.addWidget(QLabel("Notes"))
        self.layout.addWidget(self.notes_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save(self):
        self.word.term = self.term_edit.text()
        self.word.definition = self.definition_edit.text()
        self.word.notes = self.notes_edit.text()

        # Update tree item
        self.tree_item.setText(0, self.word.term)
        self.tree_item.setText(1, self.word.definition)
        self.tree_item.setText(3, self.word.notes)

        self.accept()


class WordListEditor(QDialog):
    def __init__(self, word_list: WordList):
        super().__init__()
        self.setWindowTitle(word_list.title)
        self.word_list = word_list

        self.layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels(["Selected", "Term", "Definition", "Notes"])
        self.populate_tree()
        self.layout.addWidget(self.tree)

        self.add_word_button = QPushButton("Add Word")
        self.add_word_button.clicked.connect(self.add_word)
        self.layout.addWidget(self.add_word_button)

        self.edit_word_button = QPushButton("Edit Selected Word")
        self.edit_word_button.clicked.connect(self.edit_selected_word)
        self.layout.addWidget(self.edit_word_button)

        self.start_learning_button = QPushButton("Start Learning Mode")
        self.start_learning_button.clicked.connect(self.start_learning_mode)
        self.layout.addWidget(self.start_learning_button)

        self.setLayout(self.layout)

    def populate_tree(self):
        self.tree.clear()
        for word in self.word_list.words:
            item = QTreeWidgetItem(["", word.term, word.definition, word.notes])
            self.tree.addTopLevelItem(item)
            checkbox = QCheckBox()
            checkbox.setChecked(word.selected)
            checkbox.stateChanged.connect(self.create_update_selection_callback(word))
            self.tree.setItemWidget(item, 0, checkbox)

    def create_update_selection_callback(self, word):
        return lambda state: self.update_word_selection(word, state)

    def update_word_selection(self, word, state):
        word.selected = state == Qt.CheckState.Checked

    def add_word(self):
        new_word = Word("new", "newly added word")
        self.word_list.words.append(new_word)
        item = QTreeWidgetItem(["", new_word.term, new_word.definition, new_word.notes])
        checkbox = QCheckBox()
        checkbox.setChecked(new_word.selected)
        checkbox.stateChanged.connect(self.create_update_selection_callback(new_word))
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, checkbox)

    def edit_selected_word(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_index = self.tree.indexOfTopLevelItem(selected_item)
        selected_word = self.word_list.words[selected_index]

        dialog = EditWordDialog(selected_word, selected_item)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_item.setText(1, selected_word.term)
            selected_item.setText(2, selected_word.definition)
            selected_item.setText(3, selected_word.notes)

    def start_learning_mode(self):
        dialog = LearningMode(self.word_list)
        dialog.exec()


class Quizlet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word List Application")
        self.setGeometry(100, 100, 600, 400)

        self.word_lists = [
            WordList("List 1", [
                Word("example", "a representative form or pattern"),
                Word("sample", "a small part or quantity intended to show what the whole is like")
            ]),
            WordList("List 2", [
                Word("test", "a procedure intended to establish the quality"),
                Word("trial", "a test of the performance, qualities, or suitability of someone or something")
            ])
        ]

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.title_label = QLabel("Word Lists")
        layout.addWidget(self.title_label)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Title"])
        layout.addWidget(self.tree)

        self.populate_tree()

        self.edit_list_button = QPushButton("Edit List Title")
        self.edit_list_button.clicked.connect(self.edit_list_title)
        layout.addWidget(self.edit_list_button)

        self.open_list_button = QPushButton("Open List")
        self.open_list_button.clicked.connect(self.open_list)
        layout.addWidget(self.open_list_button)

        central_widget.setLayout(layout)

    def populate_tree(self):
        self.tree.clear()
        for word_list in self.word_lists:
            item = QTreeWidgetItem([word_list.title])
            self.tree.addTopLevelItem(item)

    def edit_list_title(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            dialog = EditWordListDialog(selected_list, selected_item)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.populate_tree()

    def open_list(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            dialog = WordListEditor(selected_list)
            dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Quizlet()
    window.show()
    sys.exit(app.exec())
