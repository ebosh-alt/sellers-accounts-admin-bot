from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import config
from internal.app.app import bot
from internal.entities.database import shops
from internal.entities.states.states import AdminStates
from internal.service.GetMessage import get_mes
from internal.service.keyboards import Keyboards

router = Router()


@router.callback_query(
    F.data.in_(["change_name_shop", "change_photo_shop", "change_description_seller"])
)
async def change_name_shop(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id

    change = message.data
    text = get_mes(change)
    if message.data == "change_name_shop" or message.data == "change_description_seller":
        await state.set_state(AdminStates.change_about_shop)

    elif message.data == "change_photo_shop":
        await state.set_state(AdminStates.change_photo_shop)

    else:
        return await bot.edit_message_text(
            chat_id=id,
            message_id=message.message.message_id,
            text="Произошла ошибка",
            reply_markup=Keyboards.admin_back_menu_kb,
        )
    await state.update_data(message_id=message.message.message_id, change=change)

    return await bot.edit_message_text(
        chat_id=id,
        message_id=message.message.message_id,
        text=text,
        reply_markup=Keyboards.admin_back_menu_kb,
    )


@router.message(AdminStates.change_photo_shop)
async def set_photo_shop(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    file = await bot.get_file(message.photo[-1].file_id)
    path = f"data/{file.file_path.split('/')[1]}"
    await bot.download(file=file, destination=path)
    shop = await shops.get(1)
    shop.path_photo = path
    await shops.update(shop)
    await message.delete()
    kb = None
    if id in config.admin.ids:
        kb = Keyboards.admin_back_menu_kb
    elif id == config.manager.seller_id:
        kb = Keyboards.manager_back_menu_kb

    await bot.edit_message_text(
        chat_id=id, message_id=message_id, text="Параметр обновлен", reply_markup=kb
    )
    await state.clear()


@router.message(AdminStates.change_about_shop)
async def set_name_shop(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    change = data["change"]
    text = message.text
    kb = None
    shop = await shops.get(1)
    if id in config.admin.ids:
        kb = Keyboards.admin_back_menu_kb
    elif id == config.manager.seller_id:
        kb = Keyboards.manager_back_menu_kb
    if change == "change_name_shop":
        shop.name = text
    elif change == "change_description_seller":
        shop.description = text
    await shops.update(shop)
    await message.delete()

    await bot.edit_message_text(
        chat_id=id, message_id=message_id, text="Параметр обновлен", reply_markup=kb
    )
    await state.clear()


about_shop_rt = router
