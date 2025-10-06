from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import texts


class BlockCommandInStateMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data['state']
        current_state = await state.get_state()
        
        if (
            current_state is not None 
            and event.text 
            and event.text.startswith('/')
        ):
            await event.answer(text=texts['en']['command_off'])
            return
        
        return await handler(event, data)