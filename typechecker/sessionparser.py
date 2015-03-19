''' 
Session Parser Type Grammar as defined in Vasconceles Fundamental Session Types Paper.
Ref Pages 3 and 6
'''

from sessiontypes import *
from pyparsing import *
import unittest
import collections
import xml.etree.ElementTree as ET


linear = Group(Literal('lin'))("LinearNode")
unlimited = Group(Literal('un'))("UnNode")
qualifier = Group(linear | unlimited)("QualifierNode")

pre = Forward()
tybool = Group('bool')("TyBoolNode")
tyend = Group('end')("TyEndNode")
tyqual = Group(qualifier+pre)("TyQualNode")
ty =  Group(tybool | tyend | tyqual)("TyNode")

recv = Group('?'+ty+'.'+ty)("TyRecvNode")
send = Group('!'+ty+'.'+ty)("TySendNode")
pre << Group(recv | send)("PreTypeNode")

var = Group(Word( alphas+"*", alphanums+"*" ))("VariableNode")
vbool =  Group(Literal('true')|Literal('false'))("VBoolNode")
val = Group(vbool | var)("ValueNode")

channel = Group(var)("ChannelNode")

process = Forward()
outputt = Group(channel+val+Literal(".")+process)("OutputNode") # DO THIS
inputt = Group(qualifier+channel+Literal("(")+var+Literal(")")+Literal(".")+process)("InputNode")
par = Group(Literal("[")+process+Literal("|")+process+Literal("]"))("ParNode")
conditional = Group(Literal("if")+val+Literal("then")+process+Literal("else")+process)("IfNode") 
inaction = Group(Literal("0"))("InactionNode") #Done
screst = Group(Literal("(W")+channel+channel+ty+Literal(")")+process)("ScRestNode")
process << Group(outputt | inputt | par | conditional | inaction| screst)("ProcessNode")
program = OneOrMore(process | val)

class TypeNode():
    def __init__(self, root=None):
        self.root = root
        self.child = []
    
    def addChild(self, c):
        self.child.append(c)
        
def createNode(xmlroot):
    tag = xmlroot.tag
    
    if tag == "QualifierNode":
        return createNode(xmlroot[0])
    if tag == "UnNode":
        return Unrestricted()
    if tag == "LinearNode":
        return Linear()
    if tag == "TyNode":
        return createNode(xmlroot[0])
    if tag == "TyBoolNode":
        return TyBool()
    if tag == "TyEndNode":
        return TyEnd()
    if tag == "TyQualNode":
        return TyQual(createNode(xmlroot[0]), createNode(xmlroot[1]))
    if tag == "PreTypeNode":
        return createNode(xmlroot[0])
    if tag == "TyRecvNode":
        ty1 = createNode(xmlroot[0])
        ty3 = createNode(xmlroot[3])
        return TyRecieve(ty1, ty3)
    if tag == "TySendNode":
        ty1 = createNode(xmlroot[0])
        ty3 = createNode(xmlroot[3])
        return TySend(ty1, ty3)
    if tag == "ProcessNode":
        p = Process()
        for c in xmlroot:
            p.child.append(createNode(c))
        return p
    if tag == "InactionNode":
        return Inaction()
    if tag == "InputNode":
        qualifier = createNode(xmlroot[0])
        channel = createNode(xmlroot[1])
        variable = createNode(xmlroot[3])
        process = createNode(xmlroot[6])
        return Input(qualifier, channel, variable, process)
    if tag == "OutputNode":
        channel = createNode(xmlroot[0])
        value = createNode(xmlroot[1])
        process = createNode(xmlroot[3])
        return Output(channel, value, process)
    if tag == "ParNode":
        process1 = createNode(xmlroot[1])
        process2 = createNode(xmlroot[3])
        return Par(process1, process2)
    if tag == "ChannelNode":
        return Channel(createNode(xmlroot[0]))
    if tag == "VariableNode":
        return Variable(xmlroot[0].text)
    if tag == "VBoolNode":
        return VBool(xmlroot[0].text)
    if tag == "ValueNode":
        v = Value()
        for c in xmlroot:
            v.child.append(createNode(c))
        return v
    if tag == "IfNode":
        value = createNode(xmlroot[1])
        process1 = createNode(xmlroot[3])
        process2 = createNode(xmlroot[5])
        return If(value, process1, process2)
    if tag == "ScRestNode":
        channel1 = createNode(xmlroot[1])
        channel2 = createNode(xmlroot[2])
        ty = createNode(xmlroot[3])
        process = createNode(xmlroot[5])
        return ScopeRestriction(channel1, channel2, ty, process)
    else:
        return None
    
def XMLToTypeTree(xmlroot):
    tree = TypeNode()
    node = createNode(xmlroot)
    
    if xmlroot is None:
        return None
    
    if node is None:
        return None
    
    else:
        tree.root = node
        
    for c in xmlroot:
        #print 'Child:' + str(c)  + ' T:' + str(c.tag) + ' Parent:' + str(tree) + ' T:' + str(xmlroot.tag)
        childTree = XMLToTypeTree(c)
        if childTree:
            tree.addChild(childTree)
    return tree

def getTree(string, toPrint = False):
    ps = program.parseString(string)
    xmldata = ps.asXML()
    
    root = ET.fromstring(xmldata)
    tree = createNode(root)
    
    if toPrint:
        print xmldata
        
    return tree