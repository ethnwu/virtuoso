/* Virtuoso feature engine. No network or storage access. MIT license. */
export const DEFAULT_WEIGHTS=[35,30,20,15];
export const FEATURE_NAMES=['Rhythmic density','Simultaneous notes','High register','Melodic leaps'];
export function scoreComponents(c,weights=DEFAULT_WEIGHTS){const sum=weights.reduce((a,b)=>a+b,0);if(sum<=0)throw Error('Choose at least one nonzero weight.');return c.reduce((a,v,i)=>a+v*weights[i]/sum,0);}
export function analyzeNotes(input){
 const notes=input.filter(n=>Number.isFinite(n.start)&&Number.isFinite(n.end)&&n.end>n.start&&Number.isFinite(n.pitch)).sort((a,b)=>a.start-b.start||a.pitch-b.pitch);
 if(!notes.length)throw Error('This part contains no complete pitched notes.');
 const groups=new Map();let first=Infinity,last=-Infinity,low=127,high=0,highCount=0;
 for(const n of notes){first=Math.min(first,n.start);last=Math.max(last,n.end);low=Math.min(low,n.pitch);high=Math.max(high,n.pitch);if(n.pitch>=84)highCount++;const t=Math.round(n.start*1e8)/1e8;if(!groups.has(t))groups.set(t,[]);groups.get(t).push(n.pitch);}
 const tops=[...groups.values()].map(p=>Math.max(...p));let totalLeap=0;for(let i=1;i<tops.length;i++)totalLeap+=Math.abs(tops[i]-tops[i-1]);
 const raw={noteEvents:notes.length,onsets:groups.size,quarterBeats:last-first,density:notes.length/(last-first),chords:[...groups.values()].filter(p=>p.length>1).length/groups.size*100,register:highCount/notes.length*100,leaps:tops.length>1?totalLeap/(tops.length-1):0,low,high};
 const components=[Math.min(100,raw.density/8*100),Math.min(100,raw.chords/60*100),Math.min(100,raw.register/50*100),Math.min(100,raw.leaps/12*100)];
 const windows=new Map();for(const n of notes){const k=Math.floor(n.start/16);if(!windows.has(k))windows.set(k,{window:k+1,start:k*16,end:(k+1)*16,count:0,low:127,high:0});const w=windows.get(k);w.count++;w.low=Math.min(w.low,n.pitch);w.high=Math.max(w.high,n.pitch);}
 return {raw,components,index:scoreComponents(components),notes,passages:[...windows.values()].sort((a,b)=>a.start-b.start)};
}
export function parseMidi(buffer){
 const b=buffer instanceof Uint8Array?buffer:new Uint8Array(buffer);let p=0;const u16=()=>{if(p+2>b.length)throw Error('Truncated MIDI.');const n=b[p]*256+b[p+1];p+=2;return n;};const u32=()=>{if(p+4>b.length)throw Error('Truncated MIDI.');const n=(b[p]*16777216)+(b[p+1]<<16)+(b[p+2]<<8)+b[p+3];p+=4;return n;};const str=n=>{const s=new TextDecoder().decode(b.subarray(p,p+n));p+=n;return s;};
 if(str(4)!=='MThd')throw Error('This is not a Standard MIDI file.');const hl=u32(),format=u16(),nt=u16(),division=u16();if(hl<6||hl>1024||nt>256||format>1)throw Error('Unsupported MIDI header or asynchronous format.');if(division&0x8000||!division)throw Error('SMPTE MIDI timing is unsupported; export with quarter-note timing.');p=8+hl;
 const parts=[];let unmatched=0;
 for(let ti=0;ti<nt;ti++){
  if(str(4)!=='MTrk')throw Error('Missing MIDI track chunk.');const len=u32(),end=p+len;if(end>b.length)throw Error('Truncated MIDI track.');let tick=0,running=0,name='',events=0;const active=new Map(),channelNotes=new Map();
  const vl=()=>{let n=0;for(let i=0;i<4;i++){if(p>=end)throw Error('Truncated MIDI event.');const x=b[p++];n=n*128+(x&127);if(!(x&128))return n;}throw Error('Invalid MIDI variable-length value.');};
  while(p<end){if(++events>1000000)throw Error('This MIDI has too many events.');tick+=vl();let s=b[p++];if(s<128){if(!running)throw Error('Invalid MIDI running status.');p--;s=running;}else if(s<240)running=s;
   if(s===255){const type=b[p++],n=vl();if(p+n>end)throw Error('Truncated MIDI metadata.');if(type===3)name=new TextDecoder().decode(b.subarray(p,p+n));p+=n;continue;}
   if(s===240||s===247){const n=vl();p+=n;if(p>end)throw Error('Truncated MIDI SysEx.');running=0;continue;}
   if(s>=240)throw Error('Unsupported MIDI system event.');const type=s>>4,ch=s&15;const d1=b[p++];const d2=type===12||type===13?0:b[p++];if(p>end||d1>127||d2>127)throw Error('Invalid MIDI event data.');if(ch===9)continue;
   const key=ch+':'+d1;
   if(type===9&&d2>0){if(!active.has(key))active.set(key,[]);active.get(key).push(tick);}
   if(type===8||(type===9&&d2===0)){const q=active.get(key);if(q?.length){const start=q.shift();if(tick>start){if(!channelNotes.has(ch))channelNotes.set(ch,[]);channelNotes.get(ch).push({start:start/division,end:tick/division,pitch:d1});}}else unmatched++;}
  }
  for(const q of active.values())unmatched+=q.length;
  for(const [ch,notes] of channelNotes)if(notes.length)parts.push({id:ti+':'+ch,label:(name||'Track '+ti)+' · channel '+(ch+1),track:ti,channel:ch,notes});p=end;
 }
 if(!parts.length)throw Error('No pitched note tracks found. Percussion is excluded.');return {format:'MIDI',parts,warnings:unmatched?[unmatched+' unmatched note events were omitted.']:[]};
}
const children=(e,n)=>[...e.children].filter(c=>c.localName===n);
const child=(e,n)=>children(e,n)[0];
const txt=(e,n)=>child(e,n)?.textContent.trim()||'';
export function parseMusicXML(text,Parser=globalThis.DOMParser){
 if(!Parser)throw Error('MusicXML parsing requires a browser DOM parser.');
 const doc=new Parser().parseFromString(text,'application/xml');if(doc.querySelector('parsererror'))throw Error('The MusicXML document is malformed.');const root=doc.documentElement;
 if(root.localName!=='score-partwise')throw Error('Export as partwise MusicXML (.musicxml). Timewise files are not supported.');
 const labels=new Map();for(const list of children(root,'part-list'))for(const p of children(list,'score-part'))labels.set(p.getAttribute('id'),txt(p,'part-name'));
 let repeats=false,graces=0;const parts=[];
 for(const [partIndex,part] of children(root,'part').entries()){
  let offset=0,div=1;const notes=[],ties=new Map();
  for(const measure of children(part,'measure')){
   let cursor=0,max=0,lastStart=0;
   for(const e of [...measure.children]){
    if(e.localName==='attributes'){const d=Number(txt(e,'divisions'));if(d>0)div=d;continue;}
    if(e.localName==='barline'&&child(e,'repeat'))repeats=true;
    if(e.localName==='backup'||e.localName==='forward'){const q=Number(txt(e,'duration'))/div;if(!Number.isFinite(q)||q<0)throw Error('Invalid MusicXML timing.');cursor+=(e.localName==='backup'?-q:q);if(cursor<-.00001)throw Error('MusicXML voice timing extends before a measure.');max=Math.max(max,cursor);continue;}
    if(e.localName!=='note')continue;if(child(e,'grace')){graces++;continue;}
    const dur=Number(txt(e,'duration'))/div;if(!Number.isFinite(dur)||dur<=0)continue;const chord=!!child(e,'chord');const start=chord?lastStart:cursor;if(!chord){lastStart=start;cursor+=dur;}max=Math.max(max,start+dur,cursor);
    const pitch=child(e,'pitch');if(!pitch)continue;const steps={C:0,D:2,E:4,F:5,G:7,A:9,B:11};const step=txt(pitch,'step'),oct=Number(txt(pitch,'octave')),alter=Number(txt(pitch,'alter')||0);if(!(step in steps)||!Number.isFinite(oct)||!Number.isFinite(alter))throw Error('Invalid MusicXML pitch.');const midi=(oct+1)*12+steps[step]+alter;if(midi<0||midi>127)throw Error('Pitch is outside the supported range.');
    const types=children(e,'tie').map(t=>t.getAttribute('type'));const key=(txt(e,'voice')||'1')+':'+midi;
    if(types.includes('stop')&&ties.has(key)){const old=ties.get(key);old.end=offset+start+dur;if(!types.includes('start'))ties.delete(key);}
    else {const n={start:offset+start,end:offset+start+dur,pitch:midi};notes.push(n);if(types.includes('start'))ties.set(key,n);}
   }
   offset+=max;
  }
  if(notes.length>200000)throw Error('This part has too many notes.');if(notes.length)parts.push({id:String(partIndex),label:labels.get(part.getAttribute('id'))||'Part '+(partIndex+1),notes});
 }
 if(!parts.length)throw Error('No pitched parts were found.');const warnings=['Written durations are analyzed; notation-specific bowing, fingering and expression are not scored.'];if(repeats)warnings.push('Repeats are not unfolded; this is the written traversal.');if(graces)warnings.push(graces+' grace notes are omitted because they have no written duration.');
 return {format:'MusicXML',parts,warnings};
}
export function pitchName(n){const names=['C','C♯','D','E♭','E','F','F♯','G','A♭','A','B♭','B'];const m=Math.round(n);return names[((m%12)+12)%12]+(Math.floor(m/12)-1);}
export function nearest(result,pieces,weights=DEFAULT_WEIGHTS){const total=weights.reduce((a,b)=>a+b,0);return pieces.map(p=>({...p,distance:Math.sqrt(p.components.reduce((a,v,i)=>a+(v-result.components[i])**2*weights[i]/total,0))})).sort((a,b)=>a.distance-b.distance);}
export function resultExport(result,name,part,weights=DEFAULT_WEIGHTS){return {project:'Virtuoso',version:'1.0',file:name,part,index_type:'Experimental rules-based technical-demand index; not a predicted exam grade',index:scoreComponents(result.components,weights),weights,features:result.raw,components:Object.fromEntries(FEATURE_NAMES.map((n,i)=>[n,result.components[i]])),passages:result.passages};}
