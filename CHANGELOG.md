# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

## [1.3.2] - 2024-05-10

### Changed

- Added read-only properties to DiscordClient to enable testing of the current configuration
- Added AA4 docker config to documentation

## [1.3.1] - 2023-08-01

### Changed

- Moved tests folder into main package, so it's factories are available for other apps
- Added mandatory pylint checks
- Refactored

## [1.3.0] - 2023-06-22

### Added

### Changed

- Dropped support for Python 3.7
- Migrated to PEP 621
- Removed support for Pycord 1.x
- Added support for Python 3.11

### Fixed

- SendChannelMessage: Unexpected exception: 'NoneType' object has no attribute 'key':

## [1.2.2] - 2022-06-18

### Changed

- Automatic dark and light mode for Sphinx docs
- Add wheel to PyPI deployment

## [1.2.1] - 2022-06-02

### Changed

- Add pycord 2 to CI pipeline
- Refactor pycord API adaptor
- Removed `Channel.Type.GUILD_STORE` since it is no longer supported by the API

## [1.2.0] - 2022-06-02

### Added

- Added experimental support for py-cord 2.0, which currently is in beta. This means that Discord Proxy now works with both py-cord 1.7 and py-cord 2.0. While this has not been tested explicitely, this should resolve the conflict with allianceauth-discordbot 3. (#1)

## [1.1.0] - 2022-04-08

### Added

- Ability to specify port and host when using the **discordproxymessage** tool

## [1.0.1] - 2022-04-05

### Fixed

- Excluding grpcio-tools v1.45.0 as dependency, which in turn has a broken dependecy

Thanks to @ppfeufer for the contribution!

## [1.0.0] - 2022-02-04

>**Important update notes**<br>When upgrading from a previous version you need to uninstall discord.py **before** installing this new version, e.g. by running `pip uninstall discord.py`

## Changed

- Now using py-cord instead of the no longer maintained discord.py library. This should reduce conflicts with the new version for the aa-discordbot.
- Added support for Python 3.10

## [0.5.0] - 2022-01-12

### Added

- Tool for sending messages from the command line

## [0.4.1] - 2021-12-29

### Changed

- Include tests in destribution package

## [0.4.0] - 2021-12-29

### Added

- New client class `DiscordClient` provides a simple API for interacting with Discord as alternative to the more complex gRPC protocol.

### Changed

- Renamed modules that constitute the server to show they are private and should not be imported by client code

### Fixed

- Server keeps running after an unrecoverably Discord client exception occurs, e.g. login failed due to invalid token

## [0.3.0] - 2021-12-26

### Added

- Added more fields to the `Channel` object, e.g. `parent_id` to identify the category of a channel

## [0.2.2] - 2021-11-17

### Changed

- Minimimum Python version extented to include 3.7 due to dependency with discord.py
- Log gRPC message content on DEBUG level, not INFO
- All HTTP exceptions will be logged as WARNING

## [0.2.1] - 2021-11-16

### Changed

- Update deprecated code to remove deprecation warning from Discord Client / logout
- Remove backport of asyncio.run for 3.6

### Fixed

- Does not show listen address in log

## [0.2.0] - 2021-11-16

### Changed

- Minimimum Python version bumped up to 3.8 due to dependency with discord.py
- Added isort to pre-commit checks

## [0.1.0] - 2021-05-24

### Added

- Initial stable release

## [0.1.0b1] - 2021-03-13

### Added

- Initial BETA release
