# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

### Added

### Changed

### Fixed

## [0.4.0] - 2021-12-27

### Added

- New client class `DiscordClient` providing a simple API for interacting with Discord as alternative to the more complex gRPC protocol.

### Changed

- Renamed modules that constitue the server and should not be imported by client code to show they are private

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
