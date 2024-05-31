import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, \
    QPushButton, QDialog, QLineEdit, QCheckBox

from Database import Database
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
        self.tree_item.setText(1, self.word.term)
        self.tree_item.setText(2, self.word.definition)
        self.tree_item.setText(3, self.word.notes)

        self.accept()


class WordListEditor(QDialog):
    def __init__(self, word_list: WordList, db: Database):
        super().__init__()
        self.setWindowTitle(word_list.title)
        self.word_list = word_list
        self.db = db

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

        self.delete_word_button = QPushButton("Delete Word")
        self.delete_word_button.clicked.connect(self.delete_word)
        self.layout.addWidget(self.delete_word_button)

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
            checkbox.stateChanged.connect(lambda state, w=word: self.update_word_selection(w, state))
            self.tree.setItemWidget(item, 0, checkbox)

    def update_word_selection(self, word, state):
        word.selected = state == Qt.CheckState.Checked
        self.db.update_word(word.id, word.term, word.definition, word.selected, word.notes)

    def add_word(self):
        new_word = Word("new", "newly added word")
        new_word.id = self.db.add_word(self.word_list.id, new_word.selected, new_word.term, new_word.definition, new_word.notes)
        self.word_list.words.append(new_word)
        item = QTreeWidgetItem(["", new_word.term, new_word.definition, new_word.notes])
        checkbox = QCheckBox()
        checkbox.setChecked(new_word.selected)
        checkbox.stateChanged.connect(lambda state, w=new_word: self.update_word_selection(w, state))
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, checkbox)
        print(f"Added word: {new_word.term}, ID: {new_word.id}")  # Debug print

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
            self.db.update_word(selected_word.id, selected_word.selected, selected_word.term, selected_word.definition, selected_word.notes)

    def delete_word(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_word = self.word_list.words[selected_index]
            self.db.delete_word(selected_word.id)
            del self.word_list.words[selected_index]
            self.populate_tree()

    def start_learning_mode(self):
        selected_words = [word for word in self.word_list.words if word.selected]
        if not selected_words:
            selected_words = self.word_list.words
        dialog = LearningMode(selected_words)
        dialog.exec()


class AddWordListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Word List")

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Title:")
        self.layout.addWidget(self.title_label)

        self.title_edit = QLineEdit()
        self.layout.addWidget(self.title_edit)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_word_list)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

    def add_word_list(self):
        self.title = self.title_edit.text()
        if self.title:
            self.accept()
        else:
            self.reject()

class Quizlet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word List Application")
        self.setGeometry(100, 100, 600, 400)

        self.db = Database()
        self.word_lists = self.load_word_lists()

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

        self.add_list_button = QPushButton("Add Word List")
        self.add_list_button.clicked.connect(self.add_word_list)
        layout.addWidget(self.add_list_button)

        self.edit_list_button = QPushButton("Edit List Title")
        self.edit_list_button.clicked.connect(self.edit_list_title)
        layout.addWidget(self.edit_list_button)

        self.delete_list_button = QPushButton("Delete List")
        self.delete_list_button.clicked.connect(self.delete_list)
        layout.addWidget(self.delete_list_button)

        self.open_list_button = QPushButton("Open List")
        self.open_list_button.clicked.connect(self.open_list)
        layout.addWidget(self.open_list_button)

        central_widget.setLayout(layout)

    def populate_tree(self):
        self.tree.clear()
        for word_list in self.word_lists:
            item = QTreeWidgetItem([word_list.title])
            self.tree.addTopLevelItem(item)

    def load_word_lists(self):
        return self.db.load_word_lists()

    def add_word_list(self):
        dialog = AddWordListDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_word_list = WordList(dialog.title, [])
            new_word_list.id = self.db.add_word_list(new_word_list.title)
            self.word_lists.append(new_word_list)
            self.populate_tree()

    def edit_list_title(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            dialog = EditWordListDialog(selected_list, selected_item)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.db.update_word_list(selected_list.id, selected_list.title)
                self.populate_tree()

    def delete_list(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            self.db.delete_word_list(selected_list.id)
            del self.word_lists[selected_index]
            self.populate_tree()

    def open_list(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            dialog = WordListEditor(selected_list, self.db)
            dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Quizlet()
    window.show()
    sys.exit(app.exec())
