// Every language has every text, and every text the code asks for exists.
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';

const SRC = new URL('../extension/shared/', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const LOC = join(SRC, '_locales');
const leer = (l) => JSON.parse(readFileSync(join(LOC, l, 'messages.json'), 'utf8'));
const marcas = (m) => (m.message.match(/\$\d|\{\d+\}/g) || []).sort().join();
const idiomas = readdirSync(LOC);
const en = leer('en');

test('the fifteen languages are there', () => {
  const cortos = idiomas.map((l) => l.split('_')[0]);
  for (const c of 'en es pt fr de it nl pl ru uk zh ja ko th hi'.split(' ')) assert.ok(cortos.includes(c), c);
});

for (const l of idiomas) {
  test(`${l}: same keys and same placeholders as English`, () => {
    const d = leer(l);
    assert.deepEqual(Object.keys(d).sort(), Object.keys(en).sort());
    for (const k of Object.keys(en)) assert.equal(marcas(d[k]), marcas(en[k]), k);
    for (const k of Object.keys(en)) assert.ok(d[k].message.trim(), `${k} is empty`);
  });
}

test('every text the code uses exists', () => {
  const usados = new Set();
  for (const f of readdirSync(SRC)) {
    if (!/\.(js|html)$/.test(f)) continue;
    const t = readFileSync(join(SRC, f), 'utf8').replace(/^\s*\/\/.*$/gm, ''); // not the examples in comments
    for (const m of t.matchAll(/\b(?:ST|I)\.t\("([\w]+)"/g)) usados.add(m[1]);
    for (const m of t.matchAll(/data-i18n(?:-[a-z]+)?="([^"]+)"/g)) usados.add(m[1]);
  }
  assert.ok(usados.size > 10, 'the search found almost nothing: it must be broken');
  const faltan = [...usados].filter((k) => !(k in en));
  assert.deepEqual(faltan, []);
});
