import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    """Bridge standard Python logging into Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        # Convert the Python logging level name (for example, "INFO") into the
        # equivalent Loguru level. If Loguru does not recognize it, fall back to
        # the numeric level from the original record.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Walk up the call stack until we leave Python's logging internals. This
        # makes Loguru report the real source file/line of the application code
        # that emitted the log record instead of the logging framework itself.
        frame, depth = logging.currentframe(), 2
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Preserve the original exception metadata and send the message through
        # Loguru with the correct level and stack depth.
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
