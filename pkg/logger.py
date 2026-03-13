import logging
import sys

from loguru import logger

from config.config import config

logging.getLogger("asyncio.selector_events").setLevel(logging.INFO)

# config = Config.load()

LoggerNameRoot = config.project.name


class InterceptHandler(logging.Handler):
    # @logger.catch(default=True, onerror=lambda _: sys.exit(1))
    def emit(self, record):
        try:
            level = (
                logger.level(record.levelname).name
                if record.levelname in logger._core.levels
                else record.levelno
            )
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger_name = record.name
        log = logger.bind(logger_name=logger_name)
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def serialize(record):
    logger_name = record["extra"].get("logger_name")
    if logger_name is None:
        source = f"{LoggerNameRoot}:{record['name'].replace('.', ':')}:{record['function']}:{record['line']}"
    else:
        source = f"{logger_name}:{record['function']}:{record['line']}"
    record["extra"]["source"] = source
    return {
        "level": record["level"].name if hasattr(record["level"], "name") else str(record["level"]),
        "timestamp": record["time"].isoformat(),
        "source": source,
        "message": record["message"],
    }


def formatter_json(record):
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


def formatter_stdout(record):
    logger_name = record["extra"].get("logger_name")
    if logger_name is None:
        source = f"{LoggerNameRoot}:{record['name'].replace('.', ':')}:{record['function']}:{record['line']}"
    else:
        source = f"{logger_name}:{record['function']}:{record['line']}"
    record["extra"]["source"] = source

    return "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[source]}</cyan> - <level>{message}</level>{exception}\n"


def make_filter(name):
    def filter_looger(record):
        return record["extra"].get("name") == name or name == "*"

    return filter_looger


def set_logger():
    logger.remove(0)
    #
    logger.add(
        sink=sys.stdout,
        format=formatter_stdout,
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
        filter=make_filter("*"),
    )

    # logger.add(
    #     "scheduler.json",
    #     format=formatter_json,
    #     rotation="1 week",
    #     level="INFO",
    #     encoding="utf-8",
    #     filter=make_filter("scheduler_logger"),
    # )
    # logger.add(
    #     "logger.json",
    #     format=formatter_json,
    #     rotation="1 week",
    #     level="INFO",
    #     encoding="utf-8",
    #     filter=make_filter("*"),
    # )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
