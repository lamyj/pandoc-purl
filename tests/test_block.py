import json
import subprocess
import textwrap
import unittest

import pandoc_purl
import pandocfilters

class PurlTest(unittest.TestCase):
    def _purl(self, source):
        document = subprocess.run(
                ["pandoc", "-f", "markdown", "-t", "json"],
                input=source.encode(), stdout=subprocess.PIPE
            ).stdout
        
        altered = pandocfilters.applyJSONFilters([pandoc_purl.purl], document)
        return json.loads(altered)
        
    def _check_blocks(self, baseline, value):
        self.assertEqual(baseline, value)

class TestBlock(PurlTest):
    def test_statements(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            a = f(1+1)""")
        source = (
            "```python\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", ["python"], []], code]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_expression(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```python\n"
            + code + "\n"
            + "```\n")
        baseline = [
            {"t": "CodeBlock", "c": [["", ["python"], []], code]},
            {"t": "CodeBlock", "c": [["", [], []], "2"]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_silent(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```{.python echo=false}\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", [], []], "2"]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_no_exec(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```{.python eval=false}\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", ["python"], []], code]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_skipped(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```foobar\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", ["foobar"], []], code]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_asis(self):
        code = textwrap.dedent("""\
            def f(foo):
                return f"**{foo}**"
            f(1+1)""")
        source = (
            "```{.python echo=false results=asis}\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", [], []], "**2**"]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_hide(self):
        code = textwrap.dedent("""\
            def f(foo):
                return f"**{foo}**"
            f(1+1)""")
        source = (
            "```{.python echo=false results=hide}\n"
            + code + "\n"
            + "```\n")
        baseline = []
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_markup(self):
        code = textwrap.dedent("""\
            def f(foo):
                return f"**{foo}**"
            f(1+1)""")
        source = (
            "```{.python echo=false results=markup}\n"
            + code + "\n"
            + "```\n")
        baseline = [
            {'t': 'Para', 'c': [{'t': 'Strong', 'c': [{'t': 'Str', 'c': '2'}]}]}
        ]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
    
    def test_chunk_defaults(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```{.python echo=false}\n"
            + "import pandoc_purl" + "\n"
            + "pandoc_purl.chunk_defaults['echo'] = False" + "\n"
            + "```\n"
            + "```{.python}\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", [], []], "2"]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
        pandoc_purl.chunk_defaults["echo"] = True
    
    def test_classes(self):
        code = textwrap.dedent("""\
            def f(foo):
                return str(foo)
            f(1+1)""")
        source = (
            "```{.python echo=false}\n"
            + "import pandoc_purl" + "\n"
            + "pandoc_purl.defaults['classes']['CodeBlock'] = ['foobar']" + "\n"
            + "```\n"
            + "```{.foobar echo=false}\n"
            + code + "\n"
            + "```\n")
        baseline = [{"t": "CodeBlock", "c": [["", [], []], "2"]}]
        
        altered = self._purl(source)
        self._check_blocks(baseline, altered["blocks"])
        pandoc_purl.defaults["CodeBlock"] = ["python"]
    
if __name__ == "__main__":
    unittest.main()
