"""Module for the commands of the bot."""
from typing import Callable

import re
from logging import Logger

from nio.responses import JoinedMembersError, JoinedMembersResponse
from nio.rooms import MatrixRoom
from nio.events.room_events import Event

import simplematrixbotlib as botlib

from . import Dishwasher, Action

DISHWASHERS = [dw.value for dw in Dishwasher]

COMMAND_HELP = f"""\
This bot only works in unencrypted direct message rooms.

This bot supports the following commands:

help                 Prints this help
start <dishwasher>   Start the given dishwasher
reset <dishwasher>   Reset/Empty the given dishwasher

Valid dishwashers are:

{', '.join(DISHWASHERS[0:4])},
{', '.join(DISHWASHERS[4:])}
"""

UNAUTHORZIED = "You are not authorized to perform this function."

logger = Logger(__name__)


class Commands:
    """Class for the commands of the bot."""

    def __init__(self, bot: botlib.Bot, authorization_room: str, action_handler: Callable[[Dishwasher, Action], None]):
        """
        Initialize the commands class and register all commands.

        This does not register the commands.
        To do that call register_commands.

            Parameters:
                bot(simplematrixbotlib.Bot):
                    The bot to register the commands with.
                authorization_room(str):
                    The room, whoose members are authorized to use the bot.
                action_handler(Callable[[Dishwasher, Action], None]):
                    The callable called with the dishwasher and action when an action needs to be performed
        """
        self.bot = bot
        self.authorization_room = authorization_room
        self.action_handler = action_handler

        # Define and register the commands

        @bot.listener.on_message_event
        async def help(room: MatrixRoom, event: Event):
            """Print help about the bots features."""
            match = botlib.MessageMatch(room, event, bot)

            if self.default_match(match) and match.command("help", case_sensitive=False):
                logger.debug("Responding with help in room %s", room.room_id)
                await self.sendMessage(room, COMMAND_HELP)

        @bot.listener.on_message_event
        async def start(room: MatrixRoom, event: Event):
            """Start a dishwasher."""
            match = botlib.MessageMatch(room, event, bot)
            if match.command("start", case_sensitive=False) and self.default_match(match) and await self.authorized(match):
                logger.debug("Received authorized start command from room %s with args %s", room.room_id, match.args())
                if len(match.args()) == 0:
                    await self.sendMessage(room, "Please supply a dishwasher")
                dishwasher = match.args()[0].lower()
                if dishwasher not in DISHWASHERS:
                    await self.sendMessage(room, f"Unknown dishwasher: {dishwasher}.")
                else:
                    self.action_handler(Dishwasher(dishwasher), Action.START)
                    await self.sendMessage(room, f"Started dishwasher: {dishwasher.capitalize()}.")

        @bot.listener.on_message_event
        async def reset(room: MatrixRoom, event: Event):
            """Reset a dishwasher."""
            match = botlib.MessageMatch(room, event, bot)
            if match.command("reset", case_sensitive=False) and self.default_match(match) and await self.authorized(match):
                logger.debug("Received authorized start command from room %s with args %s", room.room_id, match.args())
                if len(match.args()) == 0:
                    await self.sendMessage(room, "Please supply a dishwasher")
                dishwasher = match.args()[0].lower()
                if dishwasher not in DISHWASHERS:
                    await self.sendMessage(room, f"Unknown dishwasher: {dishwasher}.")
                else:
                    self.action_handler(Dishwasher(dishwasher), Action.RESET)
                    await self.sendMessage(room, f"Reset dishwasher: {dishwasher.capitalize()}.")

    async def _update_allowlist(self):
        res = await self.bot.async_client.joined_members(self.authorization_room)
        if not isinstance(res, JoinedMembersResponse):
            raise Exception("Failed to get joined rooms", res)
        users = res.members
        self.bot.config.allowlist = set([re.compile(re.escape(user.user_id)) for user in users])

    def default_match(self, matcher: botlib.MessageMatch) -> bool:
        """Check if we should answer."""
        if not matcher.is_not_from_this_bot():
            return False
        if matcher.room.member_count > 2:
            return False
        return True

    async def authorized(self, matcher: botlib.MessageMatch) -> bool:
        """Check authorization and inform user if not authorized."""
        try:
            await self._update_allowlist()
        except Exception:
            logger.warn("failed to update allowlist", exc_info=True)

        if matcher.is_from_allowed_user():
            return True

        logger.debug("Authorization failed in room %s for user %s", matcher.room.room_id, matcher.event.sender)
        await self.sendMessage(matcher.room, UNAUTHORZIED)
        return False

    async def sendMessage(self, room: MatrixRoom, msg: str):
        """Send the given message to the given room."""
        await self.bot.api.send_text_message(room.room_id, msg)
