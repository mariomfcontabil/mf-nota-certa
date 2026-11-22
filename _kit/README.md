# Publicação do kit
Execute na raiz do repositório com Python 3, Node.js e acesso de escrita ao GitHub.
Instale as dependências com `python3 -m pip install -r _kit/requirements.txt` e `npm ci --prefix _kit`.

Use `python3 _kit/publicar.py --publicar` para gerar o PDF, as artes e a mensagem, ler o QR Code da Ajuda em cada arte, verificar o ZIP e publicar a Ajuda em um único envio. Omita `--publicar` para gerar localmente. As capturas são geradas pelo Chrome a partir da versão local do painel em cada execução. Instale o navegador com `node _kit/node_modules/playwright-core/cli.js install chromium-headless-shell` ou indique o executável Chromium na variável MF_CHROME. O texto compartilhado vem de `_kit/mensagem.txt`.

Após o envio, a rotina confere no GitHub Pages o HTML e o conteúdo dos quatro downloads.
