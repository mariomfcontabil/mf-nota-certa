from config import BASE, ROOT
from os import environ
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from PIL import Image
from pypdf import PdfReader


out=Path('tutorial-mf-nota-certa.pdf')
W,H=450,840
pdf=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1,invariant=1)
pdf.setTitle('MF Nota Certa - Guia rápido')
pdf.setAuthor('MF Contábil e Sistemas')
m=28
width=W-2*m
gold=HexColor('#F2C266')
ink=HexColor('#221B13')
muted=HexColor('#574B3D')
cream=HexColor('#FCFAF6')
base=BASE
logo=Image.open(ROOT / 'mf-ativo-1.webp').convert('RGBA')
logo=logo.crop(logo.getbbox())
logo.thumbnail((190,155),Image.Resampling.LANCZOS)
ASSETS=Path(environ["MF_CAPTURAS"])
images={i:Image.open(ASSETS / f'tutorial-painel-{i}.jpg') for i in (0,1,2,4,5)}

def para(text,y,size=12,leading=17,color=ink):
    p=Paragraph(text,ParagraphStyle('guide',fontName='Helvetica',fontSize=size,leading=leading,textColor=color,spaceAfter=0))
    _,h=p.wrap(width,700)
    p.drawOn(pdf,m,y-h)
    return y-h

def picture(im,y,max_w=width):
    w=min(max_w,im.width)
    h=w*im.height/im.width
    pdf.drawImage(ImageReader(im),m,y-h,width=w,height=h)
    pdf.setStrokeColor(HexColor('#BBA88A'))
    pdf.rect(m,y-h,w,h,stroke=1,fill=0)
    return y-h

def header(title,subtitle):
    pdf.setFillColor(cream);pdf.rect(0,0,W,H,stroke=0,fill=1)
    pdf.setFillColor(HexColor('#211B15'));pdf.rect(0,H-112,W,112,stroke=0,fill=1)
    pdf.setFillColor(gold);pdf.rect(0,H-114,W,2,stroke=0,fill=1)
    pdf.drawImage(ImageReader(logo),m,H-84,width=57,height=57*logo.height/logo.width,mask='auto')
    pdf.setFillColor(gold);pdf.setFont('Helvetica-Bold',23);pdf.drawString(m+68,H-49,title)
    pdf.setFillColor(HexColor('#EFE3D2'));pdf.setFont('Helvetica',11);pdf.drawString(m+68,H-69,subtitle)
    return H-134

def section(n,title,y):
    return para(f'<b>{n}. {title}</b>',y,15,19)-6

def footer(page):
    pdf.setStrokeColor(HexColor('#D8CBB8'));pdf.line(m,45,W-m,45)
    pdf.setFont('Helvetica-Bold',10);pdf.setFillColor(HexColor('#72500F'))
    pdf.drawString(m,27,'Abrir MF Nota Certa')
    pdf.linkURL(base,(m,23,m+110,39),relative=0,thickness=0)
    pdf.setFillColor(muted);pdf.setFont('Helvetica',9);pdf.drawRightString(W-m,27,f'{page} / 4')
    pdf.showPage()

y=header('MF Nota Certa','Guia rápido de preenchimento da NFS-e')
y=para('<b>Tela principal</b>',y,18,23)-12
y=para('Ao abrir o MF Nota Certa, você verá o <b>logo da MF</b> em destaque no cabeçalho e poderá escolher o modo de consulta.',y)-12
home=Image.open(ASSETS / 'tutorial-logo.jpg')
y=picture(home,y)-18
y=para('<b>Consulta simples</b> para buscar pelo nome do serviço e conferir os códigos.',y)-9
y=para('<b>Consulta avançada</b> para preencher os dados da operação, conferir os tributos e gerar a prévia da nota.',y)
assert y>=52,y
footer(1)

y=header('MF Nota Certa','Guia rápido de preenchimento da NFS-e')
y=para('<b>Consulta simples</b>',y,18,23)-13
y=section(1,'Busque pelo nome do serviço',y)
y=para('Abra <b>Consulta simples</b> e digite o que foi feito, por exemplo, <b>limpeza de escritório</b>. Toque na sugestão que descreve o serviço prestado.',y)-9
y=picture(images[0],y)-18
y=section(2,'Consulte e confira o resultado',y)
y=para('Toque em <b>Consultar serviço</b>. Confira a atividade e use os botões <b>Copiar Código nacional</b> e <b>Copiar NBS</b> para usar os códigos no emissor.',y)-9
y=picture(images[1],y,300)-13
y=para('Para calcular os tributos ou gerar a prévia, toque em <b>Continuar na consulta avançada</b>.',y,11,15,muted)
assert y>=52,y
footer(2)

y=header('MF Nota Certa','Consulta avançada')
y=section(1,'Escolha a atividade e o serviço',y)
y=para('Abra <b>Consulta avançada</b>. Selecione o <b>CNAE</b> e o <b>serviço realizado</b> e descreva o que foi feito conforme o contrato.',y)-10
y=picture(images[2],y,265)-15
y=section(2,'Preencha os dados e consulte',y)
y=para('O regime começa em <b>Simples Nacional</b>, e os municípios do prestador e da execução começam em <b>Altamira/PA</b>. Se houver dados salvos em <b>Minha empresa</b>, eles têm prioridade nos campos do prestador.',y,11,15)-9
y=picture(Image.open(ASSETS / 'tutorial-padroes.jpg'),y,345)-10
y=para('Se o serviço foi em outra cidade, substitua Altamira/PA no campo <b>Município onde o serviço foi realizado (UF)</b>. Exemplo: <b>Santarém/PA</b>. O município do prestador permanece como informado.',y,11,15)-8
y=para('Complete o tipo de tomador, a forma de contratação e o valor bruto. Toque em <b>Consultar preenchimento</b> e corrija os campos que o sistema indicar.',y,11,15)
assert y>=52,y
footer(3)

y=header('MF Nota Certa','Confira os dados e salve a prévia')
y=section(3,'Confira o resultado',y)
y=para('Use o <b>Checklist para preencher a nota</b> para revisar o <b>código de tributação</b>, a <b>NBS</b> e a descrição. Confira as retenções e o valor líquido, se aplicável. Resolva as pendências antes de emitir.',y)-9
y=picture(images[4],y)-16
y=section(4,'Gere a prévia da nota',y)
y=para('Abra <b>Dados para a prévia em PDF</b> e complete o que precisar. Toque em <b>Gerar PDF da prévia</b> e escolha <b>Salvar como PDF</b> na janela de impressão.',y)-9
y=picture(images[5],y,345)-10
y=para('<b>Sem valor fiscal.</b> Use a prévia para conferência. Emita a nota no portal autorizado.',y,10,14,muted)
assert y>=52,y
footer(4)
pdf.save()
verified=PdfReader(str(out))
assert len(verified.pages)==4
assert "Tela principal" in verified.pages[0].extract_text()
assert 'limpeza de escritório' in ' '.join(verified.pages[1].extract_text().split())
assert all(text in ' '.join(verified.pages[2].extract_text().split()) for text in ('Simples Nacional','Altamira/PA','Santarém/PA','Consultar preenchimento'))
assert 'Gerar PDF da prévia' in verified.pages[3].extract_text()
for page in verified.pages:
    assert page['/Annots'][0].get_object()['/A']['/URI']==base
