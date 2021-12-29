import argparse
import asyncio
import functools
import logging
import signal
import sys
import traceback

import discord
import grpc
from discord.errors import ClientException

from discordproxy import __title__, __version__
from discordproxy._api import DiscordApi
from discordproxy._config import setup_server
from discordproxy._discord_client import DiscordClient
from discordproxy.discord_api_pb2_grpc import add_DiscordApiServicer_to_server

logger = logging.getLogger(__name__)
discord.VoiceClient.warn_nacl = False


def handle_exception(
    loop, context, server: grpc.aio.server, discord_client: DiscordClient
):
    """Handle all uncaught exceptions raised from tasks."""
    msg = context.get("exception", context["message"])
    if isinstance(msg, Exception):
        traceback_str = "".join(traceback.format_tb(msg.__traceback__))
        logging.error("%s\n%s", msg, traceback_str)
    if isinstance(msg, ClientException):
        logging.critical("Shutting down due to Discord client error: %s", msg)
        asyncio.create_task(
            shutdown_server(server=server, discord_client=discord_client)
        )
    else:
        loop.default_exception_handler(context)


async def shutdown_server(
    server: grpc.aio.server,
    discord_client: DiscordClient,
    signal: signal.Signals = None,
) -> None:
    """Perform a graceful server shutdown."""
    if signal:
        logger.info("Received shutdown signal: %s", signal)
    logger.info("Logging out from Discord...")
    await discord_client.close()
    logger.info("Shutting down gRPC service...")
    await server.stop(0)


async def run_server(
    token: str,
    my_args: argparse.Namespace,
    server: grpc.aio.server = None,
    discord_client: DiscordClient = None,
) -> None:
    """Run the server until it is shutdown."""
    # init server
    if not server:
        server = grpc.aio.server()
    if not discord_client:
        discord_client = DiscordClient()
    add_DiscordApiServicer_to_server(DiscordApi(discord_client), server)
    listen_addr = f"{my_args.host}:{my_args.port}"
    server.add_insecure_port(listen_addr)
    # add event handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(shutdown_server(server, discord_client, s)),
        )
    loop.set_exception_handler(
        functools.partial(
            handle_exception, server=server, discord_client=discord_client
        )
    )
    # start the server
    await server.start()
    logger.info("Started gRPC service on %s", listen_addr)
    asyncio.create_task(discord_client.start(token))
    await server.wait_for_termination()
    # server has been shut down
    logger.info("gRPC service has shut down")


def main() -> None:
    """Start up the server."""
    logger.info(f"Starting {__title__} v{__version__}...")
    token, my_args = setup_server(sys.argv[1:])
    asyncio.run(run_server(token=token, my_args=my_args))


if __name__ == "__main__":
    main()
