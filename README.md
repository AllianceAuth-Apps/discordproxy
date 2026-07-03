# discordproxy

Proxy server for accessing the Discord API via gRPC

[![release](https://img.shields.io/pypi/v/discordproxy?label=release)](https://pypi.org/project/discordproxy/)
[![python](https://img.shields.io/pypi/pyversions/discordproxy)](https://pypi.org/project/discordproxy/)
[![CI/CD Pipeline](https://github.com/AllianceAuth-Apps/discordproxy/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/AllianceAuth-Apps/discordproxy/actions/workflows/ci-cd.yaml)
[![codecov](https://codecov.io/github/AllianceAuth-Apps/discordproxy/graph/badge.svg?token=MODk6IqJmx)](https://codecov.io/github/AllianceAuth-Apps/discordproxy)
[![Documentation Status](https://readthedocs.org/projects/discordproxy/badge/?version=latest)](https://discordproxy.readthedocs.io/en/latest/?badge=latest)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/AllianceAuth-Apps/discordproxy#MIT-1-ov-file)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Overview

**Discord Proxy** is a proxy server that provides access to the Discord API via gRPC.

The main purpose is to enable applications to use the Discord API without having to implement Discord's websocket protocol. Instead, applications can use the gRPC API and the proxy will resolve all requests with the Discord API server via websockets or HTTP.

Python applications can import the generated gRPC client directly. Applications in other languages can use the protobuf definition to generate their own gRPC client.

## Documentation

For more information please see the [documentation](https://discordproxy.readthedocs.io/en/latest/?badge=latest).
