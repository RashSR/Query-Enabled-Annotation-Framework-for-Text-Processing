from classes.messagetype import MessageType
from mainFlask.cachestore import CacheStore
from mainFlask.ltmatch import LTMatch

class Message:
    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = MessageType.TEXT, quoted_message = None, annotated_text = None, chat = None):
        self.chat_id = chat_id
        self._message_id = message_id
        self.sender = sender
        self.timestamp = timestamp
        self.content = content
        self.message_type = message_type
        self.quoted_message = quoted_message
        self._error_list: list[LTMatch] = []
        self._ltmatch_ids = []
        self._annotated_text = annotated_text
        self._chat = chat

    def __str__(self):
        toString = f"""ChatId: {self.chat_id}, MessageId: {str(self._message_id)}
        Sender: {self.sender.name}
        Timestamp: {self.timestamp}
        Content: {self.content}
        MessageType: {self.message_type}
        quotedMessage: {{ {self.quoted_message } }}
        ErrorTypes: {len(self._error_list)}
        """
        return toString
    
    def hasQuote(self):
        if self.quoted_message == None:
            return True
        return False
    
    def add_error(self, error: LTMatch):
        self._error_list.append(error)

    #improves performance with seen. from WC O(n²) to O(n)
    def get_error_ruleIds(self) -> list[str]:
        seen = set()
        rule_ids = []

        for ltm in self._error_list:
            rid = ltm.rule_id
            if rid not in seen: #because this is O(1) in avg case
                seen.add(rid)
                rule_ids.append(rid)

        
        return rule_ids
    
    #improves performance with seen. from WC O(n²) to O(n)
    def get_error_categories(self) -> list[str]:
        seen = set()
        category_ids = []

        for ltm in self._error_list:
            cid = ltm.category
            if cid not in seen: #because this is O(1) in avg case
                seen.add(cid)
                category_ids.append(cid)

        return category_ids

    @property
    def error_list(self) -> list[LTMatch]:
        if len(self._error_list)==0: #TODO only load errorlist once
            self._error_list = CacheStore.Instance().get_all_ltms_by_msg_id_and_chat_id(self._message_id, self.chat_id)
        return self._error_list

    @error_list.setter
    def error_list(self, value):
        self._error_list = value

    #return author
    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def annotated_text(self):
        return self._annotated_text
    
    @annotated_text.setter
    def annotated_text(self, value):
        self._annotated_text = value

    @property
    def ltmatch_ids(self):
        return self._ltmatch_ids

    @ltmatch_ids.setter
    def ltmatch_ids(self, value):
        self._ltmatch_ids = value

    @property
    def chat(self):
        self._chat = CacheStore.Instance().get_chat_by_id(self.chat_id)
        return self._chat
    
    @chat.setter
    def chat(self, value):
        self._chat = value

    def hasCategory(self, category):
        if category in self.get_error_categories():
            return True
        
        return False

    #TODO: add group functionality 
    def get_recipient(self):
        chat_participants: list = self._chat.participants.copy()
        chat_participants = [p for p in chat_participants if p.id != self._sender.id]

        if len(chat_participants) == 1:
            return chat_participants[0]

        return None
    
    def is_analyzable(self) -> bool:
        if len(self._ltmatch_ids) == 0:
            return False

        return True

    def has_analyzed_errors(self) -> bool:
        if len(self.error_list) == 0:
            return False
        
        return True

    def analyze_errors(self):
        import utils
        utils.analyze_msg_with_language_tool(self)

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.chat_id == other.chat_id and
            self.message_id == other.message_id and
            self.timestamp == other.timestamp
        )

    def __hash__(self):
        return hash((
            self.chat_id,
            self.message_id,
            self.timestamp
        ))
        
    

