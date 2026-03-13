from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from internal.app.app import bot
from internal.service.GetMessage import get_mes
from internal.service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "admin_back_menu")
@router.message(Command("admin"))
@router.message(Command("start"))
async def admin(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    if type(message) is Message:
        await message.answer(text=get_mes("admin"), reply_markup=Keyboards.admin_menu_kb(id))
    else:
        await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text=get_mes("admin"),
            reply_markup=Keyboards.admin_menu_kb(id),
        )


admin_rt = router
