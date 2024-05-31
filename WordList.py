from typing import List

import Word

class WordList:
    """
    Represents a list of words with a title.
    """

    def __init__(self, title: str, words: List[Word], id = None) -> None:
        """
        Initializes a new instance of the WordList class.

        :param title: The title of the word list.
        :param words: A list of Word objects.
        """
        self.id = id
        self._title = title
        self._words = words

    @property
    def title(self) -> str:
        """
        Returns the title of the word list.

        :return: The title.
        """
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        """
        Sets the title of the word list.

        :param title: The new title.
        """
        self._title = title

    @property
    def words(self) -> List[Word]:
        """
        Returns the list of words.

        :return: A list of Word objects.
        """
        return self._words

    @words.setter
    def words(self, words: List[Word]) -> None:
        """
        Sets the list of words.

        :param words: The new list of Word objects.
        """
        self._words = words