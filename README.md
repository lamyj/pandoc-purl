# pandoc-purl

[![PyPI](https://img.shields.io/pypi/v/pandoc-purl)](https://pypi.org/project/pandoc-purl/)

*pandoc-purl* is [Pandoc](https://pandoc.org) filter for literate
programming and dynamic document generation in Python. It is similar in
spirit to [Knitr](https://yihui.org/knitr/) or
[Pweave](https://mpastell.com/pweave/).

*pandoc-purl* can be installed through *pip*
(e.g. `python3 -m pip install pandoc-purl`), and used like other Pandoc
filters, e.g. `pandoc --filter pandoc-purl document.md -o document.tex`.

## Code chunks

*pandoc-purl* will process code blocks or inline code which are tagged
with the `.python` class.

**Note** This *README.md* file has been generated from the
*README.in.md* using *pandoc-purl*.

### Code blocks

For a code block, the following Mardown code block:

    ```{.python}
    print("Hello pandoc-purl")
    42
    ```

will display the code in the document (see below for options controlling
this behavior) and add a paragraph below it containing the printed data
and the value of the last expression, i.e.

    Hello pandoc-purl
    42

### Inline code

Inline code should contain only a single expression; the following
Markdown snippet:

    The Answer to the Ultimate Question of Life, The Universe, and Everything is `6*7`{.python}.

will generate:

    The Answer to the Ultimate Question of Life, The Universe, and Everything is 42.

If the value of the inline code is wrapped by `$` or `$$`, it will be
parsed as inline math or display math. For example,
`` `"$E=mc^2$"`{.python} `` will yield $E=mc^2$ and
`` `r"$$G_{mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}$$"`{.python} `` will
yield $$G_{mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}$$

## Chunk options

Options can be passed to code chunks using the `key=value` syntax. The
following options are available

-   `eval`: whether to run the code chunk (`true` or `false`, defaults
    to `true`)
-   `echo`: whether to show the code (code blocks only, `true` or
    `false`, defaults to `true`)

These options can also be changed globally by modifying `chunk_defaults`
in the `pandoc_purl` module:

    ```{.python echo=false}
    import pandoc_purl
    pandoc_purl.chunk_defaults["echo"] = False
    ```
