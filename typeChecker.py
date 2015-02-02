from functools import reduce
import patterns-0.3
import string
import types

@patterns
def typeCheckQ():
    if q is Linear: True
    if q is Unlimited: True
    else: False

@patterns
def typeCheckBool():
    if True: True
    if False: True
    else: False
        
@patterns
def typeCheckVar():
    if s is Var: return True
    else: False

@patterns
def typeCheckTy():
    if t is TyBool: return True
    if t is TyEnd: return True
    if t is TyQual: return typeCheckQ(t.qual) and typeCheckPre(t.pre) 
    else: False

def typeCheckList(lis):
    result = True
    for l, ty in lis:
        result = result & typeCheckLabel(l) &typeCheckTy(ty)
    return result

@patterns
def typeCheckPre():
    if t is TyRecv: return typeCheckTy(t.ty1) and typeCheckTy(t.ty2) 
    if t is TySend: return True
    if t is TyBranch: return typeCheckList(lis)       
    if t is TySelect: return typeCheckList(lis)
    else: False

@patterns
def typeCheckLabel():
    if l is Label: return True
    else: return False 
        
@patterns
def typeCheckChannel():
    if c is Channel: return typeCheckVar(c.name)
    else: return False

@patterns
def typeCheckValue():
    if var is Variable: return typeCheckVar(var)
    if vbool is VBool: return typeCheckBool(vbool)
    
@patterns
def typeCheckProcess():
    if o is Output: return typeCheckChannel(o.channel) & typeCheckValue(o.value) & typeCheckProcess(o.process)
    if i is Input: return typeCheckQ(i.qualifier) & typeCheckChannel(i.channel) & typeCheckVar(i.var), typeCheckProcess(i.process)
    if p is Par: return typeCheckProcess(p.process1) & typeCheckProcess(p.process2)
    if f is If: return typeCheckValue(p.value) & typeCheckProcess(p.process1) & typeCheckProcess(p.process2)
    if iac is Inaction: return True
    if sc is ScopeRestriction: return typeCheckChannel(sc.channel1) & typeCheckChannel(sc.channel2) & typeCheckTy(sc.ty) & typeCheckProcess(sc.process)
    if sel is Select: return typeCheckLabel(sel.label) & typeCheckProcess(sel.process)
    if b is Branch: return reduce(lambda x, (l, v): True & typeCheckLabel(l) & typeCheckProcess(v) , b.lis, 0)
    else: return False
        
@patterns
def typeCheck():
    if 0: return True
    if s is Var: return True
    if l is Label: return typeCheckLabel(l)
    if n is Value: return typeCheckValue(n)
    if q is Qualifier: return typeCheckQ(q)
    if t is Ty: return typeCheckTy(t)
    if p is PreType: return typeCheckPre(p)
    if c is Channel : return typeCheckChannel(c)
    if pc is Process : return typeCheckProcess(pc)
    else: False