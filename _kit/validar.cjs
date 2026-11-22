const assert = require('node:assert/strict');
const fs = require('node:fs');
const qr = require('jsqr');
const { PNG } = require('pngjs');
const [helpUrl] = process.argv.slice(2);
for (const [layout, height] of [['quadrada',1080], ['status',1920]]) {
  const image = PNG.sync.read(fs.readFileSync('mf-nota-certa-'+layout+'-ajuda.png'));
  assert.equal(image.width,1080);
  assert.equal(image.height,height);
  const pixels = Uint8ClampedArray.from(image.data);
  const decoded = qr(pixels, image.width, height);
  assert.equal(decoded?.data, helpUrl);
  const corners = Object.values(decoded.location).filter(p => p && 'x' in p);
  const left = Math.max(0, Math.floor(Math.min(...corners.map(p => p.x))) - 5);
  const right = Math.min(image.width, Math.ceil(Math.max(...corners.map(p => p.x))) + 5);
  const top = Math.max(0, Math.floor(Math.min(...corners.map(p => p.y))) - 5);
  const bottom = Math.min(height, Math.ceil(Math.max(...corners.map(p => p.y))) + 5);
  for (let y=top; y<bottom; y++) pixels.fill(255,4*(y*image.width+left),4*(y*image.width+right));
  assert.equal(qr(pixels,image.width,height),null,'QR adicional na arte '+layout);
}
