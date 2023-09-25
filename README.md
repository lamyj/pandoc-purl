# pandoc-purl

<figure>
<img src="https://img.shields.io/pypi/v/pandoc-purl" alt="PyPI" />
<figcaption aria-hidden="true">PyPI</figcaption>
</figure>

*pandoc-purl* is [Pandoc](https://pandoc.org) filter for literate
programming and dynamic document generation in Python. It is similar in
spirit to [Knitr](https://yihui.org/knitr/) or
[Pweave](https://mpastell.com/pweave/).

*pandoc-purl* can be installed through *pip*
(e.g. `python3 -m pip install pandoc-purl`), and used like other Pandoc
filters, e.g. `pandoc --filter pandoc-purl document.md -o document.tex`.

## Code chunks

*pandoc-purl* will process code blocks tagged with the `python` class or
inline code tagged with the `p` or `python` classes.

**Note** This *README.md* file has been generated from the
*README.in.md* using *pandoc-purl*.

### Code blocks

Code blocks marked with the `python` class will behave as if executed in
an interactive Python shell: they execute their content, display the
content and, in a following paragraph, display any printed value as well
as the value of the last expression (see below for options controlling
this behavior).

<table style="width:83%;">
<colgroup>
<col style="width: 43%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr class="header">
<th>Input</th>
<th>Rendered</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><pre><code>```python
print(&quot;Hello pandoc-purl&quot;)
42
```</code></pre></td>
<td><div class="sourceCode" id="cb2"><pre
class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&quot;Hello pandoc-purl&quot;</span>)</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="dv">42</span></span></code></pre></div>
<pre><code>Hello pandoc-purl
42</code></pre></td>
</tr>
</tbody>
</table>

If the last statement is not an expression, the code is still executed
and displayed, but no result is printed

<table style="width:83%;">
<colgroup>
<col style="width: 43%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr class="header">
<th>Input</th>
<th>Rendered</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><pre><code>```python
a = 3.14
```</code></pre></td>
<td><div class="sourceCode" id="cb2"><pre
class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>a <span class="op">=</span> <span class="fl">3.14</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

### Inline code

Inline code marked with the `p` or `python` classes should contain only
a single expression, and will display the value of that expression in
the text.

<table style="width:83%;">
<colgroup>
<col style="width: 43%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr class="header">
<th>Input</th>
<th>Rendered</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><pre><code>The answer is `6*7`{.p}</code></pre></td>
<td>The answer is 42</td>
</tr>
</tbody>
</table>

## Chunk options

Options can be passed to code chunks using the `key=value` syntax. The
following options are available:

- `eval`: whether to run the code chunk (`true` or `false`, defaults to
  `true`)

  <table>
  <colgroup>
  <col style="width: 50%" />
  <col style="width: 50%" />
  </colgroup>
  <thead>
  <tr class="header">
  <th>Input</th>
  <th>Rendered</th>
  </tr>
  </thead>
  <tbody>
  <tr class="odd">
  <td><pre><code>The answer is `6*7`{.p}</code></pre></td>
  <td>The answer is 42</td>
  </tr>
  <tr class="even">
  <td><pre><code>The answer is `6*7`{.p eval=false}</code></pre></td>
  <td>The answer is <code
  class="sourceCode pascal"><span class="dv">6</span>*<span class="dv">7</span></code></td>
  </tr>
  </tbody>
  </table>

- `echo`: whether to show the code (code blocks only, `true` or `false`,
  defaults to `true`)

  <table style="width:83%;">
  <colgroup>
  <col style="width: 43%" />
  <col style="width: 40%" />
  </colgroup>
  <thead>
  <tr class="header">
  <th>Input</th>
  <th>Rendered</th>
  </tr>
  </thead>
  <tbody>
  <tr class="odd">
  <td><pre><code>```python
  print(&quot;Hello pandoc-purl&quot;)
  ```</code></pre></td>
  <td><div class="sourceCode" id="cb2"><pre
  class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="st">&quot;Hello pandoc-purl&quot;</span>)</span></code></pre></div>
  <pre><code>Hello pandoc-purl
  </code></pre></td>
  </tr>
  <tr class="even">
  <td><pre><code>```{.python echo=false}
  print(&quot;Hello pandoc-purl&quot;)
  ```</code></pre></td>
  <td><pre><code>Hello pandoc-purl
  </code></pre></td>
  </tr>
  </tbody>
  </table>

- `results`: how to show the result of the last expression

  - `asis`: show the result as a pre-formatted code block or inline
    (default)
  - `markup`: process the result through Pandoc before showing it
  - `hide`: hide the result

  <table>
  <colgroup>
  <col style="width: 50%" />
  <col style="width: 50%" />
  </colgroup>
  <thead>
  <tr class="header">
  <th>Input</th>
  <th>Rendered</th>
  </tr>
  </thead>
  <tbody>
  <tr class="odd">
  <td><pre><code>I&#39;m `&quot;**bold**&quot;`{.p}</code></pre></td>
  <td>I’m **bold**</td>
  </tr>
  <tr class="even">
  <td><pre><code>I&#39;m `&quot;**bold**&quot;`{.p results=markup}</code></pre></td>
  <td>I’m <strong>bold</strong></td>
  </tr>
  </tbody>
  </table>

## Changing the defaults

The default chunk options can also be changed globally by modifying
`chunk_defaults` in the `pandoc_purl` module:

    ```{.python echo=false}
    import pandoc_purl
    pandoc_purl.chunk_defaults["echo"] = False
    ```
