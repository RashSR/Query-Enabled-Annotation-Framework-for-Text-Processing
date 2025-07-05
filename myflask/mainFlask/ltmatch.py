class LTMatch:
    def __init__(self, startPos: int, endPos: int, text: str, category: str, rule_id: str):
        self._startPos = startPos
        self._endPos = endPos
        self._text = text
        self._category = category
        self._rule_id = rule_id

    def __str__(self):
        toString = f"""text: {self._text}
        Category: {self._category}
        RuleId: {self._rule_id}
        text: {self._text}
        startPos: {self._startPos}
        endPos: {self._endPos}
        """

        return toString
    
    @property
    def start_pos(self) -> int:
        return self._start_pos

    @start_pos.setter
    def start_pos(self, value: int) -> None:
        self._start_pos = value

    @property
    def end_pos(self) -> int:
        return self._end_pos

    @end_pos.setter
    def end_pos(self, value: int) -> None:
        self._end_pos = value

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        self._category = value

    @property
    def rule_id(self) -> str:
        return self._rule_id

    @rule_id.setter
    def rule_id(self, value: str) -> None:
        self._rule_id = value
