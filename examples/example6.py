from sessionparser import *
from sessiontypechecker import *
from sessiontypes import *

''' Input channel example '''
ipString = "lin x (y). 0"
tree = getTree(ipString, True)
    
ctx = Context()
ctx.env["x"] =  TyQual( Linear(),  TyRecv( TyBool() ) )
ctx.env["y"] =  TyQual( Unlimited(),  TyRecv( TyBool() ) )
octxt = typeCheck(tree, ctx)