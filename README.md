# Acoustics Media Player (.py)

Acoustics Media Player (aka AMP) is a web-based music indexer and jukebox. AMP's backend was originally written in Perl; this is an API-compatible rewrite in Python. The Python rewrite is slimmer and faster than the original Perl implementation, but lacks several features from the old version.

## Features
- Multiple player support
- Multiple room support
- Multi-user voting with fair queue
- Clean JSON API
- Single-Page-Application client interface
  - Queue reordering
  - Drag+Drop
  - Manage playlists
  - View album art
  - Fullscreen "kiosk" mode
  - Searching

## TODO

- Implement plugin architecture similar to original Perl version.
- Reconfigure for use as a wsgi module.
- Support more authentication methods.
- Add Python packaging metadata.
- Implement remote playback methods.
- Rewrite `build-tagreader.pl` in Python

## License

Acoustics is released under the NCSA / University of Illinois license.

## Authors

Acoustics was originally written by [Adrian Kreher](https://github.com/avuserow), with a handful of other contributors. The current interface and the Python rewrite were both written by [Kevin Lange](https://github.com/klange).
