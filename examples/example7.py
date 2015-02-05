from sessionparser import *
from sessiontypechecker import *
from sessiontypes import *

opString = "x* true . 0"
example = "(W x* y bool) "+opString
tree = getTree(example, False)
    
ctx = Context()
ctx.env["x*"] =  TyQual( Linear(),   TySend( TyBool() ) )
ctx.env["y"] =  TyQual( Unlimited(),  TyRecv( TyBool(), TyBool()) )
octxt = typeCheck(tree, ctx)