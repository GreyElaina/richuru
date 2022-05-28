# richuru - Using Rich in Loguru to colour the logs

[简体中文](README.zh.md) | English

richuru is a lightweight dependency that provides [`rich`](https://github.com/willmcgugan/rich)'s powerful terminal rendering support for [`loguru`](https://github.com/Delgan/loguru).

This project is sourced and independent from the component `graia.amnesia.log` of [`Graia Amnesia`](https://github.com/GraiaProject/Amnesia),
and is modified from the original implementation of @BlueGlassBlock.

# Quick Start

Install ``richuru``:

```bash
elaina@localhost $ pip install richuru

elaina@localhost $ pdm add richuru

elaina@localhost $ poetry add richuru
```

Try it in REPL:

```python
>>> import richuru
>>> richuru.install()
>>>
>>> from loguru import logger
>>> logger.info("Hello World!", alt="Hello, [bold magenta]World[/bold magenta]!")
```

`richuru` is designed as an optional dependency, which means that you need to provide a fallback pattern when using `richuru` wherever possible, to be compatible with end-users who do not have `richuru` enabled.

Provide `alt` in `logger.<method>(...) ` with the `alt` option to make `richuru` recognize and enable `rich`'s rich text functionality.

Of course, you can also specify an entire entry's rich text style without using `alt`:

```python
logger.info("i'm in rich!", style="bold red")
```

which is equivalent to :

```python
logger.info("[bold red]i'm in rich![/]", alt="[bold red]i'm in rich![/]")
```

This pattern only works if ``richuru`'' is used as a mandatory dependency, otherwise the typography you write will be reproduced exactly as it is:

```
[05/28/22 11:37:21]
INFO [bold red]i'm in rich![/] 
```

Print the `ConsoleRenderable` object:

```python
from rich.markdown import Markdown

with open("README.md") as readme:
    markdown = Markdown(readme.read())

logger.info("fallback msg", rich=markdown)
```

This works with static elements like `Table`, `Markdown`, and dynamic elements like `Status`, `Progress`, which have not been tested yet.

# Open Source License

This project is open source under the MIT License.