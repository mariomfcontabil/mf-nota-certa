from config import BASE, PDF_URL, ASSETS, ROOT
from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode.qrencoder import QRCode, QRErrorCorrectLevel
from pathlib import Path
from math import hypot

W,H=1080,1080
im=Image.new('RGB',(W,H))
pix=im.load()
for y in range(H):
    for x in range(W):
        glow=max(0,1-hypot((x-540)/820,(y-240)/760))
        pix[x,y]=(round(15+24*glow),round(14+16*glow),round(13+8*glow))
d=ImageDraw.Draw(im)
d.rounded_rectangle((30,30,1050,1050),radius=34,outline='#705329',width=2)
d.rounded_rectangle((42,42,1038,1038),radius=28,outline='#3E3020',width=1)
logo=Image.open(ROOT / 'mf-ativo-1.webp').convert('RGBA')
logo=logo.crop(logo.getbbox())
logo.thumbnail((195,160),Image.Resampling.LANCZOS)
im.paste(logo,(114,52),logo)
def font(size,bold=False):
    if Path('/System/Library/Fonts/HelveticaNeue.ttc').exists():
        return ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',size,index=1 if bold else 0)
    return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',size)
def center(y,s,size,color,bold=False):
    d.text((540,y),s,fill=color,font=font(size,bold),anchor='mt')
d.text((343,62),'MF Nota Certa',fill='#F8D991',font=font(79,True),anchor='lt')
d.text((348,151),'Guia de preenchimento da NFS-e',fill='#F9EFE1',font=font(34),anchor='lt')
d.rounded_rectangle((94,226,986,321),radius=25,fill='#292015',outline='#946E38',width=2)
center(237,'Consulta simples',33,'#F9D48B',True)
center(271,'Busque pelo nome do serviço',44,'#FFF3DC',True)
center(335,'Consulta avançada',27,'#F9D48B',True)
center(372,'Simples Nacional e Altamira/PA já preenchidos',35,'#FFF3DC',True)
center(414,'A cidade da execução pode ser alterada.',30,'#F9EFE1')

def draw_qr(url, cx, label):
    card_y, card_side = 460, 425
    left = cx - card_side // 2
    d.rounded_rectangle((left, card_y, left+card_side, card_y+card_side),radius=20,fill='#FFFFFF')
    qr=QRCode(None,QRErrorCorrectLevel.H)
    qr.addData(url)
    qr.make()
    module=card_side//(len(qr.modules)+8)
    side=(len(qr.modules)+8)*module
    assert side<=card_side
    qx=cx-side//2
    qy=card_y+(card_side-side)//2
    for y,row in enumerate(qr.modules):
        for x,on in enumerate(row):
            if on:
                xp=qx+(x+4)*module
                yp=qy+(y+4)*module
                d.rectangle((xp,yp,xp+module-1,yp+module-1),fill='#000000')
    d.text((cx,905),label,fill='#F8D991',font=font(34,True),anchor='mt')

base=BASE
draw_qr(base,308,'Abrir MF Nota Certa')
draw_qr(PDF_URL,772,'Tutorial em PDF')
center(966,'QR da esquerda: abra o MF Nota Certa.',29,'#F9EFE1')
center(1001,'QR da direita: baixe o tutorial atualizado.',29,'#F9EFE1')
im.save(Path('mf-nota-certa-quadrada-dois-qr.png'),optimize=True)
