const assert = require('node:assert/strict');
const fs = require('node:fs');
const qr = require('jsqr');
const { PNG } = require('pngjs');
const [site, tutorial] = process.argv.slice(2);
for (const [layout, height] of [['quadrada',1080], ['status',1920]]) {
  const image = PNG.sync.read(fs.readFileSync('mf-nota-certa-'+layout+'-dois-qr.png'));
  assert.equal(image.width,1080);
  assert.equal(image.height,height);
  for (const [i, url] of [site,tutorial].entries()) {
    const half = new PNG({ width:540, height });
    PNG.bitblt(image,half,i*540,0,540,height,0,0);
    assert.equal(qr(Uint8ClampedArray.from(half.data),540,height)?.data,url);
  }
}
