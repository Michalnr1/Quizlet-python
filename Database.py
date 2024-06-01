import sqlite3
from Word import Word
from WordList import WordList


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('word_lists.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS word_lists (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY,
                list_id INTEGER NOT NULL,
                selected BOOLEAN NOT NULL,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (list_id) REFERENCES word_lists (id)
            )''')

    def add_word_list(self, title):
        with self.conn:
            cursor = self.conn.execute('INSERT INTO word_lists (title) VALUES (?)', (title,))
            return cursor.lastrowid

    def update_word_list(self, list_id, title):
        with self.conn:
            self.conn.execute('UPDATE word_lists SET title = ? WHERE id = ?', (title, list_id))

    def delete_word_list(self, list_id):
        with self.conn:
            self.conn.execute('DELETE FROM word_lists WHERE id = ?', (list_id,))
            self.conn.execute('DELETE FROM words WHERE list_id = ?', (list_id,))

    def add_word(self, list_id, selected, term, definition, notes):
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO words (list_id, selected, term, definition, notes) VALUES (?, ?, ?, ?, ?)',
                (list_id, selected, term, definition, notes)
            )
            return cursor.lastrowid

    def update_word(self, word_id, selected, term, definition, notes):
        with self.conn:
            self.conn.execute(
                'UPDATE words SET selected = ?, term = ?, definition = ?, notes = ? WHERE id = ?',
                (selected, term, definition, notes, word_id)
            )

    def delete_word(self, word_id):
        with self.conn:
            self.conn.execute('DELETE FROM words WHERE id = ?', (word_id,))

    def load_word_lists(self):
        word_lists = []
        with self.conn:
            cursor = self.conn.execute('SELECT id, title FROM word_lists')
            for row in cursor.fetchall():
                word_list = WordList(row[1], self.load_words(row[0]), row[0])
                word_lists.append(word_list)
        return word_lists

    def load_words(self, list_id):
        words = []
        with self.conn:
            cursor = self.conn.execute('SELECT id, selected, term, definition, notes FROM words WHERE list_id = ?', (list_id,))
            for row in cursor.fetchall():
                word = Word(row[2], row[3], row[4])
                word.id = row[0]
                word.selected = bool(row[1])
                words.append(word)
        return words

    def import_word_list(self, word_list_id, words):
        for word in words:
            self.add_word(word_list_id, word.selected, word.term, word.definition, word.notes)

    def export_word_list(self, word_list_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT term, definition, notes FROM words WHERE list_id=?", (word_list_id,))
        return cursor.fetchall()
