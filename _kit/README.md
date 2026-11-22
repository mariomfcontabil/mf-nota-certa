# Publicação do kit
Execute na raiz do repositório com Python 3, Node.js e acesso de escrita ao GitHub.
Instale as dependências com `python3 -m pip install -r _kit/requirements.txt` e `npm install --prefix _kit`.

Use `python3 _kit/publicar.py --publicar` para gerar o PDF, as artes e a mensagem, ler os quatro QR Codes, verificar o ZIP e publicar a Ajuda em um único envio. Omita `--publicar` para gerar localmente. Atualize as capturas em `_kit/imagens` quando as telas mudarem. O texto compartilhado vem de `_kit/mensagem.txt`.
