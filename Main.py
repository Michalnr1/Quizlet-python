import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTreeWidget, QTreeWidgetItem, \
    QPushButton, QDialog, QLineEdit, QCheckBox, QHBoxLayout, QFileDialog, QSpacerItem, QSizePolicy

from Database import Database
from LearningMode import LearningMode
from Word import Word
from WordList import WordList
from Style import setColours


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

        setColours(self)

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

        setColours(self)

    def save(self):
        self.word.term = self.term_edit.text()
        self.word.definition = self.definition_edit.text()
        self.word.notes = self.notes_edit.text()

        self.tree_item.setText(1, self.word.term)
        self.tree_item.setText(2, self.word.definition)
        self.tree_item.setText(3, self.word.notes)

        self.accept()

class AddWordDialog(QDialog):
    def __init__(self, word_list: WordList, db: Database):
        super().__init__()
        self.setWindowTitle("Add Word")
        self.word_list = word_list
        self.db = db
        self.current_word = Word("new", "newly added word")

        self.layout = QVBoxLayout()

        self.term_edit = QLineEdit()
        self.definition_edit = QLineEdit()
        self.notes_edit = QLineEdit()

        self.layout.addWidget(QLabel("Term"))
        self.layout.addWidget(self.term_edit)
        self.layout.addWidget(QLabel("Definition"))
        self.layout.addWidget(self.definition_edit)
        self.layout.addWidget(QLabel("Notes"))
        self.layout.addWidget(self.notes_edit)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next)
        self.layout.addWidget(self.next_button)

        self.save_button = QPushButton("Save")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save)

        self.setLayout(self.layout)

        setColours(self)

    def save(self):
        self.current_word.term = self.term_edit.text()
        self.current_word.definition = self.definition_edit.text()
        self.current_word.notes = self.notes_edit.text()
        self.current_word.id = self.db.add_word(self.word_list.id, self.current_word.selected, self.current_word.term, self.current_word.definition, self.current_word.notes)
        self.word_list.words.append(self.current_word)
        self.accept()

    def next(self):
        self.current_word.term = self.term_edit.text()
        self.current_word.definition = self.definition_edit.text()
        self.current_word.notes = self.notes_edit.text()
        self.current_word.id = self.db.add_word(self.word_list.id, self.current_word.selected, self.current_word.term, self.current_word.definition, self.current_word.notes)
        self.word_list.words.append(self.current_word)
        self.term_edit.clear()
        self.definition_edit.clear()
        self.notes_edit.clear()
        self.term_edit.setFocus()
        self.current_word = Word("new", "newly added word")


class WordListEditor(QDialog):
    def __init__(self, word_list: WordList, db: Database):
        super().__init__()
        self.setWindowTitle(word_list.title)
        self.setGeometry(200, 200, 600, 400)
        self.word_list = word_list
        self.db = db

        self.layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["Selected", "Term", "Definition", "Notes", "Edit"])
        self.populate_tree()
        self.layout.addWidget(self.tree)

        self.add_word_button = QPushButton("Add Word")
        self.add_word_button.clicked.connect(self.add_word)
        self.layout.addWidget(self.add_word_button)

        self.delete_word_button = QPushButton("Delete Word")
        self.delete_word_button.clicked.connect(self.delete_word)
        self.layout.addWidget(self.delete_word_button)

        self.start_learning_button = QPushButton("Start Learning Mode")
        self.start_learning_button.clicked.connect(self.start_learning_mode)
        self.layout.addWidget(self.start_learning_button)

        self.setLayout(self.layout)
        self.add_word_button.setFocus()

        setColours(self)

    def populate_tree(self):
        self.tree.clear()
        for word in self.word_list.words:
            item = QTreeWidgetItem(["", word.term, word.definition, word.notes, ""])
            self.tree.addTopLevelItem(item)
            checkbox = QCheckBox()
            checkbox.setChecked(word.selected)
            checkbox.stateChanged.connect(lambda state, w=word: self.update_word_selection(w, state))
            self.tree.setItemWidget(item, 0, checkbox)

            edit_button = QPushButton()
            edit_button.setObjectName("editButton")
            edit_button.setIcon(QIcon("edit_icon.png"))
            edit_button.setFixedSize(24, 24)
            edit_button.setIconSize(QSize(16, 16))
            edit_button.clicked.connect(lambda _, i=item, w=word: self.edit_word(i, w))
            self.tree.setItemWidget(item, 4, edit_button)
        self.tree.setCurrentItem(None)

    def update_word_selection(self, word, state):
        if not word.selected:
            word.selected = True
        else:
            word.selected = False
        self.db.update_word(word.id, word.selected, word.term, word.definition, word.notes)

    def add_word(self):
        dialog = AddWordDialog(self.word_list, self.db)
        dialog.exec()
        self.populate_tree()

    def edit_word(self, item, word):
        dialog = EditWordDialog(word, item)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item.setText(1, word.term)
            item.setText(2, word.definition)
            item.setText(3, word.notes)
            self.db.update_word(word.id, word.selected, word.term, word.definition, word.notes)

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

        setColours(self)

    def add_word_list(self):
        self.title = self.title_edit.text()
        if self.title:
            self.accept()
        else:
            self.reject()


class Quizlet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Buddy")
        self.setGeometry(100, 100, 300, 400)

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
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 30)
        self.tree.setHeaderLabels(["Title", "Edit"])
        layout.addWidget(self.tree)

        self.populate_tree()

        self.add_list_button = QPushButton("Add Word List")
        self.add_list_button.clicked.connect(self.add_word_list)
        layout.addWidget(self.add_list_button)

        self.delete_list_button = QPushButton("Delete List")
        self.delete_list_button.clicked.connect(self.delete_list)
        layout.addWidget(self.delete_list_button)

        import_layout = QHBoxLayout()


        self.import_button = QPushButton("Import Word List")
        self.import_button.clicked.connect(self.import_word_list)
        self.import_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        import_layout.addWidget(self.import_button)

        self.import_info_label = QLabel()
        self.import_info_label.setPixmap(QPixmap("info.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio))
        self.import_info_label.setToolTip("The file should be formatted as follows:\nTerm - Definition (Optional Notes)")
        import_layout.addWidget(self.import_info_label)

        layout.addLayout(import_layout)

        self.export_button = QPushButton("Export Word List")
        self.export_button.clicked.connect(self.export_word_list)
        layout.addWidget(self.export_button)

        self.tree.itemDoubleClicked.connect(self.open_list)

        central_widget.setLayout(layout)

        setColours(self)

    def populate_tree(self):
        self.tree.clear()
        for word_list in self.word_lists:
            item = QTreeWidgetItem([word_list.title, ""])
            self.tree.addTopLevelItem(item)

            edit_button = QPushButton()
            edit_button.setObjectName("editButton")
            edit_button.setIcon(QIcon("edit_icon.png"))
            edit_button.setFixedSize(24, 24)
            edit_button.setIconSize(QSize(16, 16))
            edit_button.clicked.connect(lambda _, i=item, wl=word_list: self.edit_list(i, wl))
            self.tree.setItemWidget(item, 1, edit_button)

    def load_word_lists(self):
        return self.db.load_word_lists()

    def add_word_list(self):
        dialog = AddWordListDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_word_list = WordList(dialog.title, [])
            new_word_list.id = self.db.add_word_list(new_word_list.title)
            self.word_lists.append(new_word_list)
            self.populate_tree()

    def edit_list(self, item, word_list):
        dialog = EditWordListDialog(word_list, item)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.db.update_word_list(word_list.id, word_list.title)
            self.populate_tree()

    def delete_list(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]
            self.db.delete_word_list(selected_list.id)
            del self.word_lists[selected_index]
            self.populate_tree()

    def open_list(self, item):
        selected_index = self.tree.indexOfTopLevelItem(item)
        selected_list = self.word_lists[selected_index]
        dialog = WordListEditor(selected_list, self.db)
        dialog.exec()

    def import_word_list(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Word List", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                words = []
                for line in lines:
                    parts = line.strip().split(' - ')
                    term = parts[0]
                    definition, notes = '', ''
                    if len(parts) > 1:
                        if '(' in parts[1] and parts[1].endswith(')'):
                            definition, notes = parts[1].rsplit(' (', 1)
                            notes = notes[:-1]
                        else:
                            definition = parts[1]
                    words.append(Word(term, definition, notes))

                dialog = AddWordListDialog(self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_word_list = WordList(dialog.title, words)
                    new_word_list.id = self.db.add_word_list(new_word_list.title)
                    self.db.import_word_list(new_word_list.id, words)
                    self.word_lists.append(new_word_list)
                    self.populate_tree()

    def export_word_list(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            selected_index = self.tree.indexOfTopLevelItem(selected_item)
            selected_list = self.word_lists[selected_index]

            file_name, _ = QFileDialog.getSaveFileName(self, "Export Word List", "", "Text Files (*.txt);;All Files (*)")
            if file_name:
                words = self.db.export_word_list(selected_list.id)
                with open(file_name, 'w', encoding='utf-8') as file:
                    for term, definition, notes in words:
                        if notes:
                            file.write(f"{term} - {definition} ({notes})\n")
                        else:
                            file.write(f"{term} - {definition}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Quizlet()
    window.show()
    sys.exit(app.exec())