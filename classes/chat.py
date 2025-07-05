
class Chat:

    #TODO: group chats? -> participants + who is admin, title of group chat, creation date
    #other features -> pinned messages, archived?

    def __init__(self, chat_id, relation = None, group_name = None):
        self._chat_id = chat_id
        self._relation = relation
        self._group_name = group_name
        self._messages = [] # are always loaded
        self._participants = [] #this is always filled
    
    def add_message(self, message):
        self.messages.append(message)
        if all(participant.id != message.sender.id for participant in self.participants):
            self.participants.append(message.sender)

    def show_messages(self):
        for msg in self.messages:
            print(msg)

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    @property
    def relation(self):
        return self._relation

    @relation.setter
    def relation(self, value):
        self._relation = value

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    @property
    def participants(self) -> list:
        return self._participants

    @participants.setter
    def participants(self, value):
        self._participants = value

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    def isGroup(self):
        if self._group_name is None:
            return False
        
        return True

    def get_participant_names(self):
        name_list = []
        for a in self._participants:
            name_list.append(a.name)
        
        return name_list
    
    def get_messages_by_author(self, author):
        messages = []
        for msg in self._messages:
            if msg.sender.id == author.id:
                messages.append(msg)

        return messages
    
    def get_error_rule_ids(self) -> list[str]:
        all_rule_ids = [
            rid
            for msg in self._messages
            for rid in msg.get_error_ruleIds()
        ]
        return sorted(set(all_rule_ids))
    
    def get_error_rule_ids_by_author(self, author) -> list[str]:
        all_rule_ids = [
            rid
            for msg in self.get_messages_by_author(author)
            for rid in msg.get_error_ruleIds()
        ]
        return all_rule_ids

    def get_error_categories(self) -> list[str]:
        all_categories = [
            cid
            for msg in self._messages
            for cid in msg.get_error_categories()
        ]
        return sorted(set(all_categories))
    
    def get_error_categories_by_author(self, author) -> list[str]:
        all_categories = [
            cid
            for msg in self.get_messages_by_author(author)
            for cid in msg.get_error_categories()
        ]
        return all_categories
