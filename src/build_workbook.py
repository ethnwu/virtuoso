"""Generate the editable Tableau starter and package its CSV sources.
Generated XML is structurally checked; opening in Tableau is a separate QA step.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import csv, zipfile, uuid, shutil
ROOT=Path(__file__).resolve().parents[1]
def sub(p,tag,text=None,**attrs):
    el=E.SubElement(p,tag,{k.rstrip('_').replace('__','-'):str(v) for k,v in attrs.items()})
    if text is not None: el.text=text
    return el
NUM={'Movement Order','Virtuoso Index','Noteheads','Onsets','Quarter Beats','Notes per Quarter','Chord Onsets Pct','High Notes Pct','Mean Leap Semitones','Lowest MIDI','Highest MIDI','Feature Score','Weight','Weighted Contribution'}
def col(p,f):
    return sub(p,'column',name=f'[{f}]',datatype='real' if f in NUM else 'string',role='measure' if f in NUM else 'dimension',type='quantitative' if f in NUM else 'nominal')
def instance(p,f):
    n=f'[sum:{f}:qk]' if f in NUM else f'[none:{f}:nk]'
    sub(p,'column-instance',column=f'[{f}]',derivation='Sum' if f in NUM else 'None',name=n,pivot='key',type='quantitative' if f in NUM else 'nominal')
    return n
w=E.Element('workbook',{'original-version':'18.1','source-build':'2024.1.0 (20241.24.0314.1442)','source-platform':'mac','version':'18.1'})
sub(w,'document-format-change-manifest')
prefs=sub(w,'preferences');sub(prefs,'preference',name='ui.encoding.shelf.height',value='24')
dss=sub(w,'datasources');fields={}
for name,file in [('pieces','pieces.csv'),('features','features.csv')]:
    with (ROOT/'data'/file).open() as f: fields[name]=next(csv.reader(f))
    ds=sub(dss,'datasource',caption='Virtuoso — '+name,inline='true',name=name,version='18.1')
    conn=sub(ds,'connection',class_='textscan',directory='Data',filename=file,**{'password':'','server':'','textscan-character-set':'UTF-8','textscan-locale':'en_US','textscan-sort-as-text':'true','version':'9.3'})
    rel=sub(conn,'relation',name=file,table=f'[{file}]',type='table')
    cs=sub(rel,'columns',**{'character-set':'UTF-8','header':'yes','locale':'en_US','separator':',','width':'0'})
    for i,f in enumerate(fields[name]): sub(cs,'column',name=f,datatype='real' if f in NUM else 'string',ordinal=i)
    sub(ds,'aliases',enabled='yes')
    for f in fields[name]:
        c=col(ds,f)
        if f in NUM: c.set('default-format','n0.0')
    sub(ds,'layout',**{'dim-ordering':'alphabetic','measure-ordering':'alphabetic','show-structure':'true'})
works=sub(w,'worksheets')
def sheet(name,ds,rows,cols,mark,encodings):
    s=sub(works,'worksheet',name=name)
    title=sub(sub(s,'layout-options'),'title');ft=sub(title,'formatted-text');sub(ft,'run',name,**{'fontname':'Avenir Next','fontsize':'14','bold':'true'})
    t=sub(s,'table');v=sub(t,'view');sources=sub(v,'datasources');sub(sources,'datasource',caption='Virtuoso — '+ds,name=ds)
    dep=sub(v,'datasource-dependencies',datasource=ds)
    used=list(dict.fromkeys([*rows,*cols,*[f for _,f in encodings]]));ins={}
    for f in used: col(dep,f)
    for f in used: ins[f]=instance(dep,f)
    sub(v,'aggregation',value='true')
    style=sub(t,'style');rule=sub(style,'style-rule',element='worksheet');sub(rule,'format',attr='background-color',value='#fbf8f1')
    panes=sub(t,'panes');pane=sub(panes,'pane',**{'selection-relaxation-option':'selection-relaxation-allow'})
    pv=sub(pane,'view');sub(pv,'breakdown',value='auto');sub(pane,'mark',class_=mark)
    enc=sub(pane,'encodings')
    for kind,f in encodings: sub(enc,kind,column=f'[{ds}].{ins[f]}')
    st=sub(pane,'style');r=sub(st,'style-rule',element='mark');sub(r,'format',attr='color',value='#97602e');sub(r,'format',attr='mark-labels-show',value='true')
    sub(t,'rows',' / '.join(f'[{ds}].{ins[f]}' for f in rows))
    sub(t,'cols',' / '.join(f'[{ds}].{ins[f]}' for f in cols))
    sub(s,'simple-id',uuid='{'+str(uuid.uuid5(uuid.NAMESPACE_URL,'virtuoso/'+name)).upper()+'}')
    return s
sheet('01 — Technical demand index','pieces',['Piece'],['Virtuoso Index'],'Bar',[('text','Virtuoso Index')])
sheet('02 — Density versus chord frequency','pieces',['Chord Onsets Pct'],['Notes per Quarter'],'Circle',[('lod','Piece'),('text','Piece'),('size','Virtuoso Index')])
sheet('03 — Technical profiles','features',['Piece'],['Feature'],'Square',[('color','Feature Score'),('text','Feature Score')])
sheet('04 — Pitch range','pieces',['Piece'],['Highest MIDI'],'Bar',[('text','Highest MIDI')])
dashboards=sub(w,'dashboards');d=sub(dashboards,'dashboard',name='Virtuoso');sub(d,'style');sub(d,'size',maxheight=900,maxwidth=1400,minheight=900,minwidth=1400)
zones=sub(d,'zones');root=sub(zones,'zone',id=0,type__v2='layout-basic',x=0,y=0,w=100000,h=100000)
tz=sub(root,'zone',id=1,type__v2='text',x=1500,y=1000,w=97000,h=12000)
ft=sub(tz,'formatted-text');sub(ft,'run','VIRTUOSO  /  The data behind violin difficulty\n',fontname='Avenir Next',fontsize='27',bold='true',fontcolor='#24382c')
sub(ft,'run','Bach pilot · Eight movements · Experimental technical-demand index, not a validated difficulty grade',fontname='Avenir Next',fontsize='11',fontcolor='#59685c')
for i,(name,x,y,ww,hh) in enumerate([('01 — Technical demand index',1500,15000,47000,38000),('02 — Density versus chord frequency',51000,15000,47500,38000),('03 — Technical profiles',1500,55000,97000,35000)],2):
    z=sub(root,'zone',id=i,name=name,x=x,y=y,w=ww,h=hh);zs=sub(z,'zone-style');sub(zs,'format',attr='margin',value=10);sub(zs,'format',attr='border-style',value='none')
tz=sub(root,'zone',id=5,type__v2='text',x=1500,y=92000,w=97000,h=6500)
ft=sub(tz,'formatted-text');sub(ft,'run','Index: 35% density + 30% chords + 20% high register + 15% leaps. Weights and scale anchors are provisional. Tempo, bowing, fingering, musicality, and performer validation are not included. Source: Mutopia Project / Erik Sandberg, public domain.',fontname='Avenir Next',fontsize=10)
sub(d,'simple-id',uuid='{'+str(uuid.uuid5(uuid.NAMESPACE_URL,'virtuoso/dashboard')).upper()+'}')
wins=sub(w,'windows',**{'saved-dpi-scale-factor':'1.0','source-height':'1000'})
for name in ['01 — Technical demand index','02 — Density versus chord frequency','03 — Technical profiles','04 — Pitch range']:
    win=sub(wins,'window',class_='worksheet',name=name);sub(win,'viewpoint',name=name).append(E.Element('zoom',{'type':'entire-view'}))
win=sub(wins,'window',class_='dashboard',name='Virtuoso');vps=sub(win,'viewpoints')
for name in ['01 — Technical demand index','02 — Density versus chord frequency','03 — Technical profiles']:
    sub(sub(vps,'viewpoint',name=name),'zoom',type='entire-view')
sub(win,'active',id='-1')
E.indent(w)
out=ROOT/'tableau';out.mkdir(exist_ok=True)
p=out/'Virtuoso.twb';E.ElementTree(w).write(p,encoding='utf-8',xml_declaration=True)
(out/'Data').mkdir(exist_ok=True)
for f in ['pieces.csv','features.csv']: shutil.copy(ROOT/'data'/f,out/'Data'/f)
with zipfile.ZipFile(out/'Virtuoso.twbx','w',zipfile.ZIP_DEFLATED) as z:
    z.write(p,'Virtuoso.twb')
    for f in ['pieces.csv','features.csv']: z.write(ROOT/'data'/f,'Data/'+f)
# Structural checks do not substitute for Tableau application rendering.
parsed=E.parse(p);assert len(parsed.findall('.//worksheet'))==4
for ds in parsed.findall('./datasources/datasource'):
    f=ds.find('connection').get('filename');assert (out/'Data'/f).exists()
with zipfile.ZipFile(out/'Virtuoso.twbx') as z: assert z.testzip() is None
print('Created TWB + TWBX; XML, CSV paths, four worksheets and ZIP integrity checked.')
