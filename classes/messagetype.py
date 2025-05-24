from enum import Enum

class MessageType(Enum):
    TEXT = "Text"
    IMAGE = "Image"
    VIDEO = "Video"
    AUDIO = "Audio"
    DOCUMENT = "Document"
    CONTACT = "Contact"
    LOCATION = "Location"
    STICKER = "Sticker"
    LINK = "Link"
    REACTION = "Reaction"
    CALL_LOG = "CallLog"
    SYSTEM = "System"  # e.g., "Messages are end-to-end encrypted"
    UNKNOWN = "Unknown"
