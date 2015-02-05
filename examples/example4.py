from sessionparser import *
from sessiontypechecker import *
from sessiontypes import *

''' Both Send and Recieve - Linear / Unlimited Types '''

example = "y* x"
tree = getTree(example)
print tree
ctx = Context()
ctx.env["x"] =  TyQual( Linear(),  TyRecv( TyBool() ) )
ctx.env["y*"] =  TyQual( Unlimited(),  TySend( TyBool() ) )
octxt = typeCheck(tree, ctx)