from typing import Iterable

import grpc

from .discord_api_pb2 import (
    Channel,
    Embed,
    GetGuildChannelsRequest,
    Message,
    SendChannelMessageRequest,
    SendDirectMessageRequest,
)
from .discord_api_pb2_grpc import DiscordApiStub
from .exceptions import to_discord_proxy_exception


class DiscordClient:
    """Client for interacting with Discord.

    All methods raise either ``DiscordProxyHttpError`` or ``DiscordProxyGrpcError``.
    """

    def __init__(self, target: str = None, options=None) -> None:
        """
        Args:
            target: The server address. Default is: "localhost:50051"
            options: An optional list of key-value pairs to configure the channel.
        """
        self.target = str(target) if target else "localhost:50051"
        self.options = options

    def get_guild_channels(self, guild_id: int) -> Iterable[Channel]:
        """Get all channels.

        Args:
            guild_id: ID of guild to get the channel for

        Returns:
            Guild channels
        """
        with grpc.insecure_channel(self.target, self.options) as channel:
            client = DiscordApiStub(channel)
            request = GetGuildChannelsRequest(guild_id=guild_id)
            try:
                response = client.GetGuildChannels(request)
            except Exception as ex:
                raise to_discord_proxy_exception(ex)
        return response.channels

    def create_channel_message(
        self, channel_id: int, content: str = "", embed: Embed = None
    ) -> Message:
        """Create new message in a channel.

        Args:
            channel_id: ID of channel to create message in
            content: Text of the message
            embed: Embed of the message

        Returns:
            Created message
        """
        if not content and not embed:
            raise ValueError("Either content or embed need to be specified.")
        with grpc.insecure_channel(self.target, self.options) as grpc_channel:
            client = DiscordApiStub(grpc_channel)
            request = SendChannelMessageRequest(
                content=content, channel_id=channel_id, embed=embed
            )
            try:
                response = client.SendChannelMessage(request)
            except Exception as ex:
                raise to_discord_proxy_exception(ex)
        return response.message

    def create_direct_message(
        self, user_id: int, content: str = "", embed: Embed = None
    ) -> Message:
        """Create new direct message.

        Args:
            user_id: ID of user to create direct message for
            content: Text of the message
            embed: Embed of the message

        Returns:
            Created message
        """
        if not content and not embed:
            raise ValueError("Either content or embed need to be specified.")
        with grpc.insecure_channel(self.target, self.options) as grpc_channel:
            client = DiscordApiStub(grpc_channel)
            request = SendDirectMessageRequest(
                content=content, user_id=user_id, embed=embed
            )
            try:
                response = client.SendDirectMessage(request)
            except Exception as ex:
                raise to_discord_proxy_exception(ex)
        return response.message
