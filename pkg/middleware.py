from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import TelegramObject
from loguru import logger

from config.config import config


class Logging:
    """middleware для человекочитаемых логов входящих событий."""

    @staticmethod
    def auth(user_id: int) -> bool:
        return user_id in config.admin.ids or user_id == config.admin.main_id

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
        ) -> Any:
        try:
            payload_type, user_name, user_id, _payload_text = self._extract(event)

            if payload_type:
                logger.info(f"{user_name} ({user_id}) | {payload_type}")
            if user_id is None or not self.auth(user_id):
                return None
            return await handler(event, data)
        except Exception as e:
            logger.exception("Logging middleware error on %s\n%s", type(event).__name__, e)
            return None

    def _extract(
            self, event: TelegramObject
    ) -> tuple[str | None, str | None, int | None, str | None]:
        if getattr(event, "message", None):
            name, user_id = self._format_user(event.message.from_user)  # noqa
            text = getattr(event.message, "text", None) or "<no text>"  # noqa
            return "message", name, user_id, text

        if getattr(event, "callback_query", None):
            name, user_id = self._format_user(event.callback_query.from_user)  # noqa
            data = event.callback_query.data or "<no data>"  # noqa
            return "callback_query", name, user_id, data

        return None, None, None, None

    def _format_user(self, user) -> list[str | int]:  # noqa
        username = user.username
        name = f"@{username}" if username else (user.first_name or "unknown")
        return [name, user.id]

