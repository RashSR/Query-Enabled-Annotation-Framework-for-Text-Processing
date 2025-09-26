from .messagetype import MessageType
from mainFlask.data.cachestore import CacheStore
from .ltmatch import LTMatch
from .spacymatch import SpacyMatch
from .message_token import MessageToken
from .annotation import Annotation
import re

class Message:
    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = MessageType.TEXT, quoted_message = None, chat = None):
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
        self._chat = chat
        self._search_results = []
        self._message_tokens: list[MessageToken] = []
        self._annotations: list[Annotation] = []

    def __str__(self):
        return (
            f"ChatId: {getattr(self, 'chat_id', None)}\n"
            f"MessageId: {getattr(self, '_message_id', None)}\n"
            f"Sender: {getattr(getattr(self, 'sender', None), 'name', None)}\n"
            f"Timestamp: {getattr(self, 'timestamp', None)}\n"
            f"Content: {getattr(self, 'content', None)}\n"
            f"MessageType: {getattr(self, 'message_type', None)}\n"
            f"quotedMessage: {{ {getattr(self, 'quoted_message', None)} }}\n"
            f"ErrorTypes: {len(getattr(self, 'error_list', []) or [])}\n"
            f"LinguisticAttributes: {len(getattr(self, 'spacy_matches', []) or [])}\n"
            f"ManualAnnotations: {len(getattr(self, 'annotations', []) or [])}\n"
        )

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
        self._error_list = sorted(
            CacheStore.Instance().get_all_ltms_by_msg_id_and_chat_id(self._message_id, self.chat_id),
            key=lambda err: (err.start_pos, err.end_pos)
        )
        return self._error_list

    @error_list.setter
    def error_list(self, value: list[LTMatch]):
        self._error_list = value

    @property
    def spacy_matches(self) -> list[SpacyMatch]:
        self._spacy_matches = CacheStore.Instance().get_all_spacy_matches_by_msg_id(self._message_id)
        self._spacy_matches = sorted(
            CacheStore.Instance().get_all_spacy_matches_by_msg_id(self._message_id),
            key=lambda sm: (sm.start_pos, sm.end_pos)
        )
        return self._spacy_matches
    
    @spacy_matches.setter
    def spacy_matches(self, value: list[SpacyMatch]):
        self._spacy_matches = value

    @property
    def annotations(self) -> list[Annotation]:
        self._annotations = sorted(
            CacheStore.Instance().get_all_annotations_by_msg_id(self._message_id),
            key=lambda ann: (ann.start_pos, ann.end_pos)
        )
        return self._annotations
    
    @annotations.setter
    def annotations(self, value: list[Annotation]):
        self._annotations = value

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
        output = ""
        open_lt_matches = []
        open_annotations = []   

        for i, token in enumerate(self.message_tokens):
            token_start = token.start_pos

            # Close LT matches that ended before this token
            to_close_lt = [lt for lt in open_lt_matches if lt.end_pos <= token_start]
            for lt in to_close_lt:
                output += "</span>"
                open_lt_matches.remove(lt)

            # Close annotations that ended before this token
            to_close_ann = [ann for ann in open_annotations if ann.end_pos <= token_start]
            for ann in to_close_ann:
                output += "</span>"
                open_annotations.remove(ann)

            # Open LT matches starting at this token
            for lt in token.lt_matches:
                if lt not in open_lt_matches:
                    output += f"<span data-error='{lt.category}' data-id='{lt.id}'>"
                    open_lt_matches.append(lt)

            # Open annotations starting at this token
            for ann in token.annotations:
                if ann not in open_annotations:
                    output += f"<span annotation='{ann.reason}' data-id='{ann.id}'>"
                    open_annotations.append(ann)

            # Always wrap the token with its spacy_match
            if token.spacy_match is None:
                token_html = f"<span class='EMPTY'>{token.text}</span>"
            else:
                token_html = f"<span part-of-speech='{token.spacy_match.pos}' data-id='{token.spacy_match.id}'>{token.spacy_match.text}</span>"

            output += token_html

            if i < len(self.message_tokens) - 1:
                output += " "

        # Close any remaining open spans in reverse order to maintain proper nesting
        while open_annotations:
            open_annotations.pop()
            output += "</span>"
        while open_lt_matches:
            open_lt_matches.pop()
            output += "</span>"
        
        return output


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
    
    #one token can have more than one annotation
    def _find_annotations_by_start_and_end_index(self, start, end) -> list[Annotation]:
        annos: list[Annotation] = []
        for anno in self.annotations:
            if start >= anno.start_pos and end <= anno.end_pos:
                annos.append(anno)
        
        return annos

    #only returns one, because all information are coded in on spacy match
    def _find_spacy_match_by_start_and_end_index(self, start, end) -> SpacyMatch:
        for sm in self.spacy_matches:
            if sm.start_pos == start and sm.end_pos == end:
                return sm

    def tokenize_with_positions(self):
        # decimals first, then emoticons, then words, then any other non-space char
        pattern = r"\d+(?:\.\d+)?|[:;8xX=][-^]?[)DPOp]|\w+|[^\w\s]"
        tokens = []
        for match in re.finditer(pattern, self.content):
            start = match.start()
            end = match.end()
            token_text = match.group()
            sm = self._find_spacy_match_by_start_and_end_index(start, end)
            ltms = self._find_lt_matches_by_start_and_end_index(start, end)
            annos = self._find_annotations_by_start_and_end_index(start, end)
            mt = MessageToken(start, end, token_text, sm, ltms, annos)
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
                    if loop_index - first_flagged_token_index > token_range:  #TODO: add direction of range
                        return False

        if first_flagged_token_index is None:
            return False

        return True
        
    def set_found_flag_for_token(self, startPos: int, endPos: int):
        for token in self.message_tokens:
            if startPos >= token.start_pos and endPos <= token.end_pos:
                token.is_flagged = True

