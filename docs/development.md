# Developer Guide

There are two different approaches on how to interact with Discord via Discord Proxy:

- DiscordClient
- gRPC

## DiscordClient

`DiscordClient` is a class provided by Discord Proxy which aims to make it easy to interact with Discord in your code. Most of the complexity of the underlying gRPC protocol is hidden behind a simple API.

```eval_rst
.. seealso::
    For the documentation of the DiscordClient class see: :ref:`package:Client`
```

### Client example

Here is a simple example for sending a direct message to a user:

```python
from discordproxy.client import DiscordClient

client = DiscordClient()
client.create_direct_message(user_id=123456789, content="Hello, world!")
```

```eval_rst
.. hint::
    To test this script please replace the user ID with your own. Here is how you can find IDs on your Discord server: `Where can I find my User/Server/Message ID? <https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->`_
```

### Error handling

There are two classes of errors which can occur:

First, errors from the Discord API, e.g. that a user can not be found. These errors will generate a `DiscordProxyHttpError` exception.

Second, errors from the network connection with the Discord Proxy server, e.g. when the server is not up or a timeout occurs. These errors will generate a `DiscordProxyGrpcError` exception.

Both exceptions objects include additional details, e.g. the HTTP error code or the Discord specific JSON error code. Both exceptions are also inherited from `DiscordProxyException`, so for a very simple error handling you can just catch the top level exception.

Here is the same example from before, but now with some rudimentary error handling:

```python
from discordproxy.client import DiscordClient, DiscordProxyException

client = DiscordClient()
try:
    client.create_direct_message(user_id=123456789, content="Hello, world!")
except DiscordProxyException as ex:
    print(f"An error occured when trying to create a message: {ex}")
```

### Timeouts

All requests are synchronous and will usually complete almost instantly. However, sometimes it can take a few seconds longer for a request to complete due to Discord rate limiting, especially if you are running multiple request to Discord in parallel. There also might be issues with the network or the Discord API, which might case requests to go on for a long time (the hard timeout on the client side is about 30 minutes). In order to build a robust application we recommend to use sensible timeouts with all requests. Note that this timeout must cover the complete duration it takes for a request to compete and should therefore not be set too short.

You can define custom timeouts with when instanciating your client. Further, when a timeout occures the specical exception ``DiscordProxyTimeoutError`` will be raised. Here is an example:

```python
from discordproxy.client import DiscordClient, DiscordProxyTimeoutError

client = DiscordClient(timeout=30)  # Defines a timeout of 30 seconds for all methods
try:
    client.create_direct_message(user_id=123456789, content="Hello, world!")
except DiscordProxyTimeoutError as ex:
    # handle timeout
    ...
```

## gRPC

Alternatively you can use the gRPC protocol directly in your code to interact with Discord. This approach is more complex and requires a deeper understanding of gRPC. But it will also give you the most flexibility with full access to all gRPC features.

### gRPC client example

Here is a hello code example for a gRPC client that is sending a direct "hello world" message to a user:

```python
import grpc

from discordproxy.discord_api_pb2 import SendDirectMessageRequest
from discordproxy.discord_api_pb2_grpc import DiscordApiStub

# opens a channel to Discord Proxy
with grpc.insecure_channel("localhost:50051") as channel:
    # create a client for the DiscordApi service
    client = DiscordApiStub(channel)
    # create a request to use the SendDirectMessageRequest method of the service
    request = SendDirectMessageRequest(user_id=123456789, content="Hello, world!")
    # send the request to Discord Proxy
    client.SendDirectMessage(request)

```

```eval_rst
.. hint::
    To test this script please replace the user ID with your own. Here is how you can find IDs on your Discord server: `Where can I find my User/Server/Message ID? <https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->`_
```

### gRPC error handling

If a gRPC request fails a `grpc.RpcError` exception will be raised. RPC errors return the context of the request, consisting of two fields:

- `code`: the [gRPC status code](https://grpc.github.io/grpc/core/md_doc_statuscodes.html)
- `details`: a string with additional details about the error.

The most common errors you can except will be originating from calls to the Discord API. e.g. if a user is no longer a member of the guild the Discord API will return a http response code 404. Discord Proxy will map all HTTP response codes from Discord to a gRPC status codes and raise a gRPC error exceptions (see also [gRPC status codes](#gRPC-status-codes)). In addition the details field of that exception will contain the full error information as JSON object (see also [gRPC details](#gRPC-details)).

#### Code Example

Here is an example on how to catch and process an error exception from your gRPC calls:

```python
try:
    client.SendDirectMessage(request)
except grpc.RpcError as e:
    # print error code and details
    print(f"Code: {e.code()}")
    print(f"Details: {e.details()}")
```

#### gRPC status codes

HTTP response code | gRPC status code
-- | --
400 (BAD REQUEST) | `INVALID_ARGUMENT`
401 (UNAUTHORIZED) | `UNAUTHENTICATED`
403 (FORBIDDEN) | `PERMISSION_DENIED`
404 (NOT FOUND) | `NOT_FOUND`
405 (METHOD NOT ALLOWED) | `INVALID_ARGUMENT`
429 (TOO MANY REQUESTS) | `RESOURCE_EXHAUSTED`
502 (GATEWAY UNAVAILABLE) | `UNAVAILABLE`
504 (GATEWAY TIMEOUT) | `DEADLINE_EXCEEDED`
5xx (SERVER ERROR) | `INTERNAL`

#### gRPC details

The [Discord API](https://discord.com/developers/docs/topics/opcodes-and-status-codes) will return two types of error codes:

- HTTP response code (e.g. 404 if a request user does not exist)
- JSON error code (e.g. 30007 when the maximum number of webhooks is reached )

In addition the response may contain some additional error text. All that information will be encoded as JSON in the details attribute of the gRPC error exception. Here is an example:

```json
{
    "type": "HTTPException",
    "status": 403,
    "code": 50001,
    "text": "Missing Access"
}
```

Legend:

- `status`: HTTP status code
- `code`: JSON error code
- `text`: Error message

```eval_rst
.. note::
    For most cases it should be sufficient to deal with the status code. The JSON error code is only needed in some special cases.
```

To simplify dealing with the JSON error objects you can also use this helper from the djangoproxy package, which will parse the details and return them as handy named tuple:

```python
from discordproxy.helpers import parse_error_details

try:
    client.SendDirectMessage(request)
except grpc.RpcError as e:
    details = parse_error_details(e)
    print(f"HTTP response code: {details.status}")
    print(f"JSON error code: {details.code}")
    print(f"Discord error message: {details.text}")
```

```eval_rst
.. seealso::
    For the documentation of all helpers see: :ref:`package:Helpers`
```

### gRPC timeouts

Here is how to use timeout with requests to the Discord Proxy. All timeouts are in seconds:

```Python
try:
    client.SendDirectMessage(request, timeout=10)
except grpc.RpcError as e:
    # handle timeouts
```

Should a timeout be triggered the client will receive a `grpc.RpcError` with status code `DEADLINE_EXCEEDED`.

## Rate limiting

The Discord API is imposing rate limiting to all requests. Discord Proxy will automatically adhere to those rate limits by suspending a request until it can be sent. This can in certain situations result in requests taking a longer time to complete. If you need to complete your Discord request within a certain time, please see the sections about how to set custom timeouts.
