from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    searching = State()
    chatting = State()