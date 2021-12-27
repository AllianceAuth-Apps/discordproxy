import json

import grpc

from ..discord_api_pb2 import Channel


def id_generator() -> int:
    seed = 1
    while True:
        yield seed
        seed += 1


unique_ids = id_generator()


def create_discordproxy_channel(**kwargs) -> Channel:
    if "id" not in kwargs:
        kwargs["id"] = next(unique_ids)
    if "type" not in kwargs:
        kwargs["type"] = Channel.Type.GUILD_TEXT
    return Channel(**kwargs)


def create_rpc_error():
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.NOT_FOUND
    error.details = lambda: json.dumps(
        {
            "type": "HTTPException",
            "status": 404,
            "code": 50001,
            "text": "User not found",
        }
    )
    return error
