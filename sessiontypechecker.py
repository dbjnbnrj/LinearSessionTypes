''' 
Session Type Checker contains the implementation of the Algorithmic Type Checker
Mentioned on Pg 23 of Vasconcelos' Fundamental Sesions Paper.
'''

from sessiontypes import *
from sessionparser import *
from functools import reduce
from patterns import patterns, Mismatch
import string
import copy

'''
Context contains the used variables and their associated Types
'''
class Context:
    def __init__(self):
        self.env = {}
        self.LinFreeVars = []

''' Determines if Types is Unlimited '''
@patterns
def isUnlimited():
    if t is TyQual:
        print "Is Ty Qual"
        print t.qual
        if isinstance(t.qual,Linear):
            print "Is Linear"
            return False
        else:
            print "Is Unlimited"
            return True
    else:
        return True

''' Consumes Linear Variable From Context Env '''
def consume(name , st):
    ''' If in consume must be a linear variable '''
    if name in st.env:
        value = copy.copy(st.env[name])
        pretype = value.pre
        
        ''' Checking if whole of PreType is used '''
        if isinstance(pretype, PreType):
            if( pretype.ty2 != None):
                ivalue = copy.copy(pretype.ty2)
                pretype.ty1 = pretype.ty2
                pretype.ty2 = None
                value.pre = pretype
                st.env[name] = value
                return (ivalue, st)
        
        del st.env[name]
        return (value, st)
    
    return False

''' Checks for duality of TyRecv and TySend '''
def areDual(t1, t2):
    return (isinstance(t1, TyRecv) and isinstance(t2, TySend) ) or (isinstance(t1, TySend) and isinstance(t2, TyRecv))
        
''' TypeChecker for Value - ie Variable and VBool Types '''
def typeCheckVal(t, st):
    if isinstance(t, Channel):
        print "Getting channel typechecked", t.name
        return typeCheckVal(t.name, st)
    if isinstance(t, Variable):
        if(t.item in st.env):
            ty = st.env[t.item]
            if isUnlimited( ty ):
                return(ty, st)
            else:
                ty, s1= consume(t.item, st)
                print "After consume ty: ", ty," s1: ", s1
                s1 = copy.copy(s1) # This is to ensure that the result persists
                return (ty, s1) 
        else:
            raise Exception("Unbound type variable ")
    if isinstance(t, VBool):
        print "TypeChecking VBool"
        return (TyBool(), st)
    if isinstance(t, Value):
        return typeCheckVal(t.child[0], st)

''' TypeChecker for Process Types 
Inaction, Output, Input, ScopeRestriction, 
Par, If and Recursive Process
'''
def typeCheckProcess(t, st):
    if isinstance(t, Inaction):
        print "In Inaction"
        return st
    
    if isinstance(t, Output):
        print "In Output"
        ty, st = typeCheckVal(t.channel, st)
        if(isinstance(ty.pre, TySend)):
            ty1, st1 = typeCheckVal(t.value, st)
            print type(ty1)
            print type(ty.pre.ty1)
            if type(ty1) != type(ty.pre.ty1):
                raise Exception("No match between Send Type and Value Type")
            else:
                return typeCheckProcess(t.process, st1)
        else:
            raise Exception("Pretype is not send")
            
    if isinstance(t, Input):
        print "In Input T: ",t," St :",st
        print "Channel has type",t.channel
        ty, st = typeCheckVal(t.channel, st)
        print "Type : ", ty
        if(isinstance(ty.pre, TyRecv)):
            ty1, st1 = typeCheckVal(t.variable, st)
            if type(ty1) != type(ty.pre.ty1):
                raise Exception("No match between Recieve Type and Value Type")
            else:
                return typeCheckProcess(t.process, st1)
        else:
            raise Exception("Pretype is not recieve")
        return st
    
    if isinstance(t, ScopeRestriction):
        # Check if Dual Types
        print "In Scope Restriction"
        c1 =  st.env[t.channel1.name.item].pre
        c2 =  st.env[t.channel2.name.item].pre
        if ( areDual(c1, c2) ):
            print "Dual Channels"
            return typeCheckProcess(t.process, st)
        else:
            raise Exception("Channels are not dual")
    if isinstance(t, Par):
        print "TypeChecking Parallel Processes"
        st1 = typeCheckProcess(t.process1, st)
        return typeCheckProcess(t.process2, st1)
    if isinstance(t, If):
        print "TypeChecking If Process"
        condition = t.value.child[0].item
        if condition == "true":
            print "In Condition 1"
            return typeCheckProcess(t.process1, st)
        else:
            return typeCheckProcess(t.process2, st)   
    if isinstance(t, Process):
        return typeCheckProcess(t.child[0], st)

''' 
Main TypeChecker for Process/Values
Accepts a tree and state variable
'''       
def typeCheck(t, st):
    if isinstance(t, Value):
        print "Type checking Value"
        result = []
        s1 = copy.copy(st)
        for c in t.child:
            r = typeCheckVal(c, s1)
            result.append(r)
        
        print("---- Result : TypeChecking Success ---")
        return result
    
    if isinstance(t, Process):
        print("TypeChecking Process")
        result = []
        s1 = copy.copy(st)
        for c in t.child:
            r = typeCheckProcess(c, s1)
            result.append(r)
            
        print("---- Result : TypeChecking Success ---")
        return result