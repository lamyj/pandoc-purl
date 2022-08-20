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
        (k,v) for (k,v) in value_meta_data if k not in chunk_options]
    
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = sys.stdout
    tb = None
    try:
        tree = ast.parse(textwrap.dedent(content))
        result = None
        for child in ast.iter_child_nodes(tree):
            runner = eval if isinstance(child, ast.Expr) else exec
            compiled = compile(ast.unparse(child), "<string>", runner.__name__)
            result = runner(compiled, globals(), globals())
            
            if runner.__name__ is eval:
                result = str(result)
    except Exception as e:
        tb = traceback.format_exception(*sys.exc_info())
    
    if tb:
        result = "\n".join([sys.stdout.getvalue(), "", *tb])
    elif result:
        result = "\n".join([sys.stdout.getvalue(), result])
    else:
        result = sys.stdout.getvalue()
    
    result = result.strip("\n")
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
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
