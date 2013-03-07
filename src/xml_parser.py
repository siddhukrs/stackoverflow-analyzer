from xml.dom.minidom import parseString
from collections import defaultdict
packdict=defaultdict(list)
classdict=defaultdict(list)
import numpy


def getClass(s):
    temp=s
    i=0
    while(temp.find("/")<>-1):
        i=temp.find("/")
        temp=temp[i+1:len(temp)]
    return temp
    

def getPackage(s):
    temp=s
    i=0
    while(temp.find("/")<>-1):
        i=temp.find("/")
        temp=temp[i+1:len(temp)]
    return s[0:len(s)-len(temp)-1]
    

def getMethodTypes(s,class_name):
    types=[]
    lb=s.find("(")
    rb=s.find(")")
    method_name=str(s[0:lb])
    return_type=str(s[rb+1:len(s)])
    
    if return_type=="V":
        return_type="void"
    else:
        return_type=getClass(return_type)
        return_type=return_type[0:len(return_type)-1]
    if method_name.find("init")<>-1:
        method_name=getClass(class_name)
    param=[]
    st=s[lb+1:rb]
    i=0
    while(st.find(";")<>-1):
        l=st.find(";")
        param.append(str(st[i+1:l]))
        st=st[l+1:len(st)]
    #To generate method listing, uncomment
    #fpo.write(getClass(class_name)+":"+method_name+":"+return_type+"\n")
    types.append(method_name)
    #types.append(return_type)
    #types.append(param)
    return types

def parsefile():
    ip="/u3/s23subramanian/Desktop/extract_fields/api-versions.xml"
    op="/u3/s23subramanian/Desktop/extract_fields/methodlisting"
    #fpo=open(op,'w')
    fp=open(ip)
    data = fp.read()
    fp.close()
    dom = parseString(data)
    for classname in dom.getElementsByTagName('class'):
        imp_list=[] #[list of interfaces in the class]
        ext_list=[] #[list of superclass names]
        field_list=[] #[list of field names]
        method_list=[] #[method name,return type,list of parameter types]
        pack_class_name=classname.getAttribute('name')
        for method in classname.getElementsByTagName('method'):
            #method_list.append(getMethodTypes(method.getAttribute('name').strip(),pack_class_name,fpo))
            method_list.append(getMethodTypes(method.getAttribute('name').strip(),pack_class_name))

        for interface in classname.getElementsByTagName('implements'):
            imp_list.append(str(interface.getAttribute('name')).strip())
        for extends in classname.getElementsByTagName('extends'):
            ext_list.append(str(extends.getAttribute('name')).strip())
        for field in classname.getElementsByTagName('field'):
            field_list.append(str(field.getAttribute('name')).strip())
        #print pack_class_name
        package_name=getPackage(pack_class_name)
        class_name=getClass(pack_class_name)
        packdict[package_name].append(class_name)
        classdict[pack_class_name].append(method_list)
    #fpo.close()
