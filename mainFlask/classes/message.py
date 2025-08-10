from .messagetype import MessageType
from mainFlask.data.cachestore import CacheStore
from .ltmatch import LTMatch
from .spacymatch import SpacyMatch
from .message_token import MessageToken
import re

#TODO:  Klasse e.g. message_element und hier wird jedes einzelne Element aus einer Nachricht erstellt hinzu kommen eine Liste an lt_matches und spacy_matches hinzu. 
# Diese können beim annotieren bearbeitet werden
# Für aufeinanderfolgende Suche praktisch -> iteriere über alle und falls zwei hintereinander richtig sind -> hinzufügen

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
        self._spacy_match_ids = []
        self._spacy_matches: list[SpacyMatch] = []
        self._annotated_text = annotated_text
        self._chat = chat
        self._search_results = []
        self._message_tokens: list[MessageToken] = []

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
        self.error_list.append(error)

    #improves performance with seen. from WC O(n²) to O(n)
    def get_error_ruleIds(self) -> list[str]:
        seen = set()
        rule_ids = []

        for ltm in self.error_list:
            rid = ltm.rule_id
            if rid not in seen: #because this is O(1) in avg case
                seen.add(rid)
                rule_ids.append(rid)

        
        return rule_ids
    
    #improves performance with seen. from WC O(n²) to O(n)
    def get_error_categories(self) -> list[str]:
        seen = set()
        category_ids = []

        for ltm in self.error_list:
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
    def error_list(self, value: list[LTMatch]):
        self._error_list = value

    @property
    def spacy_matches(self) -> list[SpacyMatch]:
        if len(self._spacy_matches)==0: #TODO only load errorlist once
            self._spacy_matches = CacheStore.Instance().get_all_spacy_matches_by_msg_id(self._message_id)
        return self._spacy_matches
    
    @spacy_matches.setter
    def spacy_matches(self, value: list[SpacyMatch]):
        self._spacy_matches = value

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
    def spacy_match_ids(self):
        return self._spacy_match_ids

    @spacy_match_ids.setter
    def spacy_match_ids(self, value):
        self._spacy_match_ids = value

    @property
    def chat(self):
        self._chat = CacheStore.Instance().get_chat_by_id(self.chat_id)
        return self._chat
    
    @chat.setter
    def chat(self, value):
        self._chat = value

    @property
    def search_results(self):
        return self._search_results
    
    @search_results.setter
    def search_results(self, value):
        self._search_results = value

    @property
    def message_tokens(self) ->list[MessageToken]:
        #check if dictionary is already created
        if len(self._message_tokens) == 0:
            self.message_tokens = self.tokenize_with_positions()
        return self._message_tokens
    
    @message_tokens.setter
    def message_tokens(self, value: list[MessageToken]):
        self._message_tokens = value

    #one token can have more than one ltmatch
    def _find_lt_matches_by_start_and_end_index(self, start, end) -> list[LTMatch]:
        ltms: list[LTMatch] = []
        for lt in self.error_list:
            if start >= lt.start_pos and end <= lt.end_pos:
                ltms.append(lt)
        
        return ltms

    #only returns one, because all information are coded in on spacy match
    def _find_spacy_match_by_start_and_end_index(self, start, end) -> SpacyMatch:
        for sm in self.spacy_matches:
            if sm.start_pos == start and sm.end_pos == end:
                return sm

    def tokenize_with_positions(self):
        pattern = r"\w+|[:;8xX=][-^]?[)DPOp]|[^\w\s]"
        tokens = []
        for match in re.finditer(pattern, self.content):
            start = match.start()
            end = match.end()
            token_text = match.group()
            sm = self._find_spacy_match_by_start_and_end_index(start, end)
            ltms = self._find_lt_matches_by_start_and_end_index(start, end)
            mt = MessageToken(start, end, token_text, sm, ltms)
            tokens.append(mt)
        return tokens

    def hasCategory(self, category):
        if category in self.get_error_categories():
            return True
        
        return False
    
    def hasRuleId(self, rule_id):
        if rule_id in self.get_error_ruleIds():
            return True
        
        return False

    #TODO: add group functionality 
    def get_recipient(self):
        chat_participants: list = self.chat.participants.copy()
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
    
    def hasTokensWithinRange(self, token_range: int) -> bool:
        first_flagged_token_index = None
        for loop_index, token in enumerate(self.message_tokens):
            if token.is_flagged:
                if first_flagged_token_index is None:
                    first_flagged_token_index = loop_index
                else: #check if the next found token is in range
                    if loop_index - first_flagged_token_index > token_range:
                        return False
                    
        return True;
        
    def set_found_flag_for_token(self, startPos: int, endPos: int):
        for token in self.message_tokens:
            if startPos >= token.start_pos and endPos <= token.end_pos:
                token.is_flagged = True
                break

