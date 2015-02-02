from functools import reduce
from patterns import patterns, Mismatch
import string

class State:
    def __init__(self, env, freevar):
        self.env = env
        self.freevar= freevar

st = State(None, None)

@patterns
def isUnlimitedType():
    if q is Unlimited: return True
    if q is Linear: return False
    if q is TyQual: return isUnlimitedType(q.qual)
    else: return False


''' Removing linear variables '''
def removeVar(var, state):
    state.env.pop(var)
    return state

''' Checking if two environments are equal '''
def equivEnv(env1, env2):
    if len(env1) != len(env2):
        return False
    for k in env1:
        print(k)
        if k in env2:
            if type(env2[k]) != type(env1[k]):
                return False
        else:
            return False
        
    return True

''' Check if two variable lists are equal'''
def equalVarLists(lvar1, lvar2):
    return lvar1.sort() == lvar2.sort()

''' Check if the states are equal '''
def equivStates(env1, env2):
    return equivStates(env1.states, env2.states) and equalVarLists(env1.freevar, env2.freevar)


''' See Context Difference pg 23 '''
def envDiff(e1, L):
    if(L == []):
        return s1
    temps1 = e1.copy()
    for ele in L:
        if ele in s1:
            if isinstance(e1[ele], TyQual) and isinstance(e1[ele].qual, Unlimited):
                continue
            else:
                temps1.pop(ele)
    return temps1

''' Update the env '''
def envUpdate(env, var, ty):
    env[var] = ty

''' Update the state '''
def stateUpdate(state, env):
    state.env = env

''' Handling dual Types '''
@patterns
def preTyDual():
    if t is TyRecv: return TySend(t.ty1, tyDual(t.ty2))
    if t is TySend: return TyRecv(t.ty1, tyDual(t.ty2))
    else: print("Dual Type not defined")
        
@patterns
def tyDual():
    if ty is TyQual: return TyQual(ty.qual, preTyDual(ty.pre))
    if ty is TyEnd: return TyEnd
    else: print("Dual Type not defined")

''' typeChecks the Values in the Process'''
def typeCheckVal(ty, name, st):
    if isinstance(ty,VBool):
        return (TyBool, st)
    if isinstance(ty,Variable):
        if name in st.env:
            if isUnlimitedType(st.env[name]):
                return (st.env[name], st)
            else:
                return (st.env[name], removeVar(name, st) ) 
    else:
        print("Error: Unbound type variable")


''' Process typeChecker '''
@patterns
def typeCheck():
    if t is Inaction: st = st
    
def eval():
    