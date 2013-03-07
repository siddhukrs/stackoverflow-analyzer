from xml.dom.minidom import parseString
from collections import defaultdict
import re
import numpy

def getclass(classname):
    #regex="<code>(.+?)</code>"
    i=0
    dot=0
    op=""
    for i in range(len(classname)):
        if classname[i]=='.':
            if classname[i+1].isupper():
                op=classname[i+1:len(classname)]
                #print op
                return op

def getmethod(classname, method):
    l1=len(classname)
    l2=method.find('(')
    op=method[l1+1:l2]
    return op

def getfield(classname,field):
    l1=len(classname)
    op=field[l1+1:len(field)]
    return op

def parsefile():
    ip="/u3/s23subramanian/Desktop/extract_fields/android dependency.xml"
    op="/u3/s23subramanian/Desktop/extract_fields/newlisting"
    #fpo=open(op,'w')
    fp=open(ip)
    data = fp.read()
    fp.close()
    dom = parseString(data)
    for detail in dom.getElementsByTagName('classDetails'):
        for classname in detail.getElementsByTagName('ce'):
            cname=classname.getAttribute('id')
            for field in classname.getElementsByTagName('fe'):
                #print "f"+getclass(cname)+":"+getfield(cname,field.getAttribute('id'))+":"+field.getAttribute('type')
                print getfield(cname,field.getAttribute('id'))
            for method in classname.getElementsByTagName('me'):
                c=0
                ret_type=""
                for param in method.getElementsByTagName('param'):
                    c=c+1
                for returntype in method.getElementsByTagName('return'):
                    ret_type=returntype.getAttribute('id')
                    #print method.getAttribute('id')
                    #print cname
                #print "m"+getclass(cname)+":"+getmethod(cname,method.getAttribute('id'))+":"+str(c)+":"+ret_type

def checkduplicate():
    ip="/u3/s23subramanian/Desktop/extract_fields/android dependency.xml"
    fp=open(ip)
    data = fp.read()
    fp.close()
    fqn=""
    cname=""
    dom = parseString(data)
    classdict=defaultdict(list)
    for detail in dom.getElementsByTagName('classList'):
        for classname in detail.getElementsByTagName('ce'):
            fqn=classname.getAttribute('id')
            cname=getclass(fqn)
            if(classdict.has_key(cname)):
                if(cname<>None):
                    print "PROBLEM:"+str(cname)+":"+str(fqn)+":"+str(classdict[cname])
                    classdict[cname]=classdict[cname]+1
            else:
                classdict[cname]=1
    print "done"
    c=0
    for value in classdict.values():
        if value<>1:
            c=c+1
    print str(c)+":"+str(len(classdict))
    print numpy.sort(classdict.values())

'''    
def checkreturntypes():
    ip="/u3/s23subramanian/Desktop/extract_fields/android dependency.xml"
    fp=open(ip)
    data = fp.read()
    fp.close()
    dom = parseString(data)    
    returntypedict=defaultdict(list)

    for detail in dom.getElementsByTagName('classDetails'):
        for classname in detail.getElementsByTagName('ce'):
            cname=classname.getAttribute('id')
            for method in classname.getElementsByTagName('me'):
                ret_type=""
                for returntype in method.getElementsByTagName('return'):
                    ret_type=returntype.getAttribute('id')
                mname=method.getAttribute('id')
                if(returntypedict.has_key(mname)):
                    if(mname<>None):
                        print "PROBLEM:"+str(cname)+":"+str(fqn)+":"+str(returntypedict[cname])
                        returntypedict[cname]=returntypedict[cname]+1
                    else:
                        returntypedict[cname]=1
                
                print "m"+getclass(cname)+":"+getmethod(cname,mname)+":"+ret_type
'''
    
parsefile()
#checkduplicate()
#sample="org.xmlpull.v1.XmlPullParserFactory.asd.Sdf"
#getclass(sample)