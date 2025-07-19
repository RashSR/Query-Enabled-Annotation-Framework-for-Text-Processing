class SpacyMatch:
    def __init__(
        self,
        message_id: int,
        chat_id: int,
        start_pos: int,
        end_pos: int,
        text: str,
        lemma: str = None,
        pos: str = None,
        tag: str = None,
        dep: int = None,
        shape: str = None,
        is_alpha: bool = None,
        is_stop: bool = None,
        tense: str = None,
        person: str = None,
        verb_form: str = None,
        voice: str = None,
        degree: str = None,
        gram_case: str = None,
        number: str = None,
        gender: str = None,
        mood: str = None,
        pron_type: str = None
    ):
        self._id = None
        self._message_id = message_id
        self._chat_id = chat_id
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._text = text
        self._lemma = lemma
        self._pos = pos
        self._tag = tag
        self._dep = dep
        self._shape = shape
        self._is_alpha = is_alpha
        self._is_stop = is_stop
        self._tense = tense
        self._person = person
        self._verb_form = verb_form
        self._voice = voice
        self._degree = degree
        self._gram_case = gram_case
        self._number = number
        self._gender = gender
        self._mood = mood
        self._pron_type = pron_type

    def __str__(self):
        return f"""SpacyMatch(
    id: {self._id},
    message_id: {self._message_id},
    chat_id: {self._chat_id},
    start_pos: {self._start_pos},
    end_pos: {self._end_pos},
    text: '{self._text}',
    lemma: '{self._lemma}',
    pos: '{self._pos}',
    tag: '{self._tag}',
    dep: {self._dep},
    shape: '{self._shape}',
    is_alpha: {self._is_alpha},
    is_stop: {self._is_stop},
    tense: '{self._tense}',
    person: '{self._person}',
    verb_form: '{self._verb_form}',
    voice: '{self._voice}',
    degree: '{self._degree}',
    gram_case: '{self._gram_case}',
    number: '{self._number}',
    gender: '{self._gender}',
    mood: '{self._mood}',
    pron_type: '{self._pron_type}'
)"""

    # --- Properties ---
    @property
    def id(self): return self._id
    @id.setter
    def id(self, value): self._id = value

    @property
    def message_id(self): return self._message_id
    @message_id.setter
    def message_id(self, value): self._message_id = value

    @property
    def chat_id(self): return self._chat_id
    @chat_id.setter
    def chat_id(self, value): self._chat_id = value

    @property
    def start_pos(self): return self._start_pos
    @start_pos.setter
    def start_pos(self, value): self._start_pos = value

    @property
    def end_pos(self): return self._end_pos
    @end_pos.setter
    def end_pos(self, value): self._end_pos = value

    @property
    def text(self): return self._text
    @text.setter
    def text(self, value): self._text = value

    @property
    def lemma(self): return self._lemma
    @lemma.setter
    def lemma(self, value): self._lemma = value

    @property
    def pos(self): return self._pos
    @pos.setter
    def pos(self, value): self._pos = value

    @property
    def tag(self): return self._tag
    @tag.setter
    def tag(self, value): self._tag = value

    @property
    def dep(self): return self._dep
    @dep.setter
    def dep(self, value): self._dep = value

    @property
    def shape(self): return self._shape
    @shape.setter
    def shape(self, value): self._shape = value

    @property
    def is_alpha(self): return self._is_alpha
    @is_alpha.setter
    def is_alpha(self, value): self._is_alpha = value

    @property
    def is_stop(self): return self._is_stop
    @is_stop.setter
    def is_stop(self, value): self._is_stop = value

    @property
    def tense(self): return self._tense
    @tense.setter
    def tense(self, value): self._tense = value

    @property
    def person(self): return self._person
    @person.setter
    def person(self, value): self._person = value

    @property
    def verb_form(self): return self._verb_form
    @verb_form.setter
    def verb_form(self, value): self._verb_form = value

    @property
    def voice(self): return self._voice
    @voice.setter
    def voice(self, value): self._voice = value

    @property
    def degree(self): return self._degree
    @degree.setter
    def degree(self, value): self._degree = value

    @property
    def gram_case(self): return self._gram_case
    @gram_case.setter
    def gram_case(self, value): self._gram_case = value

    @property
    def number(self): return self._number
    @number.setter
    def number(self, value): self._number = value

    @property
    def gender(self): return self._gender
    @gender.setter
    def gender(self, value): self._gender = value

    @property
    def mood(self): return self._mood
    @mood.setter
    def mood(self, value): self._mood = value

    @property
    def pron_type(self): return self._pron_type
    @pron_type.setter
    def pron_type(self, value): self._pron_type = value
