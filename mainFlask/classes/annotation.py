class Annotation:

    def __init__(self, id: int, message_id: int, start_pos: int, end_pos: int, annotation: str, reason: str, comment: str):
        self._id = id
        self._message_id = message_id
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._annotation = annotation
        self._reason = reason
        self._comment = comment

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def message_id(self) -> int:
        return self._message_id

    @message_id.setter
    def message_id(self, value: int):
        self._message_id = value

    @property
    def start_pos(self) -> int:
        return self._start_pos

    @start_pos.setter
    def start_pos(self, value: int):
        self._start_pos = value

    @property
    def end_pos(self) -> int:
        return self._end_pos

    @end_pos.setter
    def end_pos(self, value: int):
        self._end_pos = value

    @property
    def annotation(self) -> str:
        return self._annotation

    @annotation.setter
    def annotation(self, value: str):
        self._annotation = value

    @property
    def reason(self) -> str:
        return self._reason

    @reason.setter
    def reason(self, value: str):
        self._reason = value

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    def __str__(self):
        return (f"Annotation(id={self._id}, message_id={self._message_id}, start_pos={self._start_pos}, "
                f"end_pos={self._end_pos}, annotation={self._annotation}, reason={self._reason}, comment={self._comment})")
    
    def __eq__(self, other):
        if isinstance(other, Annotation):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

