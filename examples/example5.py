from sessionparser import *
from sessiontypechecker import *
from sessiontypes import *

''' Output Channel Example '''

opString = "x* true . 0"
tree = getTree(opString, False)
print tree
    
ctx = Context()
ctx.env["x*"] =  TyQual( Unlimited(),  TySend( TyBool() ) )
ctx.env["y"] =  TyQual( Linear(),  TyRecv( TyBool() ) )
# ctx.env["y*"] =  TyQual( Unlimited(),  TyRecv( TyBool() ) )
octxt = typeCheck(tree, ctx)
print octxt[0].env