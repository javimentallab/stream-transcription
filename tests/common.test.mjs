// The helpers every page of the extension uses, above all how it reaches the server.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import vm from 'node:vm';

const CODIGO = readFileSync(new URL('../extension/shared/common.js', import.meta.url), 'utf8');

function cargar(extra = {}) {
  const ctx = vm.createContext({ URL, Intl, setTimeout, clearTimeout, ...extra });
  vm.runInContext(CODIGO, ctx);
  return ctx.ST;
}
const plano = (x) => JSON.parse(JSON.stringify(x));
const ST = cargar();

for (const [entrada, salida] of [
  ['192.168.1.10:9090', 'ws://192.168.1.10:9090/'],
  ['  192.168.1.10:9090  ', 'ws://192.168.1.10:9090/'],
  ['http://host:9090', 'ws://host:9090/'],
  ['https://host/ws', 'wss://host/ws'],
  ['ws://host:1234', 'ws://host:1234/'],
  ['wss://host', 'wss://host/'],
  ['host', 'ws://host:9090/'],
  ['ws://host/path', 'ws://host/path'],
  ['', ''],
  ['   ', ''],
  [null, ''],
  ['ws://', ''],
  ['http://', ''],
]) {
  test(`normalizeServerUrl(${JSON.stringify(entrada)})`, () => {
    assert.equal(ST.normalizeServerUrl(entrada), salida);
  });
}

test('prettyServer', () => {
  assert.equal(ST.prettyServer('ws://host:9090/'), 'host:9090');
  assert.equal(ST.prettyServer('wss://host/ws'), 'host/ws');
  assert.equal(ST.prettyServer('not a url'), 'not a url');
  assert.equal(ST.prettyServer(undefined), '');
});

test('formatBytes', () => {
  assert.equal(ST.formatBytes(0), '0 MB');
  assert.equal(ST.formatBytes(500000), '1 MB');
  assert.equal(ST.formatBytes(120000000), '120 MB');
  assert.equal(ST.formatBytes(1500000000), '1.5 GB');
  assert.equal(ST.formatBytes(2000000000), '2 GB');
});

test('splitModelId', () => {
  assert.deepEqual(plano(ST.splitModelId('Systran/faster-whisper-small')), { name: 'faster-whisper-small', org: 'Systran' });
  assert.deepEqual(plano(ST.splitModelId('url:https://x.example/m')), { name: 'https://x.example/m', org: '' });
  assert.deepEqual(plano(ST.splitModelId('tiny')), { name: 'tiny', org: '' });
  assert.deepEqual(plano(ST.splitModelId('')), { name: '', org: '' });
});

test('languageName: a code it cannot name stays as it is', () => {
  assert.equal(ST.languageName('es', 'en'), 'Spanish');
  assert.equal(ST.languageName('!!', 'en'), '!!');
});

test('sortedLanguages sorts by name', () => {
  const out = plano(ST.sortedLanguages(['fr', 'de', 'es'], 'en'));
  assert.deepEqual(out.map((x) => x.code), ['fr', 'de', 'es']);
});

test('settings: defaults fill in what is missing', async () => {
  const guardado = {};
  const storage = { local: {
    get: async () => ({ settings: guardado.settings }),
    set: async (d) => Object.assign(guardado, d),
  } };
  const S = cargar({ chrome: { storage } });
  assert.equal((await S.getSettings()).captionLines, 2);
  await S.setSettings({ fontSize: 30 });
  const r = await S.getSettings();
  assert.equal(r.fontSize, 30);
  assert.equal(r.captionLines, 2);
});

function servidor() {
  class FakeWS {
    constructor(url) { FakeWS.ultimo = this; this.url = url; this.enviado = []; }
    send(d) { this.enviado.push(d); }
    close() { this.cerrado = true; }
  }
  return FakeWS;
}

test('serverRequest: an answer of ours arrives, and the payload was sent', async () => {
  const WS = servidor();
  const p = cargar({ WebSocket: WS }).serverRequest('ws://h/', { a: 1 });
  WS.ultimo.onopen();
  assert.equal(WS.ultimo.enviado[0], '{"a":1}');
  WS.ultimo.onmessage({ data: '{"st":1,"ok":true}' });
  assert.equal((await p).ok, true);
  assert.ok(WS.ultimo.cerrado);
});

for (const [nombre, accion, error] of [
  ['a plain WhisperLive server answers something else', (w) => { w.onopen(); w.onmessage({ data: '{"message":"hi"}' }); }, 'unsupported'],
  ['an answer that is not JSON', (w) => { w.onopen(); w.onmessage({ data: 'nope' }); }, 'unsupported'],
  ['closes after connecting', (w) => { w.onopen(); w.onclose(); }, 'unsupported'],
  ['does not connect', (w) => { w.onerror(); }, 'unreachable'],
  ['closes without connecting', (w) => { w.onclose(); }, 'unreachable'],
]) {
  test(`serverRequest: ${nombre}`, async () => {
    const WS = servidor();
    const p = cargar({ WebSocket: WS }).serverRequest('ws://h/', {});
    accion(WS.ultimo);
    assert.equal((await p).error, error);
  });
}

test('serverRequest: a bad URL', async () => {
  const WebSocket = function () { throw new Error('bad'); };
  assert.equal((await cargar({ WebSocket }).serverRequest('x', {})).error, 'bad_url');
});

test('serverRequest: no answer ends in a timeout', async () => {
  const WS = servidor();
  assert.equal((await cargar({ WebSocket: WS }).serverRequest('ws://h/', {}, 10)).error, 'timeout');
});
