# richuru - 在 Loguru 中使用 Rich 为日志增色

简体中文 | [English](README.md)

richuru 是一个轻量级的依赖, 为 [`loguru`](https://github.com/Delgan/loguru) 提供 [`rich`](https://github.com/willmcgugan/rich) 强大的终端渲染支持。

本项目来源并独立自 [`Graia Amnesia`](https://github.com/GraiaProject/Amnesia) 的组件 `graia.amnesia.log`,
且由 @BlueGlassBlock 的原始实现修改而成。

# Quick Start

安装 `richuru`:

```bash
elaina@localhost $ pip install richuru

elaina@localhost $ pdm add richuru

elaina@localhost $ poetry add richuru
```

在 REPL 内试用:

```
>>> import richuru
>>> richuru.install()
>>>
>>> from loguru import logger
>>> logger.info("Hello World!", alt="Hello, [bold magenta]World[/bold magenta]!")
```

`richuru` 被设计为一个可选依赖, 这意味着在使用 `richuru` 时你需要尽可能的提供回退模式(fallback pattern), 以兼容未启用 `richuru` 的终端用户.

在 `logger.<method>(...)` 时提供 `alt` 选项即可使 `richuru` 识别并启用 `rich` 的富文本功能.

当然, 你也能不使用 `alt`, 而是直接指定一整个条目的富文本样式:

```python
logger.info("i'm in rich!", style="bold red")
```

其等同于:

```python
logger.info("i'm in rich!", alt="[bold red]i'm in rich![/]")
# 实际上你一点也不 rich, 如果你没使用 richuru; just a joke :P
```

打印 `ConsoleRenderable` 对象:

```python
from rich.markdown import Markdown

with open("README.md") as readme:
    markdown = Markdown(readme.read())

logger.info("fallback msg", rich=markdown)
```

这适用于像是 `Table`, `Markdown` 这样的静态元素。

当需要使用动态元素时，需要将你所使用的 rich `Console` 对象传入 `install`。实际上，如果需要向标准输出打印任何 `ConsoleRenderable`，都推荐使用一个 `Console` 的单例。

```python
from richuru import install
from rich import Console

console = Console()
install(console=console)

with Progress(
    TextColumn('[bold green]{task.description}'),
    BarColumn(bar_width=None),
    MofNCompleteColumn(),
    '•',
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task('[cyan]Working...', total=10)
    while not progress.finished:
        logger.success('Hello, World!')
        progress.update(task, advance=1)
        progress.refresh()
        sleep(0.2)
```

# 开源协议相关

本项目使用 MIT License 开源.
