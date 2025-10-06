from collections import deque
from contextlib import suppress


class UserQueueManager:
    def __init__(self) -> None:
        self._que: deque[int] = deque()

    def add(self, peer_id: int) -> None:
        self._que.append(peer_id)
    
    def pop(self) -> int:
        return self._que.popleft()
    
    def kick(self, peer_id: int) -> None:
        with suppress(ValueError):
            self._que.remove(peer_id)
        
    def is_user_in_que(self, peer_id: int) -> bool:
        return peer_id in self._que
        
    def has_que(self) -> bool:
        return len(self._que) > 0
    
    def __len__(self) -> int:
        return len(self._que)