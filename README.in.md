# pandoc-purl

![PyPI](https://img.shields.io/pypi/v/pandoc-purl)

_pandoc-purl_ is [Pandoc](https://pandoc.org) filter for literate programming and dynamic document generation in Python. It is similar in spirit to [Knitr](https://yihui.org/knitr/) or [Pweave](https://mpastell.com/pweave/).

_pandoc-purl_ can be installed through _pip_ (e.g. `python3 -m pip install pandoc-purl`), and used like other Pandoc filters, e.g. `pandoc --filter pandoc-purl document.md -o document.tex`.

## Code chunks

_pandoc-purl_ will process code blocks or inline code which are tagged with the `.python` class.

**Note** This _README.md_ file has been generated from the _README.in.md_ using _pandoc-purl_.

### Code blocks

For a code block, the following Mardown code block:

    ```{.python}
    print("Hello pandoc-purl")
    42
    ```

will display the code in the document (see below for options controlling this behavior) and add a paragraph below it containing the printed data and the value of the last expression, i.e.

```{.python echo=false}
print("Hello pandoc-purl")
42
```

### Inline code

Inline code should contain only a single expression; the following Markdown snippet:

    The Answer to the Ultimate Question of Life, The Universe, and Everything is `6*7`{.python}.

will generate:

    The Answer to the Ultimate Question of Life, The Universe, and Everything is 42.

If the value of the inline code is wrapped by `$` or `$$`, it will be parsed as inline math or display math. For example, `` `"$E=mc^2$"`{.python} `` will yield `"$E=mc^2$"`{.python} and `` `r"$$G_{mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}$$"`{.python} `` will yield `r"$$G_{mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}$$"`{.python}

## Chunk options

Options can be passed to code chunks using the `key=value` syntax. The following options are available

- `eval`: whether to run the code chunk (`true` or `false`, defaults to `true`)
- `echo`: whether to show the code (code blocks only, `true` or `false`, defaults to `true`)

These options can also be changed globally by modifying `chunk_defaults` in the `pandoc_purl` module:
    
    ```{.python echo=false}
    import pandoc_purl
    pandoc_purl.chunk_defaults["echo"] = False
    ```
