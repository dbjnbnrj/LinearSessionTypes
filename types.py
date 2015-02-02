''' Qualifier Type '''
class Qualifier:
    def __init__(self):
        pass

class Linear(Qualifier):
    def __init__(self):
        pass

class Unlimited(Qualifier):
    def __init__(self):
        pass

''' Var Type '''
Var = str

''' Ty Type '''
class Ty :
    def __init__(self):
        pass
        
class TyBool(Ty):
        def __init__(self):
            pass
            
class TyEnd(Ty):
        def __init__(self):
            pass
            
class TyQual(Ty): 
    def __init__(self, qual,pre):
        self.qual = qual
        self.pre = pre

''' PreType Class '''
class PreType:
    def __init__(self):
        pass

class TyRecv(PreType):
    def __init__(self, ty1, ty2):
        self.ty1 = ty1
        self.ty2 = ty2
        
class TySend(PreType):
    def __init__(self, ty1, ty2):
        self.ty1 = ty1
        self.ty2 = ty2

class TyBranch(PreType):
    def __init__(self, lis):
        self.lis = lis

class TySelect(PreType):
    def __init__(self, lis):
        self.lis = lis

''' Label Type '''
class Label:
    def __init__(self, name):
        self.name = name

''' Value Type'''
class Value:
    def __init__(self):
        pass

class Variable(Value):
    def __init__(self, var):
        self.val = var
    
class VBool(Value):
    def __init__(self, boolval):
        self.boolval = boolval

''' Channel Type '''
class Channel:
    def __init__(self, name):
        self.name = name 

''' Process Type '''
class Process:
    def __init__(self):
        pass

class Output(Process):
    def __init__(self, channel, value, process):
        self.channel = channel
        self.value = value
        self.process = process

class Input(Process):
    def ___init___(self, qualifier, channel, variable, process):
        self.qualifier = qualifier
        self.channel = channel
        self.variable = variable
        self.process = process
        
class Par(Process):
    def __init__(self, process1, process2):
        self.process1 = process1
        self.process2 = process2

class If(Process):
    def __init__(self, value, process1, process2):
        self.value = value
        self.process1 = process1
        self.process2 = process2
        
class Inaction(Process):
    def __init__(self):
        pass

class ScopeRestriction(Process):
    def __init__(self, channel1, channel2, ty, process):
        self.channel1 = channel1
        self.channel2 = channel2
        self.ty = ty
        self.process = process

class Select(Process):
    def __init__(self, label, process):
        self.label = label
        self. process
        
class Branch(Process):
    def __init__(self, lis):
        self.lis = lis
        
class Context:
    def __init__(self, ele):
        self.ele = ele