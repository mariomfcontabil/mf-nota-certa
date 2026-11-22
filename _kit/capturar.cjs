const { chromium } = require('playwright-core');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs/promises');
const {pathToFileURL} = require('node:url');

async function capture() {
  const dest = process.argv[2];
  await fs.mkdir(dest, {recursive:true});
  const browser = await chromium.launch({
    executablePath:process.env.MF_CHROME || undefined,
    args:process.platform === 'darwin' ? ['--single-process','--no-zygote','--disable-gpu','--disable-software-rasterizer'] : [],
  });
  try {
    const page = await browser.newPage({viewport:{width:1280,height:900},locale:'pt-BR',colorScheme:'light'});
    await page.goto(pathToFileURL(path.join(__dirname,'../index.html')).href);
    await page.evaluate(() => Promise.all([...document.images].map(img => img.decode())));
    const el = sel => page.locator(sel);
    async function shot(name, first, last=first) {
      const box = await page.evaluate(([first,last]) => {
        const a=document.querySelector(first).getBoundingClientRect();
        const b=document.querySelector(last).getBoundingClientRect();
        const x=Math.min(a.left,b.left)+scrollX, y=a.top+scrollY;
        return {x,y,width:Math.max(a.right,b.right)+scrollX-x,height:b.bottom+scrollY-y};
      },[first,last]);
      await page.screenshot({path:path.join(dest,name+'.jpg'),fullPage:true,clip:box,quality:94,animations:'disabled',caret:'hide'});
    }
    await shot('tutorial-logo','.shell','#busca-servico-painel');
    await el('#busca-servico').fill('limpeza de escritório');
    const suggestion=page.getByRole('button',{name:/Limpeza geral de prédio/});
    await suggestion.waitFor();
    await shot('tutorial-painel-0','#busca-servico-painel');
    await suggestion.click();
    await el('#consulta-submit').click();
    await el('#continuar-avancada').waitFor();
    await shot('tutorial-painel-1','#resultado-simples');
    await el('#continuar-avancada').click();
    await el('#servico').fill('Limpeza geral de escritório conforme contrato.');
    await shot('tutorial-painel-2','.service-fields');
    assert.equal(await el('#regime').inputValue(),'Simples Nacional');
    for(const id of ['prestador','local']) assert.equal(await el('#'+id).inputValue(),'Altamira/PA');
    await shot('tutorial-padroes','label[for=regime]','#local-help');
    await el('#regime').selectOption({label:'Lucro Presumido'});
    await el('#tomador').selectOption({label:'Pessoa jurídica privada'});
    await el('#contratacao').selectOption({label:'Serviço contratado por resultado'});
    await el('#valor-servico').fill('1500');
    await el('#consulta-submit').click();
    await el('#resultado-titulo').waitFor();
    await shot('tutorial-painel-4','#resultado-titulo','#checklist-wrap tbody tr:first-child');
    await el('#pdf-complementos summary').click();
    await el('#pdf-tomador').fill('Cliente Exemplo');
    await shot('tutorial-painel-5','#pdf-complementos','#gerar-nota-pdf');
    await el('#modo-simples').click();
    await el('#busca-servico').fill('limpeza de escritório ');
    await suggestion.click();
    await el('#consulta-submit').click();
    assert.ok(await el('#resultado-simples').isVisible());
    await el('#busca-servico').fill('pintura');
    assert.equal(await el('#atividade').inputValue(),'');
    assert.ok(await el('#resultado-simples').isHidden());
    for (const width of [320,390,768,1280]) {
      await page.setViewportSize({width,height:800});
      const help = await page.evaluate(() => {
        const section = document.querySelector('#ajuda');
        return {
          width:document.documentElement.scrollWidth,
          downloads:section.querySelectorAll('a[download]').length,
          first:section.querySelector('a[download]').getBoundingClientRect().top - section.getBoundingClientRect().top,
        };
      });
      assert.ok(help.width <= width && help.first < 500);
      assert.equal(help.downloads,4);
    }
  } finally { await browser.close(); }
}
capture().catch(error => {console.error(error);process.exitCode=1;});
