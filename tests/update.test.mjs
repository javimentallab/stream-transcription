// "Check for updates": version order, the answer from GitHub and every way it can fail.
// The network is always simulated: these tests never reach GitHub.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import vm from 'node:vm';

const CODIGO = readFileSync(new URL('../extension/shared/common.js', import.meta.url), 'utf8');

function cargar({ firefox = false, version = '2.1.1' } = {}) {
  const manifest = { version, ...(firefox ? { browser_specific_settings: { gecko: {} } } : {}) };
  const chrome = { runtime: { getManifest: () => manifest } };
  const ctx = vm.createContext({ URL, Intl, setTimeout, clearTimeout, AbortController, chrome });
  vm.runInContext(CODIGO, ctx);
  return ctx.ST;
}
const ST = cargar();

// A fake fetch that answers like GitHub, and remembers what it was asked.
function github(body, status = 200) {
  const f = async (url, init) => {
    f.llamadas.push({ url, init });
    return {
      ok: status >= 200 && status < 300, status,
      json: async () => (typeof body === 'string' ? JSON.parse(body) : body),
    };
  };
  f.llamadas = [];
  return f;
}
const release = (tag) => ({
  tag_name: tag, draft: false, prerelease: false,
  html_url: `https://github.com/javimentallab/stream-transcription/releases/tag/${tag}`,
});

for (const [a, b, r] of [
  ['2.1.1', '2.1.1', 0],
  ['v2.1.1', '2.1.1', 0],
  ['2.1', '2.1.0', 0],
  ['2.1.2', '2.1.1', 1],
  ['2.1.10', '2.1.9', 1],      // numbers, not text
  ['2.2.0', '2.10.0', -1],
  ['3.0.0', '2.99.99', 1],
  ['2.2.0-beta.1', '2.2.0', -1],
  ['2.2.0-beta.2', '2.2.0-beta.10', -1],
  ['2.2.0-alpha', '2.2.0-beta', -1],
  ['2.2.0-1', '2.2.0-alpha', -1],
  ['2.2.0-beta', '2.2.0-beta.1', -1],
  ['2.2.0+build5', '2.2.0', 0],
]) {
  test(`compareVersions(${a}, ${b}) = ${r}`, () => {
    assert.equal(ST.compareVersions(a, b), r);
    assert.equal(ST.compareVersions(b, a), -r || 0);
  });
}

test('compareVersions: something that is not a version', () => {
  for (const x of ['', null, undefined, 'latest', '2.x', 'v', '1.2.3.4']) {
    assert.equal(ST.compareVersions(x, '1.0.0'), null, String(x));
  }
});

test('a newer release: says so and, in Chromium, points to that release', async () => {
  const fetch = github(release('v2.2.0'));
  const r = await ST.checkForUpdate({ fetch });
  assert.equal(r.ok, true);
  assert.equal(r.newer, true);
  assert.equal(r.latest, '2.2.0');
  assert.equal(r.current, '2.1.1');
  assert.equal(r.page, 'https://github.com/javimentallab/stream-transcription/releases/tag/v2.2.0');
});

test('a newer release in Firefox: points to the add-on on AMO', async () => {
  const r = await cargar({ firefox: true }).checkForUpdate({ fetch: github(release('v2.2.0')) });
  assert.equal(r.newer, true);
  assert.equal(r.page, 'https://addons.mozilla.org/firefox/addon/stream-transcription/');
});

test('the same version, or an older one: nothing new', async () => {
  assert.equal((await ST.checkForUpdate({ fetch: github(release('v2.1.1')) })).newer, false);
  assert.equal((await ST.checkForUpdate({ fetch: github(release('v2.0.0')) })).newer, false);
});

test('asks the right address, without cookies or referrer', async () => {
  const fetch = github(release('v2.1.1'));
  await ST.checkForUpdate({ fetch });
  assert.equal(fetch.llamadas.length, 1);
  const { url, init } = fetch.llamadas[0];
  assert.equal(url, 'https://api.github.com/repos/javimentallab/stream-transcription/releases/latest');
  assert.equal(init.credentials, 'omit');
  assert.equal(init.referrerPolicy, 'no-referrer');
  assert.equal(init.headers.Accept, 'application/vnd.github+json');
  assert.ok(!('User-Agent' in init.headers));
});

test('a release link that is not ours is not followed', async () => {
  const r = await ST.checkForUpdate({ fetch: github({ tag_name: 'v9.0.0', html_url: 'https://evil.example/' }) });
  assert.equal(r.page, 'https://github.com/javimentallab/stream-transcription/releases/latest');
});

for (const [nombre, fetch, error] of [
  ['no network', async () => { throw new TypeError('NetworkError'); }, 'network'],
  ['GitHub limits the checks (403)', github({}, 403), 'rate_limited'],
  ['GitHub limits the checks (429)', github({}, 429), 'rate_limited'],
  ['no release yet', github({}, 404), 'no_release'],
  ['server error', github({}, 502), 'http'],
  ['an answer that is not JSON', github('<html>', 200), 'bad_reply'],
  ['an answer without a tag', github({ name: 'x' }), 'bad_reply'],
  ['a tag that is not a version', github(release('nightly')), 'bad_reply'],
]) {
  test(`checkForUpdate: ${nombre}`, async () => {
    assert.deepEqual({ ...(await ST.checkForUpdate({ fetch })) }, { ok: false, error });
  });
}

test('checkForUpdate: no answer ends in a timeout, and the request is aborted', async () => {
  let senal;
  const fetch = (url, init) => { senal = init.signal; return new Promise(() => {}); };
  const r = await ST.checkForUpdate({ fetch, timeoutMs: 20 });
  assert.equal(r.error, 'timeout');
  assert.equal(senal.aborted, true);
});

test('serverUpdateState', () => {
  assert.equal(ST.serverUpdateState('2.1.1', '2.2.0'), 'newer');
  assert.equal(ST.serverUpdateState('2.2.0', '2.2.0'), 'current');
  assert.equal(ST.serverUpdateState('2.3.0', '2.2.0'), 'current');
  assert.equal(ST.serverUpdateState(undefined, '2.2.0'), 'unknown');
});

test('the server update commands are the README ones', () => {
  for (const f of ['README.md', 'README.es.md']) {
    const readme = readFileSync(new URL('../' + f, import.meta.url), 'utf8').replace(/\r\n/g, '\n');
    assert.ok(readme.includes(ST.SERVER_UPDATE_COMMANDS), f + ' must show the same commands');
  }
});
