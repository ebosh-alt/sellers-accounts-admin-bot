from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from internal.app.app import bot
from internal.entities.database import Deal, accounts_data, deals
from internal.entities.states.states import AdminStates
from internal.service.GetMessage import get_mes
from internal.service import SendDeals
from internal.service.keyboards import Keyboards

router = Router()


@router.callback_query(F.data == "show_deals")
async def show_deals(message: CallbackQuery):
    all_data_deals = await deals.get_data_deals()
    if len(all_data_deals) == 0:
        return await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text="Пока ничего нет",
            reply_markup=Keyboards.admin_back_menu_kb,
        )
    return await SendDeals.send(
        message=message,
        all_data_deals=all_data_deals,
        keyboard=Keyboards.admin_menu_kb(message.from_user.id),
    )


@router.callback_query(F.data == "cancel_buy")
async def cancel_buy_start(message: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        chat_id=message.message.chat.id,
        message_id=message.message.message_id,
        text=get_mes("input_DealId_admin"),
        reply_markup=Keyboards.admin_back_menu_kb,
    )
    await state.set_state(AdminStates.cancel_buy)


@router.message(AdminStates.cancel_buy)
async def cancel_buy_end(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if message.text.isdigit():
        deal_id = int(message.text)
        if await deals.in_(deal_id):
            deal: Deal = await deals.get(id=deal_id)
            deal.payment_status = False
            await deals.update(deal)
            reserved_data = await accounts_data.find_by_deal(deal.id)
            for account_data in reserved_data:
                account_data.is_payment = False
                account_data.deal_id = None
                await accounts_data.update(account_data)
            return await message.answer(
                text=get_mes("success_cancel_buy"),
                reply_markup=Keyboards.admin_menu_kb(user_id),
            )

    return await message.answer(
        text=get_mes("err_cancel_buy"),
        reply_markup=Keyboards.admin_menu_kb(user_id),
    )


deals_rt = router
