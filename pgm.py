from types import * 

c1 = Channel("hello world")
c2 = Channel("what?") 
recv = TyRecv(TyBool(), TyEnd())
qual = TyQual(Linear(), TyRecv(), Inaction()) 
ScopeRestriction( c1, c2, qual, Inaction() )