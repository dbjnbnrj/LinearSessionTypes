from sessiontypechecker import *
from sessionparser import *
from sessiontypes import *

''' Third Example Simple Inaction Process '''

example3 = "0"
tree = getTree(example3)

ctx = Context()
ctx.env["x*"] =  TyQual( Linear(),  TySend( TyBool() ) )

octxt = typeCheck(tree, ctx)
for c in octxt:
    print c.env