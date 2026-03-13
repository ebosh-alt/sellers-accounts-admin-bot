from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from internal.app.app import bot
from internal.entities.database import sellers
from internal.entities.states.states import AdminStates
from internal.service.GetMessage import get_mes
from internal.service.keyboards import Keyboards
from misc.is_float import is_float

router = Router()


@router.callback_query(F.data == "change_balance")
async def admin(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=get_mes("change_balance"),
        reply_markup=Keyboards.admin_back_menu_kb,
    )
    await state.set_state(AdminStates.change_balance)
    await state.update_data(message_id=message.message.message_id)


@router.message(AdminStates.change_balance)
async def change_balance(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    await message.delete()
    if is_float(message.text):
        seller = await sellers.get()
        seller.balance -= float(message.text)
        await sellers.update(seller)
        await bot.edit_message_text(
            chat_id=id,
            message_id=message_id,
            text=get_mes("change_balance_complete"),
            reply_markup=Keyboards.admin_menu_kb(id),
        )
        await state.clear()
    else:
        await bot.edit_message_text(
            chat_id=id,
            message_id=message_id,
            text=get_mes("change_balance_err"),
            reply_markup=Keyboards.admin_menu_kb(id),
        )


balance_rt = router
