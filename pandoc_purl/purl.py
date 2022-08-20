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
            k: bool(v) if v.lower() in ["true", "false"] else v
            for k,v in value_meta_data})
    
    if "python" not in classes or not chunk_options["eval"]:
        return
    
    value_meta_data = [
        (k,v) for (k,v) in value_meta_data if k not in chunk_options]
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    old_stderr = sys.stderr
    sys.stderr = sys.stdout
    try:
        tree = ast.parse(textwrap.dedent(content))
        result = None
        for child in ast.iter_child_nodes(tree):
            if isinstance(child, ast.Expr):
                result = eval(
                    compile(ast.unparse(child), "<string>", "eval"),
                    globals(), globals())
                if result:
                    result = str(result)
            else:
                result = exec(
                    compile(ast.unparse(child), "<string>", "exec"),
                    globals(), globals())
    except Exception as e:
        result = (
            sys.stdout.getvalue()
            + "\n"
            + "\n".join(traceback.format_exception(*sys.exc_info())))
    else:
        if result:
            result = sys.stdout.getvalue() + "\n" + result
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
