from sessiontypechecker import *
from sessionparser import *
from sessiontypes import *

''' Second Example Simple Recieve Value '''

example2 = "y true y"
tree = getTree(example2)
ctx = Context()
ctx.env["y"] =  TyQual( Linear(),  TyRecv( TyBool(), TyBool() ) )
octxt = typeCheck(tree, ctx)