// Frame Math engine: frame time budget arithmetic. Milliseconds in one frame at a frame rate, the share of a frame a task uses, and the frame slots a task spans. Exact integers, results rounded half up.
var _FPS = "the frame rate must be a whole number from 1 to 1000";
var _WORK = "the task time must be from 0.1 to 1000 ms with at most one decimal place";
function _fps(t) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(_FPS);
  var v = parseInt(t, 10);
  if (v < 1 || v > 1000) throw new Error(_FPS);
  return v;
}
function _work(t) { // tenths of a ms
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(_WORK);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < 1 || v > 10000) throw new Error(_WORK);
  return v;
}
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _ms(fps) { return _dec(_hu(100000, fps), 2) + " ms"; }

function frameTruth(fps) {
  var f = _fps(fps);
  return "At " + f + (f === 1 ? " frame" : " frames") + " a second, each frame lasts " + _ms(f) + ".";
}
function budgetTruth(fps, workMs) {
  var f = _fps(fps), w = _work(workMs);
  var head = "A task of " + _dec(w, 1) + " ms ";
  var prod = w * f;                       // compare w/10 ms with 1000/f ms: w*f against 10000
  if (prod === 10000) return head + "uses all of a " + _ms(f) + " frame, with nothing left.";
  var pct = _dec(prod, 2);                // percent, 2 places
  if (prod < 10000) return head + "uses " + pct + " percent of a " + _ms(f) + " frame, which leaves " + _dec(_hu((10000 - prod) * 10, f), 2) + " ms.";
  return head + "uses " + pct + " percent of a " + _ms(f) + " frame, which is " + _dec(_hu((prod - 10000) * 10, f), 2) + " ms over.";
}
function slotsTruth(fps, workMs) {
  var f = _fps(fps), w = _work(workMs);
  var n = Math.floor((w * f + 9999) / 10000);
  return "A task of " + _dec(w, 1) + " ms needs " + n + (n === 1 ? " frame slot" : " frame slots") + " at " + f + (f === 1 ? " frame" : " frames") + " a second, which is " + _dec(_hu(n * 100000, f), 2) + " ms in all.";
}
