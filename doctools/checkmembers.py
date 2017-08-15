## lazy way to check member docs
## does so in a very primitive way
import os
from pprint import pprint
def parseMemberDec():
    with open('../pol-core/bscript/objmembers.h','r') as f:
        in_dec=False
        decs=[]
        for l in f.readlines():
            l=l.strip();
            if l=='enum MemberID':
                in_dec=True
                continue
            if not in_dec:
                continue
            if l.startswith('MBR_'):
                decs.append([l.split(',')[0],None])
            elif l.startswith('};'):
                break
    return decs

def parseMemberDef(decs):
    defs=dict()
    with open('../pol-core/bscript/parser.cpp','r') as f:
        in_def=False
        for l in f.readlines():
            l=l.strip();
            if l.startswith('ObjMember object_members[]'):
                in_def=True
                continue
            if not in_def:
                continue
            if l.startswith('{MBR_'):
                l=l.replace('{','').replace('"','')
                l=[_.strip() for _ in l.split(',')]
                for d in decs:
                    if d[0]==l[0]:
                        defs[d[0]]=l[1].lower()
                        del d
                        break
            elif l.startswith('};'):
                break
    return defs

def parseFile(file,defs,members):
    with open(file,'r') as f:
        in_d=False
        active=None
        supported=[]
        openb=0
        linec=0
        in_c=False
        for l in f.readlines():
            linec+=1
            l=l.strip()
            if l.startswith('//'):
                continue
            cs=l.rfind('/*')
            ce=l.rfind('*/')
            if cs>ce:
                in_c=True
            elif ce>cs:
                in_c=False
            if in_c:
                continue
            if l.startswith('return'):
                continue
            if not in_d and '::get_member_id' in l:
                l=l[:l.find('::get_member_id')]
                active=l.split()[-1]
                in_d=True
            elif not in_d and '::get_script_member_id' in l:
                l=l[:l.find('::get_script_member_id')]
                active=l.split()[-1]
                in_d=True
            elif in_d:
                if '{' in l:
                    openb+=1
                if '}' in l:
                    openb-=1
                    if not openb and in_d:
                        if len(supported):
                            members[active]=supported
                        supported=[]
                        in_d=False
                if l.startswith('case'):
                    try:
                        if '::' in l:
                            m=l.split('::')[1]
                        else:
                            m=l
                        m=m.replace('(','').replace(')','')
                        m=m.split(':')[0].split()[-1]
                        supported.append(defs[m])
                    except Exception as e:
                        print(e)
                        print(file)
                        print(l)
                        print(linec)
                        continue
                        raise
    return members

def checkDocs():
    docs=dict()
    with open('../docs/docs.polserver.com/pol099/objref.xml','r') as f:
        in_c=None
        for l in f.readlines():
            l=l.strip()
            if l.startswith('<class'):
                n=l.split('name="')[1].split('"')[0]
                in_c=n
            elif l.startswith('</class>'):
                in_c=None
            elif in_c and l.startswith('<member'):
                p=l.split('mname="')[1].split('(')[0].split('"')[0].lower()
                if in_c in docs:
                    docs[in_c].append(p)
                else:
                    docs[in_c]=[p]
    return docs


                
decs=parseMemberDec()
defs =parseMemberDef(decs)
pprint(defs)

members=dict()
for r,d,files in os.walk('../pol-core/'):
    for f in files:
        if f.endswith('.cpp'):
            parseFile(os.path.join(r,f),defs,members)
pprint(members)
pprint(members.keys())
docs=checkDocs()
pprint(docs)

for dc,dm in docs.items():
    pm=dc
    if pm=='Struct':
        pm='BStruct'
    elif pm=='Dictionary':
        pm='BDictionary'
    elif pm=='Array':
        pm='ObjArray'
    elif pm=='BinaryFile':
        pm='BBinaryfile'
    elif pm=='Script':
        pm='ScriptExObjImp'
    elif pm=='Packet':
        pm='BPacket'
    elif pm=='Boat':
        pm='UBoat'
    elif pm=='Door':
        pm='UDoor'
    elif pm=='Client':
        pm='EClientRefObjImp'
    elif pm=='Account':
        pm='AccountObjImp'
    elif pm=='Datafile':
        pm='DataFileRefObjImp'
    elif pm=='Guild':
        pm='EGuildRefObjImp'
    elif pm=='Party':
        pm='EPartyRefObjImp'
    elif pm=='House':
        pm='UHouse'
    elif pm=='Lockable':
        pm='ULockable'
    elif pm=='Container':
        pm='UContainer'
    elif pm=='Corpse':
        pm='UCorpse'
    elif pm=='Plank':
        pm='UPlank'
    elif pm=='Weapon':
        pm='UWeapon'
    elif pm=='Multi':
        pm='UMulti'
    elif pm=='Armor':
        pm='UArmor'
    
    if pm in members:
        print('checking {}'.format(dc))
        for m in members[pm]:
            if m not in dm:
                print('   {} not in {}'.format(m,dc))
        for m in dm:
            if m not in members[pm]:
                print('   {} docentry not found'.format(m))
    else:
        print('Class {} not found'.format(pm))

