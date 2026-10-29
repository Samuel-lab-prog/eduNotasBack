from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
GREEN = '#315F62'
INK = '#273536'
MUTED = '#687575'
PALE = '#EDF0EB'
LINE = '#D8DEDB'
TERRA = '#A66640'

def font(size, bold=False):
    file = Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf')
    return ImageFont.truetype(str(file), size) if file.exists() else ImageFont.load_default(size=size)

def centered(draw, box, text, fnt, fill=INK, gap=7):
    x1,y1,x2,y2=box
    words=text.split()
    lines=[]; line=''
    for word in words:
        test=f'{line} {word}'.strip()
        if draw.textbbox((0,0),test,font=fnt)[2] <= x2-x1-28: line=test
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    heights=[draw.textbbox((0,0),s,font=fnt)[3]-draw.textbbox((0,0),s,font=fnt)[1] for s in lines]
    y=y1+(y2-y1-(sum(heights)+gap*(len(lines)-1)))/2
    for s,h in zip(lines,heights):
        width=draw.textbbox((0,0),s,font=fnt)[2]
        draw.text((x1+(x2-x1-width)/2,y),s,font=fnt,fill=fill)
        y+=h+gap

def draw_actor(draw, x, y, scale=1):
    sw=max(3,round(4*scale)); r=19*scale
    draw.ellipse((x-r,y-145*scale-r,x+r,y-145*scale+r),outline=INK,width=sw)
    draw.line((x,y-126*scale,x,y-55*scale),fill=INK,width=sw)
    draw.line((x-40*scale,y-105*scale,x+40*scale,y-105*scale),fill=INK,width=sw)
    draw.line((x,y-55*scale,x-34*scale,y),fill=INK,width=sw)
    draw.line((x,y-55*scale,x+34*scale,y),fill=INK,width=sw)
    draw.text((x-60*scale,y+12*scale),'Professor',font=font(round(23*scale),True),fill=INK)

def dashed_arrow(draw, start, end, label=None):
    x1,y1=start; x2,y2=end
    length=((x2-x1)**2+(y2-y1)**2)**.5
    if length==0:return
    ux=(x2-x1)/length; uy=(y2-y1)/length
    step=20
    p=0
    while p < length-18:
        q=min(p+11,length-18)
        draw.line((x1+ux*p,y1+uy*p,x1+ux*q,y1+uy*q),fill=MUTED,width=3)
        p+=step
    ax=x2-ux*18; ay=y2-uy*18
    draw.line((ax-uy*10,ay+ux*10,x2,y2),fill=MUTED,width=3)
    draw.line((ax+uy*10,ay-ux*10,x2,y2),fill=MUTED,width=3)
    if label:
        mx=(x1+x2)/2; my=(y1+y2)/2
        draw.text((mx-38,my-29),label,font=font(16,True),fill=MUTED)

def diagrams():
    folder=DOCS/'01-modelagem'/'diagrams'; folder.mkdir(parents=True,exist_ok=True)
    # Main use case diagram.
    im=Image.new('RGB',(1700,1050),'white'); d=ImageDraw.Draw(im)
    d.text((70,42),'EduNotas — casos de uso',font=font(34,True),fill=INK)
    boundary=(310,120,1620,960); d.rounded_rectangle(boundary,radius=10,outline=GREEN,width=4)
    d.text((340,140),'Sistema EduNotas',font=font(24,True),fill=GREEN)
    actor=(135,595); labels=[('Acessar sistema',570,275),('Entrar como professor',1110,275),('Consultar alunos',570,465),('Cadastrar aluno',1110,465),('Consultar notas do aluno',570,700),('Editar notas do aluno',1110,700)]
    for _,cx,cy in labels:
        d.line((actor[0]+60,actor[1]-10,cx-160,cy),fill='#8B9692',width=2)
    for label,cx,cy in labels:
        box=(cx-160,cy-47,cx+160,cy+47); d.ellipse(box,fill='#F7F8F6',outline=GREEN,width=3); centered(d,box,label,font(22,True))
    draw_actor(d,*actor,scale=.85)
    im.save(folder/'casos-de-uso.png')

    # Expanded use cases with the included validation and database work.
    im=Image.new('RGB',(1800,1120),'white'); d=ImageDraw.Draw(im)
    d.text((60,35),'EduNotas — fluxos expandidos',font=font(34,True),fill=INK)
    boundary=(245,115,1735,1060); d.rounded_rectangle(boundary,radius=10,outline=GREEN,width=4)
    d.text((275,135),'Sistema EduNotas',font=font(23,True),fill=GREEN)
    actor=(105,625); draw_actor(d,*actor,scale=.72)
    main=[('Cadastrar aluno',520,300),('Consultar notas',520,575),('Editar notas',520,850)]
    included=[('Validar dados',1180,260),('Gravar aluno\nno PostgreSQL',1180,420),('Calcular média',1180,575),('Validar notas\nde 0 a 10',1180,745),('Gravar notas\nno PostgreSQL',1180,920)]
    for _,cx,cy in main: d.line((actor[0]+52,actor[1]-8,cx-155,cy),fill='#8B9692',width=2)
    for label,cx,cy in included:
        box=(cx-172,cy-44,cx+172,cy+44); d.ellipse(box,fill='#F7F8F6',outline=GREEN,width=3); centered(d,box,label.replace('\n',' '),font(21,True))
    for label,cx,cy in main:
        box=(cx-155,cy-44,cx+155,cy+44); d.ellipse(box,fill='#E9EFED',outline=GREEN,width=3); centered(d,box,label,font(21,True))
    dashed_arrow(d,(675,300),(1008,260),'<<include>>')
    dashed_arrow(d,(675,315),(1008,420),'<<include>>')
    dashed_arrow(d,(675,575),(1008,575),'<<include>>')
    dashed_arrow(d,(675,850),(1008,745),'<<include>>')
    dashed_arrow(d,(675,865),(1008,920),'<<include>>')
    dashed_arrow(d,(675,835),(1008,610),'<<include>>')
    d.text((275,1000),'Média = (nota 1 + nota 2) / 2. O valor é calculado e não armazenado.',font=font(18),fill=MUTED)
    im.save(folder/'casos-de-uso-expandido.png')

    # Domain class diagram.
    im=Image.new('RGB',(1700,780),'white'); d=ImageDraw.Draw(im)
    d.text((70,38),'EduNotas — classes do domínio',font=font(34,True),fill=INK)
    def class_box(x,y,w,h,title,rows,footer=None):
        d.rounded_rectangle((x,y,x+w,y+h),radius=8,fill='white',outline=GREEN,width=3)
        d.rectangle((x,y,x+w,y+58),fill='#E9EFED')
        centered(d,(x,y+3,x+w,y+55),title,font(24,True),GREEN)
        yy=y+82
        for row in rows:
            d.text((x+20,yy),row,font=font(20),fill=INK); yy+=40
        if footer:
            d.line((x,y+h-85,x+w,y+h-85),fill=LINE,width=2)
            centered(d,(x+10,y+h-78,x+w-10,y+h-8),footer,font(18),MUTED)
    class_box(105,160,530,390,'Professor',['id: String','name: String','email: String','passwordHash: String'])
    class_box(1055,160,530,490,'Aluno',['id: String','name: String','registration: String','classroom: String','grade1: Decimal','grade2: Decimal','teacherId: String'],'calcularMedia() = (grade1 + grade2) / 2')
    y=355; d.line((635,y,1055,y),fill=INK,width=3); d.polygon([(1055,y),(1035,y-10),(1035,y+10)],fill=INK)
    d.text((655,y-42),'1',font=font(18,True),fill=INK); d.text((1004,y-42),'0..*',font=font(18,True),fill=INK)
    d.text((735,y+15),'possui',font=font(18),fill=MUTED)
    d.text((105,690),'A média é calculada na API. A matrícula é única para cada professor.',font=font(20),fill=MUTED)
    im.save(folder/'classes.png')
    return folder

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill.lstrip('#')); tcPr.append(shd)

def cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr(); tcMar=tcPr.first_child_found_in('w:tcMar')
    if tcMar is None: tcMar=OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for m,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node=tcMar.find(qn(f'w:{m}'))
        if node is None: node=OxmlElement(f'w:{m}'); tcMar.append(node)
        node.set(qn('w:w'),str(v)); node.set(qn('w:type'),'dxa')

def set_font(run, size=11, color=INK, bold=False, name='Arial'):
    run.font.name=name; run._element.rPr.rFonts.set(qn('w:eastAsia'),name)
    run.font.size=Pt(size); run.font.color.rgb=RGBColor.from_string(color.lstrip('#')); run.bold=bold

def add_rich(paragraph,text,size=11,color=INK):
    pattern=re.compile(r'(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)')
    cursor=0
    for match in pattern.finditer(text):
        if match.start()>cursor: set_font(paragraph.add_run(text[cursor:match.start()]),size,color)
        token=match.group()
        if token.startswith('**'): set_font(paragraph.add_run(token[2:-2]),size,color,True)
        elif token.startswith('`'): set_font(paragraph.add_run(token[1:-1]),size,GREEN,False,'Consolas')
        else:
            r=paragraph.add_run(token[1:-1]); set_font(r,size,color); r.italic=True
        cursor=match.end()
    if cursor<len(text): set_font(paragraph.add_run(text[cursor:]),size,color)

def add_table(doc, lines):
    rows=[]
    for idx,line in enumerate(lines):
        cells=[part.strip() for part in line.strip('|').split('|')]
        if idx==1 and all(re.fullmatch(r':?-{3,}:?',part) for part in cells): continue
        rows.append(cells)
    if not rows:return
    columns=max(map(len,rows)); table=doc.add_table(rows=1,cols=columns); table.autofit=False
    table.style='Table Grid'
    for ri,row in enumerate(rows):
        cells=table.rows[0].cells if ri==0 else table.add_row().cells
        for ci in range(columns):
            value=row[ci] if ci<len(row) else ''
            cell=cells[ci]; cell.text=''; cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(0); p.paragraph_format.line_spacing=1.05
            add_rich(p,value,10 if columns<=3 else 9, 'FFFFFF' if ri==0 else INK)
            if ri==0:
                for run in p.runs: run.bold=True
                shade(cell,GREEN)
            elif ri%2==0: shade(cell,'F4F3EE')
            cell_margins(cell)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)

def add_image(doc,path,width=6.75):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(5); p.paragraph_format.space_after=Pt(8)
    p.add_run().add_picture(str(path),width=Inches(width))

def next_content(lines,index):
    return next((line.strip() for line in lines[index+1:] if line.strip()),'')

def build_doc(folder,filename,diagram_dir):
    md=DOCS/folder/'README.md'; lines=md.read_text(encoding='utf-8').splitlines()
    doc=Document(); section=doc.sections[0]
    section.page_width=Inches(8.5); section.page_height=Inches(11)
    section.left_margin=Inches(.72); section.right_margin=Inches(.72); section.top_margin=Inches(.68); section.bottom_margin=Inches(.65)
    normal=doc.styles['Normal']; normal.font.name='Arial'; normal._element.rPr.rFonts.set(qn('w:eastAsia'),'Arial'); normal.font.size=Pt(11); normal.font.color.rgb=RGBColor.from_string(INK.lstrip('#'))
    normal.paragraph_format.space_after=Pt(6); normal.paragraph_format.line_spacing=1.12
    for style_name,size in [('Heading 1',17),('Heading 2',13)]:
        style=doc.styles[style_name]; style.font.name='Arial'; style._element.rPr.rFonts.set(qn('w:eastAsia'),'Arial'); style.font.size=Pt(size); style.font.bold=True; style.font.color.rgb=RGBColor.from_string(GREEN.lstrip('#')); style.paragraph_format.space_before=Pt(12); style.paragraph_format.space_after=Pt(5); style.paragraph_format.keep_with_next=True
    title=doc.styles['Title']; title.font.name='Arial'; title._element.rPr.rFonts.set(qn('w:eastAsia'),'Arial'); title.font.size=Pt(24); title.font.bold=True; title.font.color.rgb=RGBColor.from_string('000000'); title.paragraph_format.space_after=Pt(7)
    # Plain running header/footer.
    header=section.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    set_font(header.add_run('EDUNOTAS  |  TRABALHO ACADÊMICO'),8,MUTED,True)
    footer=section.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    set_font(footer.add_run('EduNotas  ·  '),8,MUTED)
    field=OxmlElement('w:fldSimple'); field.set(qn('w:instr'),'PAGE'); footer._p.append(field)

    i=0; in_code=False; code=[]; image_count=0; doc1_figures={'casos-de-uso.puml':'casos-de-uso.png','casos-de-uso-expandido.puml':'casos-de-uso-expandido.png','classes.puml':'classes.png'}
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            if in_code:
                p=doc.add_paragraph(); p.paragraph_format.left_indent=Inches(.18); p.paragraph_format.space_after=Pt(7)
                for j,part in enumerate(code):
                    if j: p.add_run().add_break()
                    run=p.add_run(part); set_font(run,9,INK,False,'Consolas')
                code=[]; in_code=False
            else: in_code=True
            i+=1; continue
        if in_code: code.append(line); i+=1; continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].startswith('|'): block.append(lines[i]); i+=1
            add_table(doc,block); continue
        image=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if image:
            if image_count and folder!='03-design-telas': doc.add_page_break()
            image_count+=1
            add_image(doc,(md.parent/image.group(2)).resolve())
            i+=1; continue
        if line.startswith('# '):
            p=doc.add_paragraph(style='Title'); add_rich(p,line[2:],24,'000000')
        elif line.startswith('## '):
            following=next_content(lines,i)
            if folder=='03-design-telas' and image_count and following.startswith('!['): doc.add_page_break()
            p=doc.add_paragraph(style='Heading 1'); add_rich(p,line[3:],17,GREEN,)
        elif line.startswith('### '):
            p=doc.add_paragraph(style='Heading 2'); add_rich(p,line[4:],13,GREEN)
        elif line.startswith('- '):
            p=doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after=Pt(3); add_rich(p,line[2:],10.5,INK)
        elif re.match(r'^\d+\. ',line):
            p=doc.add_paragraph(style='List Number'); p.paragraph_format.space_after=Pt(4); add_rich(p,re.sub(r'^\d+\. ','',line),10.5,INK)
        elif line.strip():
            p=doc.add_paragraph(); add_rich(p,line,10.5,INK)
            if folder=='01-modelagem':
                for source,image_name in doc1_figures.items():
                    if source in line:
                        doc.add_page_break(); add_image(doc,diagram_dir/image_name,6.7)
        else:
            if not (doc.paragraphs and doc.paragraphs[-1].text==''): doc.add_paragraph().paragraph_format.space_after=Pt(1)
        i+=1
    out=md.parent/filename; doc.save(out); print(out)

if __name__=='__main__':
    diagram_dir=diagrams()
    build_doc('01-modelagem','entrega-01-modelagem.docx',diagram_dir)
    build_doc('02-wireframe-moodboard','entrega-02-wireframes.docx',diagram_dir)
    build_doc('03-design-telas','entrega-03-telas.docx',diagram_dir)
    build_doc('04-design-system','entrega-04-design-system.docx',diagram_dir)
