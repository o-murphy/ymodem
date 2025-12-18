try:
    try:
        from importlib.metadata import metadata, PackageNotFoundError
    except ImportError:
        from importlib_metadata import metadata, PackageNotFoundError

    __version__ = metadata("ymodem")["Version"]
except PackageNotFoundError:
    __version__ = "unknown"
