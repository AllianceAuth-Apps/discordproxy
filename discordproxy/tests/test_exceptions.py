import json
from unittest import TestCase

import grpc

from ..exceptions import (
    DiscordProxyGrpcError,
    DiscordProxyHttpError,
    to_discord_proxy_exception,
)


class TestToDiscordProxyException(TestCase):
    def test_should_return_other_exceptions(self):
        # when
        result = to_discord_proxy_exception(OSError)
        # then
        self.assertIs(result, OSError)

    def test_should_return_http_exception(self):
        # given
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
        # when
        result = to_discord_proxy_exception(error)
        # then
        self.assertIsInstance(result, DiscordProxyHttpError)
        self.assertEqual(result.status, 404)
        self.assertEqual(result.code, 50001)
        self.assertEqual(result.text, "User not found")

    def test_should_return_grpc_exception(self):
        # given
        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.ABORTED
        error.details = lambda: "text"
        # when
        # when
        result = to_discord_proxy_exception(error)
        # then
        self.assertIsInstance(result, DiscordProxyGrpcError)
        self.assertIs(result.status, grpc.StatusCode.ABORTED)
        self.assertEqual(result.details, "text")


class TestDiscordProxyHttpError(TestCase):
    def test_str(self):
        # given
        ex = DiscordProxyHttpError(status=404, code=50001, text="User not found")
        # when
        self.assertEqual(
            str(ex),
            (
                "HTTP error from the Discord API. HTTP status code: 404 - "
                "JSON error code: 50001 - Error message: User not found"
            ),
        )


class TestDiscordProxyGrpcError(TestCase):
    def test_str(self):
        # given
        ex = DiscordProxyGrpcError(status=grpc.StatusCode.ABORTED, details="some text")
        # when
        self.assertEqual(
            str(ex), ("gRPC error. Status code: ABORTED - Error message: some text")
        )
