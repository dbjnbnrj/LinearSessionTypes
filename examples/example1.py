from sessiontypechecker import *
from sessionparser import *
from sessiontypes import *

''' First Example Simple Send Value '''
example1 = "x* true"
tree = getTree(example1, True)
ctx = Context()
ctx.env["x*"] =  TyQual( Unlimited(), TySend(TyBool()) )
typeCheck(tree, ctx)
#print octxt