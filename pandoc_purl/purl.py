import ast
import io
import json
import subprocess
import sys
import textwrap
import traceback

import pandocfilters

chunk_defaults = {
    "eval": True, # Whether to run the code chunk
    "echo": True, # Whether to show the code chunk (code block only)
    "results": "asis", # if "markup", pass to pandoc; if "hide", hide results
}

defaults = {
    "classes": {
        "CodeBlock": ["python"],
        "Code": ["python", "p"]
    }
}

def purl(type_, value, format_, meta_data):
    if type_ not in ["CodeBlock", "Code"]:
        return
    
    (identifiers, classes, value_meta_data), content = value
    
    chunk_options = chunk_defaults.copy()
    chunk_options.update(
        {
            k: eval(v.lower().capitalize())
                if v.lower() in ["true", "false"] else v
            for k,v in value_meta_data})
    
    if not any(x in defaults["classes"][type_] for x in classes):
        return
    
    if type_ == "CodeBlock":
        return __purl_codeblock(value, format_, meta_data)
    elif type_ == "Code":
        return __purl_inline(value, format_, meta_data)

def __purl_codeblock(value, format_, meta):
    (identifiers, classes, value_meta_data), content = value
    chunk_options, result, traceback = __purl_common(content, value_meta_data)
    
    blocks = []
    if chunk_options["echo"]:
        value_meta_data = [
            (k,v) for (k,v) in value_meta_data if k not in chunk_defaults]
        blocks.append(
            pandocfilters.CodeBlock(
                (identifiers, classes, value_meta_data), content))
    if chunk_options["results"] != "hide" and result is not None and result.strip():
        if not traceback and chunk_options["results"] == "markup":
            document = json.loads(
                subprocess.run(
                    ["pandoc", "-f", "markdown", "-t", "json"],
                    input=result.encode(), stdout=subprocess.PIPE
                ).stdout)
            blocks.extend(document["blocks"])
        else:
            blocks.append(pandocfilters.CodeBlock(["", [], []], result))
    
    return blocks

def __purl_inline(value, format_, meta):
    (identifiers, classes, value_meta_data), content = value
    chunk_options, result, traceback = __purl_common(content, value_meta_data)
    
    blocks = []
    if not chunk_options["eval"]:
        value_meta_data = [
            (k,v) for (k,v) in value_meta_data if k not in chunk_defaults]
        blocks.append(
            pandocfilters.Code(
                (identifiers, classes, value_meta_data), content))
    if chunk_options["results"] != "hide" and result is not None and result.strip():
        if not traceback and chunk_options["results"] == "markup":
            document = json.loads(
                subprocess.run(
                    ["pandoc", "-f", "markdown", "-t", "json"],
                    input=result.encode(), stdout=subprocess.PIPE
                ).stdout)
            if len(document["blocks"]) == 1 and document["blocks"][0]["t"] == "Para":
                blocks.extend(document["blocks"][0]["c"])
            else:
                raise Exception("Not an inline content")
        else:
            blocks.append(pandocfilters.Str(result))
    
    return blocks

def __purl_common(content, value_meta_data):
    chunk_options = chunk_defaults.copy()
    chunk_options.update(
        {
            k: eval(v.lower().capitalize())
                if v.lower() in ["true", "false"] else v
            for k,v in value_meta_data})
    
    result = None
    traceback = False
    if chunk_options["eval"]:
        result, traceback = __purl_capture(content)
    
    return chunk_options, result, traceback

def __purl_exec(content):
    tree = ast.parse(content)
    
    # Check whether we have a final expression. If so remove it from the tree
    # and keep it for later
    final = None
    for name, nodes in ast.iter_fields(tree):
        if name != "body":
            continue
        if nodes and isinstance(nodes[-1], ast.Expr):
            final = ast.Expression(nodes.pop().value)
    
    # The tree is now a sequence of statements without a final expression.
    # It can be exec()ed since there is no return value
    exec(compile(tree, "<string>", "exec"), globals(), globals())
    # If there was a final expression in the tree, eval() it and get its result
    result = None
    if final:
        result = eval(compile(final, "<string>", "eval"), globals(), globals())
    return result

def __purl_capture(content):
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = sys.stdout
    
    tb = None
    result = None
    try:
        result = __purl_exec(content)
    except Exception as e:
        tb = traceback.format_exception(*sys.exc_info())
    
    if tb:
        result = "\n".join([sys.stdout.getvalue(), "", *tb])
    elif result:
        result = "".join([sys.stdout.getvalue(), str(result)])
    else:
        result = sys.stdout.getvalue()
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    return result, tb is not None
