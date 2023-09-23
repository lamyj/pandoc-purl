import ast
import io
import sys
import textwrap
import traceback

import pandocfilters

chunk_defaults = {
    "eval": True, # Whether to run the code chunk
    "echo": True, # Whether to show the code chunk
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
    
    if "python" not in classes or not chunk_options["eval"]:
        return
    
    value_meta_data = [
        (k,v) for (k,v) in value_meta_data if k not in chunk_defaults]
    
    result, is_traceback = __purl_capture(textwrap.dedent(content))
    
    blocks = []
    if type_ == "CodeBlock" and chunk_options["echo"]:
        Block = getattr(pandocfilters, type_)
        blocks.append(Block((identifiers, classes, value_meta_data), content))
    if result:
        if type_ == "Code":
            if result.startswith("$") and result.endswith("$"):
                Block = pandocfilters.Math
                if result.startswith("$$") and result.endswith("$$"):
                    math_type = "DisplayMath"
                else:
                    math_type = "InlineMath"
                args = ({"t": math_type}, result.strip("$ "))
            else:
                Block = pandocfilters.Str
                args = (result,)
            blocks.append(Block(*args))
        else:
            blocks.append(pandocfilters.CodeBlock(["", [], []], result))
        
    return blocks

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
