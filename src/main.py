########################################################################################
'''
TABLE : android
SCHEMA : title | qbody | abody | tags| qid | aid
Contains all posts from SO that are tagged android and have an accepted answer with code
count : 65095

To update, rerun this query on pgAdmin
CREATE TABLE android (title,qbody,abody,tags,qid,aid) as (WITH accepted_ques AS (SELECT title,body,id,accepted_answer_id FROM posts WHERE tags SIMILAR TO '%android%' AND accepted_answer_id IS NOT NULL) SELECT accepted_ques.title,accepted_ques.body,posts.body,posts.tags,accepted_ques.id,posts.id FROM posts,accepted_ques WHERE posts.id=accepted_ques.accepted_answer_id AND posts.body SIMILAR TO '%<code>%');
'''
#######################################################################################
import psycopg2
import sys
from collections import defaultdict
import re
import shelve
import numpy
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab
import xml_parser
import os
from lxml import etree as ET
from xml.sax.saxutils import escape,quoteattr
from xml.dom.minidom import Text, Element
import sqlite3
from numpy.matlib import rand

def run_sql():
    con = None
    try:
        con = psycopg2.connect(database='stackoverflow', user='s23subra') 
        cur = con.cursor()
        cur.execute("select * from android;")
        posts=cur.fetchall()
        print "fetched"
    except psycopg2.DatabaseError,e:
        print 'Error %s' % e    
        sys.exit(1)    
    finally:    
        if con:
            con.close()
        return posts     

def get_linecount(text):
    count=0
    for line in text:
        if line=="\n":
            count=count+1
    return count

def extract_code(text):
    regex="<code>(.+?)</code>"
    op=re.findall(regex,text.strip(),flags=re.DOTALL)
    return op

def getresults():
    try:
        conn = sqlite3.connect('/u3/s23subramanian/Desktop/extract_fields/code_final.db')
        c = conn.cursor()
        c.execute("select * from methods;")
        posts=c.fetchall()
    except:
        print 'DB Error'    
        sys.exit(1)       
    finally:    
        if conn:
            conn.close()
        return posts     

def getfromtypes(aid, codeid, prob):
    #print "select count(tname) from types where prob="+str(prob)+" and aid="+str(aid)+" and codeid="+str(codeid)+";"
    try:
        conn = sqlite3.connect('/u3/s23subramanian/Desktop/extract_fields/code.db')
        c = conn.cursor()
        #print "select count(tname) from types where prob="+prob+" and aid="+aid+" and codeid="+codeid+";"
        c.execute("select count(tname) from types where prob="+str(prob)+" and aid="+str(aid)+" and codeid="+str(codeid)+";")
        posts=c.fetchall()
    except:
        print 'DB Error'    
        sys.exit(1)       
    finally:    
        if conn:
            conn.close()
        return posts   
    pass

def generateXML():
    pass
'''
lengthvector=[]
posts=run_sql() 
c=0  
e=0
f=0
root = ET.Element("android")
for post in posts:
    accepted_code=extract_code(post[2])
    qid=post[4]
    aid=post[5]
    for code in accepted_code:
        str1=code
        if get_linecount(code)>2:
            if code.find("android:")==-1:
                c=c+1
                #print c
                f=0
                post = ET.SubElement(root, "post")
                post.set("qid",str(qid))
                post.set("aid",str(aid))
                try:
                    code = ET.SubElement(post,"code")
                    code.text=unicode(str1)
                except:
                    #print str1+"\n------------------"
                    e=e+1
                    f=1

                
print "c"+str(c)
print "e"+str(e)                     
tree = ET.ElementTree(root)
tree.write('/u3/s23subramanian/Desktop/extract_fields/android_codes.xml', pretty_print=True, xml_declaration=True,encoding='utf-8')
'''
'''
count=0
aid=""
codeid=""
i=0
size=[]
posts=getresults()
for post in posts:
    if post[5]==1:
        if(aid<>post[0] or codeid<>post[2]):
            aid=post[0]
            codeid=post[2]
            size.append(count)
            count=1+int(getfromtypes(aid,codeid,1)[0][0])
            i=i+1
            print i
        else:
            count=count+1
print len(size)
print numpy.max(size)

#print getfromtypes(9998114,1,1)[0][0]
plt.hist(size,bins =50,range={0,50})
plt.xlabel("No. of API elements identified by our approach")
plt.ylabel("No. of code snippets")
plt.xlim([1,30])
plt.savefig('/u3/s23subramanian/Desktop/methods.pdf', dpi=None, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.1)
plt.show()
'''

count=0
aid=""
codeid=""
i=0
count_expand=0
size1=[]
expand_size=[]
aidlist=[]
posts=getresults()
for post in posts:
    if post[5]==1:
        if(aid<>post[0] or codeid<>post[2]):
            size1.append(count)
            expand_size.append(count_expand)
            aid=post[0]
            codeid=post[2]
            i=i+1
            if post[7]==0:
                count_expand=1
            else:
                count_expand=post[7]
            count=1
            aidlist.append(aid)
            print i
        else:
            count=count+1
            if post[7]==0:
                count_expand=count_expand+1
            else:
                count_expand=count_expand+post[7]
            
print sum(size1)
print numpy.max(expand_size)

n=30
ind = numpy.arange(n)   # the x locations for the groups
width = 0.35            # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
x=numpy.random.random_integers(0,14240)
y=x+n
list1=size1[x:y]
list2=expand_size[x:y]
#list1, list2 = zip(*sorted(zip(list1, list2)))
#list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2))))
rects1 = ax.bar(ind, list1, width, color='#333333')
rects2 = ax.bar(ind+width, list2, width, color='#DDDDDD')
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm
matplotlib.rcParams['ps.useafm']=True
matplotlib.rcParams['pdf.use14corefonts']=True
matplotlib.rcParams['text.usetex']=True
#fontP = FontProperties()
#fontP.set_size('small')
#prop = fm.FontProperties(fname='/usr/share/fonts/truetype/freefont/FreeSans.ttf')
#ax.set_title('This is some random font', fontproperties=prop, size=10)
#fontP.set_family('sans-serif')
font = { 'fontname':'Arial', 'fontsize':10 }
plt.xlabel("Code snippet number",**font)
plt.ylabel("No. of API elements identified",**font)
ax.legend( (rects1[0], rects2[0]), ('API elements identified using our approach', 'API elements identified by lexical search'))

plt.xlim([0,n])
plt.savefig('/u3/s23subramanian/Desktop/fig3.pdf', dpi=None, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches=None, pad_inches=0.1)
plt.show()

