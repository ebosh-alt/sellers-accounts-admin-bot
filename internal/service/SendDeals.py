from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from internal.app.app import bot
from internal.entities.models import DataDeals
from internal.service.GetMessage import get_mes, rounding_numbers

MAX_MSG_LEN = 3800


def _format_deal(deal: DataDeals) -> DataDeals:
    return deal.model_copy(update={"price": rounding_numbers(str(deal.price))})


def _build_text(deals: list[DataDeals]) -> str:
    return get_mes("history_buy", deals=deals)


async def send(message: CallbackQuery, all_data_deals: list[DataDeals], keyboard):
    """service.GetMessage.get_mes() использует в качестве аргумента fmes_text_path\n
    fmes_text_path - название файла .md\n
    get_mes(fmes_text_path)"""
    batch: list[DataDeals] = []
    batch_text = ""
    msg = None
    if len(all_data_deals) == 0:
        await message.answer("У вас ещё нет совершенных сделок")
        return

    for data_deal in all_data_deals:
        # formatted = _format_deal(data_deal)
        candidate = batch + [data_deal]
        candidate_text = _build_text(candidate)

        if len(candidate_text) <= MAX_MSG_LEN:
            batch = candidate
            batch_text = candidate_text
            continue

        if batch:
            await bot.send_message(
                chat_id=message.message.chat.id,
                text=batch_text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            batch = [data_deal]
            batch_text = _build_text(batch)
        else:
            msg = await bot.send_message(
                chat_id=message.message.chat.id,
                text=candidate_text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            batch = []
            batch_text = ""

    if batch:
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=batch_text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif msg:
        await bot.edit_message_reply_markup(
            chat_id=message.message.chat.id,
            message_id=msg.message_id,
            reply_markup=keyboard,
        )
