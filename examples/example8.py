from sessionparser import *
from sessiontypechecker import *
from sessiontypes import *

opString = "x* true . 0"
example = "["+opString+"|"+ipString+"] "
tree = getTree(example, False)
print opString
print ipString

ctx = Context()
ctx.env["x*"] =  TyQual( Linear(),  TySend( TyBool() ) )
ctx.env["x"] =  TyQual( Linear(),  TyRecv( TyBool() ) )
ctx.env["y"] =  TyQual( Unlimited(),  TyRecv( TyBool() ) )
octxt = typeCheck(tree, ctx)