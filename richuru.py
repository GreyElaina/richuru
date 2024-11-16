import logging
import sys
import types
from datetime import datetime
from logging import LogRecord
from types import TracebackType
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, Union

from loguru import logger
from loguru._logger import Core
from rich.console import Console, ConsoleRenderable
from rich.logging import RichHandler
from rich.text import Text
from rich.theme import Theme

for lv in Core().levels.values():
    logging.addLevelName(lv.no, lv.name)


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())



def highlight(style: str) -> Dict[str, Callable[[Text], Text]]:
    """Add `style` to RichHandler's log text.

    Example:
    ```py
    logger.warning("Sth is happening!", **highlight("red bold"))
    ```
    """

    def highlighter(text: Text) -> Text:
        return Text(text.plain, style=style)

    return {"highlighter": highlighter}


class LoguruRichHandler(RichHandler):
    """
    Interpolate RichHandler in a better way

    Example:

    ```py
    logger.warning("Sth is happening!", style="red bold")
    logger.warning("Sth is happening!", **highlight("red bold"))
    logger.warning("Sth is happening!", alt="[red bold]Sth is happening![/red bold]")
    logger.warning("Sth is happening!", text=Text.from_markup("[red bold]Sth is happening![/red bold]"))
    ```
    """

    def render_message(self, record: LogRecord, message: str) -> "ConsoleRenderable":
        # alternative time log
        time_format = None if self.formatter is None else self.formatter.datefmt
        time_format = time_format or self._log_render.time_format
        log_time = datetime.fromtimestamp(record.created)
        if callable(time_format):
            log_time_display = time_format(log_time)
        else:
            log_time_display = Text(log_time.strftime(time_format))
        if not (log_time_display == self._log_render._last_time and self._log_render.omit_repeated_times):
            self.console.print(log_time_display, style="log.time")
            self._log_render._last_time = log_time_display

        # add extra attrs to record
        extra: dict = getattr(record, "extra", {})
        if "rich" in extra:
            return extra["rich"]
        if "style" in extra:
            record.__dict__.update(highlight(extra["style"]))
        elif "highlighter" in extra:
            setattr(record, "highlighter", extra["highlighter"])
        if "alt" in extra:
            message = extra["alt"]
            setattr(record, "markup", True)
        if "markup" in extra:
            setattr(record, "markup", extra["markup"])
        if "text" in extra:
            setattr(record, "highlighter", lambda _: extra["text"])
        return super().render_message(record, message)


ExceptionHook = Callable[[Type[BaseException], BaseException, Optional[TracebackType]], Any]


def _loguru_exc_hook(typ: Type[BaseException], val: BaseException, tb: Optional[TracebackType]):
    logger.opt(exception=(typ, val, tb)).error("Exception:")


def install(
    rich_console: Optional[Console] = None,
    exc_hook: Optional[ExceptionHook] = _loguru_exc_hook,
    rich_traceback: bool = True,
    tb_ctx_lines: int = 3,
    tb_theme: Optional[str] = None,
    tb_suppress: Iterable[Union[str, types.ModuleType]] = (),
    time_format: Union[str, Callable[[datetime], Text]] = "[%x %X]",
    keywords: Optional[List[str]] = None,
    level: Union[int, str] = 20,
) -> None:
    """Install Rich logging and Loguru exception hook"""
    logging.basicConfig(handlers=[LoguruHandler()], level=0)
    logger.configure(
        handlers=[
            {
                "sink": LoguruRichHandler(
                    console=rich_console
                    or Console(
                        theme=Theme(
                            {
                                "logging.level.success": "green",
                                "logging.level.trace": "bright_black",
                            }
                        )
                    ),
                    rich_tracebacks=rich_traceback,
                    tracebacks_show_locals=True,
                    tracebacks_suppress=tb_suppress,
                    tracebacks_extra_lines=tb_ctx_lines,
                    tracebacks_theme=tb_theme,
                    show_time=False,
                    log_time_format=time_format,
                    keywords=keywords,
                ),
                "format": (lambda _: "{message}") if rich_traceback else "{message}",
                "level": level,
            }
        ]
    )
    if exc_hook is not None:
        sys.excepthook = exc_hook
