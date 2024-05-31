class Word:
    """
    Represents a word with its definition, selection status, and notes.
    """

    def __init__(self, term: str, definition: str, notes: str = "", selected: bool = False) -> None:
        """
        Initializes a new instance of the Word class.

        :param term: The term or word.
        :param definition: The definition of the term.
        :param notes: Additional notes about the word.
        :param selected: The selection status of the word.
        """
        self.id = None
        self._term = term
        self._definition = definition
        self._selected = selected
        self._notes = notes
        self.result = 0  # not saved to the database

    @property
    def term(self) -> str:
        """
        Returns the term.

        :return: The term.
        """
        return self._term

    @term.setter
    def term(self, term: str) -> None:
        """
        Sets the term.

        :param term: The new term.
        """
        self._term = term

    @property
    def definition(self) -> str:
        """
        Returns the definition.

        :return: The definition.
        """
        return self._definition

    @definition.setter
    def definition(self, definition: str) -> None:
        """
        Sets the definition.

        :param definition: The new definition.
        """
        self._definition = definition

    @property
    def selected(self) -> bool:
        """
        Returns the selection status.

        :return: True if selected, False otherwise.
        """
        return self._selected

    @selected.setter
    def selected(self, selected: bool) -> None:
        """
        Sets the selection status.

        :param selected: The new selection status.
        """
        self._selected = selected

    @property
    def notes(self) -> str:
        """
        Returns the notes.

        :return: The notes.
        """
        return self._notes

    @notes.setter
    def notes(self, notes: str) -> None:
        """
        Sets the notes.

        :param notes: The new notes.
        """
        self._notes = notes
