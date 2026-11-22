from pathlib import Path
from os import environ

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / '_kit' / 'imagens'
BASE = 'https://mariomfcontabil.github.io/mf-nota-certa/'
PDF = 'tutorial-mf-nota-certa.pdf'
ZIP = 'mf-nota-certa-kit-whatsapp.zip'
PDF_URL = BASE + PDF + environ.get('MF_TUTORIAL_VERSION', '')
