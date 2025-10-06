from collections import defaultdict


class MessageMappingManager:
    def __init__(self) -> None:
        self._mapped_messages = defaultdict(dict)
    
    def add_mapping(
        self, 
        peer_id: int, 
        peer_message_id: int, 
        original_message_id
    ) -> None:
        self._mapped_messages[peer_id][peer_message_id] = original_message_id
    
    def get_source_message_id(self, peer_id: int, message_id: int) -> int:
        return self._mapped_messages[peer_id][message_id]
    
    def clear_mapping(self, peer_id: int) -> None:
        self._mapped_messages.pop(peer_id, None)
        