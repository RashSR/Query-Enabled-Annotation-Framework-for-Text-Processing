class LTMatch:
    def __init__(self, message_id: int, chat_id: int, start_pos: int, end_pos: int, text: str, category: str, rule_id: str):
        self._message_id = message_id #TODO: load message
        self._chat_id = chat_id
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._text = text
        self._category = category
        self._rule_id = rule_id

    def __str__(self):
        toString = f"""text: {self._text}
        Category: {self._category}
        RuleId: {self._rule_id}
        text: {self._text}
        startPos: {self._start_pos}
        endPos: {self._end_pos}
        id: {self._id}
        message_id: {self._message_id}
        chat_id: {self._chat_id}
        """

        return toString
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        self._id = value

    @property
    def message_id(self) -> int:
        return self._message_id
    
    @message_id.setter
    def message_id(self, value: int) -> None:
        self._message_id = value

    #TODO: dont need to be there
    @property
    def chat_id(self) -> int:
        return self._chat_id
    
    @chat_id.setter
    def chat_id(self, value: int) -> None:
        self._chat_id = value

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
