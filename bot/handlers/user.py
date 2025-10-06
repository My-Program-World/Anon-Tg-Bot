from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from config import texts
from keyboards import markup, inline
from manager.chat import ChatManager
from state import ChatState
from storage import redis_storage

router = Router(name='user')
chat_manager = ChatManager()

#region Commands
@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer(
        text=texts['en']['welcome'], 
        reply_markup=markup.home
    )


@router.message(F.text == '🔍 Search')
async def search_handler(msg: Message, bot: Bot, state: FSMContext) -> None:
    assert msg.from_user
    
    user_id = msg.from_user.id
    
    if (
        not chat_manager.que.is_user_in_que(user_id)
        and not chat_manager.is_user_chatting(user_id)
    ):
        await msg.answer(
            text=texts['en']['searching_partner'],
            reply_markup=markup.search
        )
        
        if chat_manager.que.has_que():
            partner_id = chat_manager.search_partner()
            
            key = StorageKey(bot.id, partner_id, partner_id)
            partner_state = FSMContext(storage=redis_storage, key=key)
            
            chat_manager.start_chat(user_id, partner_id)
            
            template = texts['en']['partner_searched']
            
            await bot.send_message(
                chat_id=user_id, 
                text=template, 
                reply_markup=markup.chatting
            )
            
            await bot.send_message(
                chat_id=partner_id, 
                text=template, 
                reply_markup=markup.chatting
            )
            
            await state.set_state(ChatState.chatting)
            await partner_state.set_state(ChatState.chatting)
        else:
            chat_manager.que.add(user_id)
            await state.set_state(ChatState.searching)
    else:
        await msg.answer(
            text=texts['en']['already_in_chatting'],
            reply_markup=inline.confirm_keyboard
        )


@router.message(F.text == '🛑 Stop Search')
async def stop_search_handler(msg: Message, state: FSMContext) -> None:
    assert msg.from_user
    
    user_id = msg.from_user.id
    
    if (
        chat_manager.que.is_user_in_que(user_id)
        and not chat_manager.is_user_chatting(user_id)
    ):
        chat_manager.que.kick(user_id)
        
        await state.clear()
        
        await msg.answer(
            text=texts['en']['stoped_search'],
            reply_markup=markup.home
        )


@router.message(F.text == '🚷 Skip')
async def skip_user_handler(msg: Message, bot: Bot, state: FSMContext) -> None:
    assert msg.from_user
    
    user_id = msg.from_user.id
    partner_id = chat_manager.get_partner(user_id)
    
    key = StorageKey(bot.id, partner_id, partner_id)
    partner_state = FSMContext(storage=redis_storage, key=key)
    
    chat_manager.end_chat(peer_id=user_id, back_to_que=True)
    
    await partner_state.clear()
    await partner_state.set_state(ChatState.searching)
    
    await state.clear()
    await state.set_state(ChatState.searching)
    
    await bot.send_message(
        chat_id=partner_id,
        text=texts['en']['you_were_skipped'],
        reply_markup=markup.search
    )
    
    await bot.send_message(
        chat_id=user_id,
        text=texts['en']['user_skipped'],
        reply_markup=markup.search
    )


@router.message(F.text == '🚪 Exit')
async def exit_user_handler(msg: Message, bot: Bot, state: FSMContext) -> None:
    assert msg.from_user
    
    user_id = msg.from_user.id
    partner_id = chat_manager.get_partner(user_id)
    
    key = StorageKey(bot.id, partner_id, partner_id)
    partner_state = FSMContext(storage=redis_storage, key=key)
    
    chat_manager.end_chat(user_id)
    
    await partner_state.clear()
    await partner_state.set_state(ChatState.searching)
    
    await state.clear()
    
    await bot.send_message(
        chat_id=partner_id,
        text=texts['en']['you_were_skipped'],
        reply_markup=markup.search
    )
    
    await bot.send_message(
        chat_id=user_id,
        text=texts['en']['you_exit'],
        reply_markup=markup.home
    )
#endregion

#region States
@router.message(ChatState.chatting)
async def chat_message_handler(msg: Message, bot: Bot) -> None:
    assert msg.from_user 
    
    user_id = msg.from_user.id
    partner_id = chat_manager.get_partner(user_id)
    reply_id: int | None = None
    
    if msg.reply_to_message:
        reply_id = chat_manager.mapping.get_source_message_id(
            user_id, 
            msg.reply_to_message.message_id
        )
    
    match msg.content_type:
        case 'text':
            text = msg.text
            if text:
                partner_msg = await bot.send_message(
                    chat_id=partner_id,
                    text=text,
                    reply_to_message_id=reply_id
                )
        case 'sticker':
            sticker = msg.sticker
            if sticker:
                partner_msg = await bot.send_sticker(
                    chat_id=partner_id,
                    sticker=sticker.file_id,
                    reply_to_message_id=reply_id
                )
        case 'animation':
            animation = msg.animation
            if animation:
                partner_msg = await bot.send_animation(
                    chat_id=partner_id,
                    animation=animation.file_id,
                    reply_to_message_id=reply_id
                )
        case 'voice':
            voice = msg.voice
            if voice:
                partner_msg = await bot.send_voice(
                    chat_id=partner_id,
                    voice=voice.file_id,
                    reply_to_message_id=reply_id
                )
        case 'video_note':
            video_note = msg.video_note
            if video_note:
                partner_msg = await bot.send_video_note(
                    chat_id=partner_id,
                    video_note=video_note.file_id,
                    reply_to_message_id=reply_id
                )
        case 'photo':
            photo = msg.photo
            if photo:
                partner_msg = await bot.send_photo(
                    chat_id=partner_id,
                    photo=photo[-1].file_id,
                    reply_to_message_id=reply_id
                )
        case 'video':
            video = msg.video
            if video:
                partner_msg = await bot.send_video(
                    chat_id=partner_id,
                    video=video.file_id,
                    reply_to_message_id=reply_id
                )
    
    chat_manager.mapping.add_mapping(
        peer_id=user_id,
        peer_message_id=msg.message_id,
        original_message_id=partner_msg.message_id
    )
    
    chat_manager.mapping.add_mapping(
        peer_id=partner_id,
        peer_message_id=partner_msg.message_id,
        original_message_id=msg.message_id
    )
#endregion

#region Callbacks
@router.callback_query(F.data == 'exit_confirm')
async def exit_confirm_handler(
    cb: CallbackQuery, 
    bot: Bot,
    state: FSMContext
) -> None:
    user_id = cb.from_user.id
    
    if chat_manager.is_user_chatting(user_id):        
        partner_id = chat_manager.get_partner(user_id)
        key = StorageKey(bot.id, partner_id, partner_id)
        partner_state = FSMContext(storage=redis_storage, key=key)
        
        await state.clear()
        await partner_state.set_state(ChatState.chatting)
        
        chat_manager.end_chat(user_id)
        
        await bot.send_message(
            chat_id=partner_id, 
            text=texts['en']['user_skipped'],
            reply_markup=markup.search
        )
        
        await bot.send_message(
            chat_id=user_id,
            text=texts['en']['welcome'],
            reply_markup=markup.home
        )


@router.callback_query(F.data == 'exit_cancel')
async def exit_cancel_handler(cb: CallbackQuery, bot: Bot) -> None:
    assert cb.message
    
    await bot.delete_message(
        chat_id=cb.from_user.id, 
        message_id=cb.message.message_id
    )
    