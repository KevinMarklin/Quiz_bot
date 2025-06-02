from typing import Callable, Dict, Any, Awaitable
from lock_state import is_locked
import toml
from aiogram import BaseMiddleware
from aiogram.types import Message

config = toml.load("config.toml")
ADMIN_IDS = config["support"]["id1"]



class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id in ADMIN_IDS:
            return await handler(event, data)

        if is_locked():
            await event.answer("⛔ Доступ ограничен. Бот находится на тех.обслуживание\n"
                               "Оповестим, когда всё заработает")
            return

        return await handler(event, data)
