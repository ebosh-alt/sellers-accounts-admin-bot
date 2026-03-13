from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from internal.app.app import bot
from internal.entities.database import Category, categories
from internal.entities.states.states import AdminStates
from internal.service.GetMessage import get_mes
from internal.service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "add_acc_type")
async def add_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.enter_new_acc_type)
    acceptable_account_names = await categories.get_names()
    await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=get_mes("add_acc_type_1", acc_types=acceptable_account_names),
        reply_markup=Keyboards.admin_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.update_data(message_id=message.message.message_id)


@router.message(AdminStates.enter_new_acc_type)
async def add_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data.get("message_id")
    acceptable_account_names = await categories.get_names()

    if message.text in acceptable_account_names:
        pass
    else:
        await categories.new(Category(name=message.text))
    acceptable_account_names = await categories.get_names()
    await message.delete()
    await state.clear()
    await bot.edit_message_text(
        chat_id=id,
        message_id=message_id,
        text=get_mes("add_acc_type_success", acc_types=acceptable_account_names),
        reply_markup=Keyboards.admin_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data == "delete_acc_type")
async def delete_acc_type(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.enter_acc_type_to_del)
    acceptable_account_names = await categories.get_names()

    await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=get_mes("delete_acc_type_1", acc_types=acceptable_account_names),
        reply_markup=Keyboards.admin_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.update_data(message_id=message.message.message_id)


@router.message(AdminStates.enter_acc_type_to_del)
async def delete_acc_type_enter(message: Message, state: FSMContext):
    id = message.from_user.id
    acceptable_account_names = await categories.get_names()
    data = await state.get_data()
    message_id = data.get("message_id")
    await message.delete()
    if message.text in acceptable_account_names:
        acceptable = await categories.get_by_name(message.text)
        await categories.delete(acceptable)
    else:
        pass
    acceptable_account_names = await categories.get_names()

    await state.clear()
    await bot.edit_message_text(
        chat_id=id,
        message_id=message_id,
        text=get_mes("delete_acc_type_success", acc_types=acceptable_account_names),
        reply_markup=Keyboards.admin_back_menu_kb,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


acc_types_rt = router
