from .queue import UserQueueManager
from .message import MessageMappingManager


class ChatManager:
    def __init__(self) -> None:
        self._active_chattings: dict[int, int] = {}
        self._que_manager = UserQueueManager()
        self._mapping_manager = MessageMappingManager()
    
    @property
    def active_chattings(self) -> dict[int, int]:
        return self._active_chattings
    
    @property
    def que(self) -> UserQueueManager:
        return self._que_manager

    @property
    def mapping(self) -> MessageMappingManager:
        return self._mapping_manager
    
    def search_partner(self) -> int:
        return self._que_manager.pop()
    
    def get_partner(self, peer_id: int) -> int:
        return self._active_chattings[peer_id]
    
    def is_user_chatting(self, peer_id: int) -> bool:
        return peer_id in self._active_chattings
    
    def start_chat(self, peer_id: int, partner_id: int) -> None:
        self._active_chattings[peer_id] = partner_id
        self._active_chattings[partner_id] = peer_id
    
    def end_chat(self, peer_id: int, back_to_que: bool = False) -> None:
        partner_id = self.get_partner(peer_id)
        
        self._active_chattings.pop(peer_id, None)
        self._active_chattings.pop(partner_id, None)
        
        self._mapping_manager.clear_mapping(peer_id)
        self._mapping_manager.clear_mapping(partner_id)
        
        if back_to_que:
            self._que_manager.add(peer_id)
            
        self._que_manager.add(partner_id)
        