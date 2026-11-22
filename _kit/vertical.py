from config import BASE, PDF_URL, ASSETS, ROOT
from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode.qrencoder import QRCode, QRErrorCorrectLevel
from pathlib import Path
from math import hypot

W,H=1080,1920
im=Image.new('RGB',(W,H))
pix=im.load()
for y in range(H):
    for x in range(W):
        glow=max(0,1-hypot((x-540)/820,(y-430)/1050))
        pix[x,y]=(round(15+24*glow),round(14+16*glow),round(13+8*glow))
d=ImageDraw.Draw(im)
d.rounded_rectangle((42,172,1038,1785),radius=34,outline='#705329',width=2)
d.rounded_rectangle((54,184,1026,1773),radius=28,outline='#3E3020',width=1)
logo=Image.open(ROOT / 'mf-ativo-1.webp').convert('RGBA')
logo=logo.crop(logo.getbbox())
logo.thumbnail((348,325),Image.Resampling.LANCZOS)
im.paste(logo,((W-logo.width)//2,235),logo)
def font(size,bold=False):
    if Path('/System/Library/Fonts/HelveticaNeue.ttc').exists():
        return ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',size,index=1 if bold else 0)
    return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',size)
def center(y,s,size,color,bold=False):
    d.text((540,y),s,fill=color,font=font(size,bold),anchor='mt')
center(596,'MF Nota Certa',95,'#F8D991',True)
center(707,'Guia de preenchimento da NFS-e',39,'#F9EFE1')
d.rounded_rectangle((94,826,986,1000),radius=25,fill='#292015',outline='#946E38',width=2)
center(852,'Consulta simples',33,'#F9D48B',True)
center(910,'Busque pelo nome do serviço',51,'#FFF3DC',True)
center(1032,'Consulta avançada',31,'#F9D48B',True)
center(1076,'Simples Nacional e Altamira/PA já preenchidos',36,'#FFF3DC',True)
center(1127,'A cidade da execução pode ser alterada.',32,'#F9EFE1')

def draw_qr(url, cx, label):
    card_y, card_side = 1190, 425
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
    d.text((cx,1630),label,fill='#F8D991',font=font(34,True),anchor='mt')

draw_qr(BASE+'#ajuda',540,'Abra a Ajuda do MF Nota Certa')
center(1683,'Escaneie para consultar o serviço, baixar o tutorial',29,'#F9EFE1')
center(1721,'e acessar o kit completo.',29,'#F9EFE1')
im.save(Path('mf-nota-certa-status-ajuda.png'),optimize=True)
