"""Add reviewer tags to current marked PDF without changing manuscript layout."""
from pathlib import Path
from io import BytesIO
import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white

ANCHORS = [
 ('To support ubiquitous connectivity', 'R1-C5'),
 ('Each satellite can cover at most J cells and activate at most', 'R2-C3,R3-C2'),
 ('User-level resource allocation uses', 'R2-C6'),
 ('RT packets have a time-to-live', 'R2-C1,R2-C6'),
 ('The association remains fixed', 'R1-C1'),
 ('The overall utility combines', 'R2-C2'),
 ('Constraint C1 restricts illumination', 'R2-C3,R3-C2'),
 ('The optimized cell-satellite association matrix', 'R3-C4'),
 ('During offline centralized training', 'R1-C3,R3-C3'),
 ('The local observation is organized', 'R1-C4,R2-C5'),
 ('The critic receives the five features', 'R3-C3'),
 ('MAPPO uses the expected discounted return', 'R2-C2'),
 ('Fig. 2.', 'R2-C4,R2-C5'),
 ('For PPO updates', 'R2-C4'),
 ('Offline trajectories are collected', 'R1-C3'),
 ('All compared association schemes', 'R3-C1'),
 ('A controlled pairwise diagnostic evaluates', 'R1-C4,R2-C5'),
 ('Error bars in Figs.', 'R3-C6'),
 ('Fig. 6.', 'R3-C1,R3-C6'),
 ('Fig. 7.', 'R2-C1,R3-C6'),
 ('3) Ablation Analysis:', 'R2-C7'),
 ('Fig. 8.', 'R1-C4,R2-C5,R2-C7,R3-C6'),
 ('4) Hotspot-Reversal Sensitivity:', 'R1-C1'),
 ('5) ISA Parameter Sensitivity:', 'R1-C2'),
 ('Fig. 9.', 'R1-C2'),
 ('The actor forward-pass latency was measured', 'R1-C6,R3-C5'),
 ('7) Action-Delay Sensitivity:', 'R1-C6'),
]

def norm(s):
    return re.sub('[^a-z0-9]', '', s.lower())

def main(source, output, map_path):
    xml = subprocess.run(['pdftotext', '-bbox-layout', str(source), '-'], capture_output=True, check=True).stdout.decode('utf8')
    xml = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', xml)
    root = ET.fromstring(xml)
    pages = [e for e in root.iter() if e.tag.endswith('}page')]
    tags = []
    for phrase, ids in ANCHORS:
        target = norm(phrase)
        hits = []
        for pn, page in enumerate(pages,1):
            words = [e for e in page.iter() if e.tag.endswith('}word')]
            for i, w in enumerate(words):
                if not norm(w.text or ''):
                    continue
                value = ''
                for e in words[i:i+30]:
                    value += norm(e.text or '')
                    if value == target:
                        hits.append((pn,w))
                        break
                    if not target.startswith(value):
                        break
        assert len(hits) == 1, (phrase, [(n,w.text) for n,w in hits])
        pn,w = hits[0]
        names = ids.split(',')
        tags.append({'page':pn, 'anchor':phrase, 'ids':names,
                     'side':'left' if float(w.attrib['xMin'])<306 else 'right',
                     'desired_y':float(w.attrib['yMin']), 'height':len(names)*7+5})
    for pn in range(1,len(pages)+1):
        for side in ('left','right'):
            group = sorted((t for t in tags if t['page']==pn and t['side']==side),key=lambda t:t['desired_y'])
            bottom=40
            for t in group:
                t['y']=max(t['desired_y'],bottom+3)
                bottom=t['y']+t['height']
            if bottom>752:
                shift=bottom-752
                for t in group: t['y']-=shift
                assert group[0]['y']>=36
    covered={c for t in tags for c in t['ids']}
    expected={f'R{r}-C{c}' for r,n in [(1,6),(2,7),(3,6)] for c in range(1,n+1)}
    assert covered==expected, (covered,expected)
    reader=PdfReader(source)
    writer=PdfWriter(clone_from=reader)
    blue=Color(0,70/255,175/255)
    for pn,page in enumerate(writer.pages,1):
        buf=BytesIO()
        w,h=float(page.mediabox.width),float(page.mediabox.height)
        cv=canvas.Canvas(buf,pagesize=(w,h))
        cv.setFillColor(blue)
        if pn==1:
            cv.setFont('Helvetica',7)
            cv.drawCentredString(w/2,h-18,'Reviewer tags: Rn-Cm = Reviewer n, Comment m.')
        for t in (x for x in tags if x['page']==pn):
            x=3 if t['side']=='left' else w-42
            y=h-t['y']-t['height']
            cv.setFillColor(white);cv.setStrokeColor(blue);cv.setLineWidth(0.25)
            cv.rect(x,y,39,t['height'],stroke=1,fill=1)
            cv.setFillColor(blue);cv.setFont('Helvetica',6)
            for i,name in enumerate(t['ids']):
                cv.drawCentredString(x+19.5,h-t['y']-8-i*7,name)
            if abs(t['y']-t['desired_y'])>2:
                leader=x+39 if t['side']=='left' else x
                cv.line(leader,h-t['desired_y'],leader,h-t['y'])
        cv.save();buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
    writer.add_metadata({'/Title':'Marked Revised Manuscript with Reviewer Tags - TCCN-TP-26-1155'})
    with output.open('wb') as f: writer.write(f)
    map_path.write_text(json.dumps(tags,indent=2),encoding='utf8')
    print(json.dumps({'pages':len(pages),'tags':len(tags),'comments_covered':len(covered),'output':str(output)}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('map',type=Path)
    a=p.parse_args()
    main(a.source,a.output,a.map)
