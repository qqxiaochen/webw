'use strict';
const fs = require('fs');
const path = require('path');
const csso = require('csso');
const { minify } = require('html-minifier-terser');
const JavaScriptObfuscator = require('javascript-obfuscator');

const OBF_OPTS = {
  compact: true,
  controlFlowFlattening: true,
  controlFlowFlatteningThreshold: 0.6,
  deadCodeInjection: false,
  numbersToExpressions: true,
  stringArray: true,
  stringArrayEncoding: ['base64'],
  stringArrayThreshold: 0.75,
  splitStrings: true,
  splitStringsChunkLength: 4,
  simplify: true,
  renameGlobals: false,
  identifierNamesGenerator: 'hexadecimal',
  unicodeEscapeSequence: false,
  debugProtection: false,
  selfDefending: false,
  disableConsoleOutput: false
};

const HTML_OPTS = {
  collapseWhitespace: true,
  removeComments: true,
  removeRedundantAttributes: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  useShortDoctype: true,
  minifyCSS: false,
  minifyJS: false,
  caseSensitive: true,
  keepClosingSlash: true,
  ignoreCustomFragments: [/<\%[\s\S]*?\%>/, /<\?[\s\S]*?\?>/]
};

function obfuscateJS(code) {
  try {
    return JavaScriptObfuscator.obfuscate(code, OBF_OPTS).getObfuscatedCode();
  } catch (e) {
    console.error('  ! JS 混淆失败，保留原样:', e.message);
    return code;
  }
}

async function processFile(file) {
  console.log('→ 处理:', file);
  let html = fs.readFileSync(file, 'utf8');

  // 1) 压缩内联 CSS
  html = html.replace(/<style[^>]*>([\s\S]*?)<\/style>/gi, (m, css) => {
    try {
      const min = csso.minify(css).css;
      return '<style>' + min + '</style>';
    } catch (e) {
      console.error('  ! CSS 压缩失败，保留原样:', e.message);
      return m;
    }
  });

  // 2) 强混淆内联 JS
  html = html.replace(/<script[^>]*>([\s\S]*?)<\/script>/gi, (m, js) => {
    if (!js.trim()) return m;
    return '<script>' + obfuscateJS(js) + '</script>';
  });

  // 3) HTML 压平 + 去注释
  let minified;
  try {
    const out = await minify(html, HTML_OPTS);
    minified = typeof out === 'string' ? out : (out && out.html);
  } catch (e) {
    console.error('  ! HTML 压缩失败，保留混淆后版本:', e.message);
    minified = html;
  }
  if (!minified) { console.error('  ! minify 返回空，跳过写入'); return; }
  fs.writeFileSync(file, minified, 'utf8');
  const before = Buffer.byteLength(html, 'utf8');
  const after = Buffer.byteLength(minified, 'utf8');
  console.log('  ✅ 完成  ' + (before / 1024).toFixed(1) + 'KB → ' + (after / 1024).toFixed(1) + 'KB  (' + (100 - Math.round(after / before * 100)) + '% 减小)');
}

(async () => {
  const targets = process.argv.slice(2);
  if (!targets.length) {
    console.error('用法: node obfuscate.js file1.html file2.html');
    process.exit(1);
  }
  for (const t of targets) {
    if (!fs.existsSync(t)) { console.error('文件不存在:', t); continue; }
    await processFile(t);
  }
  console.log('全部处理完毕。');
})();
