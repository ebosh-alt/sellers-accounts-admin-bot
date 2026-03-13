import base64
import hashlib
import hmac
import time
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.config import config


class Builder:
    @staticmethod
    def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        if type(name_buttons) is list:
            for name_button in name_buttons:
                keyboard.button(text=name_button, callback_data=name_button)
        elif type(name_buttons) is dict:
            for name_button in name_buttons:
                if "http" in name_buttons[name_button] or "@" in name_buttons[name_button]:
                    keyboard.button(text=name_button, url=name_buttons[name_button])
                else:
                    keyboard.button(text=name_button, callback_data=name_buttons[name_button])

        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


# todo: добавить историю сделок для менеджера в веб
class Keyboards:
    _MANAGER_PANEL_TOKEN_TTL = 60 * 60  # 1 hour

    @classmethod
    def admin_menu_kb(cls, user_id):
        kb = Builder.create_keyboard(
            {
                "Работа с каталогом": cls._manager_panel_link(user_id),
                "Отменить покупку": "cancel_buy",
                "Просмотреть сделки": "show_deals",
                "Просмотреть инфо продавца": "show_seller_info",
                "Изменить баланс": "change_balance",
                "Изменить реквизиты продавца": "change_seller_wallet",
                "Изменить название магазина": "change_name_shop",
                "Изменить описание продавца": "change_description_seller",
                "Изменить фото магазина": "change_photo_shop",
                "Добавить тип аккаунтов": "add_acc_type",
                "Удалить тип аккаунтов": "delete_acc_type",
            }
        )
        return kb

    admin_back_menu_kb = Builder.create_keyboard({"Назад": "admin_back_menu"})

    @classmethod
    def _manager_panel_link(cls, user_id: int) -> str:
        """
        Добавляет к базовой ссылке fragment access с HMAC-подписью.
        Токен содержит user_id и время истечения (unix) и живёт 1 час.
        """
        issued_at = int(time.time())
        expires_at = issued_at + cls._MANAGER_PANEL_TOKEN_TTL
        payload = f"{user_id}:{issued_at}:{expires_at}"

        secret = config.project.manager_panel_signing_key.encode()
        signature = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()

        token_bytes = f"{payload}:{signature}".encode()
        token = base64.urlsafe_b64encode(token_bytes).decode().rstrip("=")

        parsed = urlparse(config.project.link_manager_panel)
        fragment = dict(parse_qsl(parsed.fragment))
        fragment["access"] = token

        return urlunparse(parsed._replace(fragment=urlencode(fragment)))

    manager_back_menu_kb = Builder.create_keyboard({"Назад": "manager_back_menu"})
