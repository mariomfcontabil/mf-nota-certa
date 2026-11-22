"""Gera e verifica o kit. Use --publicar para enviar a versão aprovada ao Pages."""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from config import BASE, PDF, ZIP, ROOT

KIT = Path(__file__).resolve().parent


def run(*args, cwd=ROOT, env=None):
    subprocess.run(args, cwd=cwd, env=env, check=True)


def version(data):
    return '?v=' + hashlib.sha256(data).hexdigest()[:12]


ARTES = ('arte-quadrada-whatsapp.png', 'arte-vertical-status.png')


def build(stage):
    captures = stage / 'imagens'
    run('node', KIT / 'capturar.cjs', captures, cwd=stage)
    run(sys.executable, KIT / 'tutorial.py', cwd=stage,
        env=dict(os.environ, MF_CAPTURAS=str(captures)))
    pdf = (stage / PDF).read_bytes()
    suffix = version(pdf)
    url = BASE + PDF + suffix
    for layout in ('quadrada', 'vertical'):
        run(sys.executable, KIT / (layout + '.py'), cwd=stage,
            env=dict(os.environ, MF_TUTORIAL_VERSION=suffix))
    run('node', KIT / 'validar.cjs', BASE + '#ajuda', cwd=stage)
    help_url = BASE + '#ajuda'
    message = (KIT / 'mensagem.txt').read_text().format(ajuda=help_url)
    assert re.findall(r'https?://\S+', message) == [help_url]
    files = {
        'arte-quadrada-whatsapp.png': (stage / 'mf-nota-certa-quadrada-ajuda.png').read_bytes(),
        'arte-vertical-status.png': (stage / 'mf-nota-certa-status-ajuda.png').read_bytes(),
        PDF: pdf, 'mensagem-whatsapp.txt': message.encode(),
    }
    with ZipFile(stage / ZIP, 'w') as archive:
        for name, data in files.items():
            archive.writestr(ZipInfo(name), data, compress_type=ZIP_DEFLATED)
    with ZipFile(stage / ZIP) as archive:
        assert {n: archive.read(n) for n in archive.namelist()} == files
    html = (ROOT / 'index.html').read_text()
    for name in ARTES:
        (stage / name).write_bytes(files[name])
    for name in (PDF, ZIP, *ARTES):
        token = version((stage / name).read_bytes())
        html, count = re.subn('href="' + re.escape(name) + r'(?:\?[^"]*)?"',
                              'href="' + name + token + '"', html)
        assert count == 1
    html, count = re.subn(r'(<textarea id="whatsapp-copy-text"[^>]*>).*?(</textarea>)',
                          lambda m: m[1] + escape(message.rstrip()) + m[2], html, flags=re.S)
    assert count == 1 and 'id="ajuda"' in html
    (stage / 'index.html').write_text(html)
    for name in (PDF, ZIP, *ARTES, 'index.html'):
        shutil.copyfile(stage / name, ROOT / name)


def verify_publication():
    names = ['index.html', 'matriz-fiscal-23-atividades.html', PDF, ZIP, *ARTES]
    for name in names:
        expected = (ROOT / name).read_bytes()
        location = BASE + ('' if name == 'index.html' else name) + version(expected)
        for attempt in range(30):
            # Pages pode servir a versão anterior enquanto distribui o novo commit.
            response = subprocess.run(
                ['curl', '-fsSL', '--max-time', '15', location + '&check=' + str(time.time_ns())],
                capture_output=True,
            )
            if response.returncode == 0 and response.stdout == expected:
                break
            if attempt == 29:
                raise RuntimeError('Publicação não confirmada para ' + name)
            time.sleep(4)
    print('Ajuda, tutorial, kit e duas artes verificados no site público.')


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--publicar', action='store_true')
args = parser.parse_args()
with TemporaryDirectory() as tmp:
    build(Path(tmp))
if args.publicar:
    paths = ['_kit', PDF, ZIP, *ARTES, 'index.html', 'matriz-fiscal-23-atividades.html']
    run('git', 'add', '--', *paths)
    if subprocess.run(['git','diff','--cached','--quiet','--',*paths], cwd=ROOT).returncode:
        run('git','commit','-m','Atualizar kit de distribuição do MF Nota Certa','--',*paths)
    run('git','push','origin','HEAD:main')
    verify_publication()
