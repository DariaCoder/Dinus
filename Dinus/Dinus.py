#!/usr/bin/env python3
"""
Dinus Workspace – Full admin assistant in one Python file.
Run: python3 dinus.py
"""

import http.server
import socketserver
import webbrowser

PORT = 8000

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dinus Workspace</title>
    <style>
        /* ... (same styles as before) ... */
        :root {
            --green: #178653;
            --green-dark: #106c41;
            --green-soft: #eaf7f0;
            --green-hover: #def2e7;
            --white: #ffffff;
            --text: #19231d;
            --muted: #77827c;
            --border: #dfe9e3;
            --danger: #c33c3c;
            --danger-soft: #fff0f0;
            --panel: #fbfdfc;
            --tok-keyword: #c7254e;
            --tok-string: #178653;
            --tok-comment: #9aa69f;
            --tok-number: #b76b01;
            --tok-builtin: #0550ae;
            --tok-identifier: #19231d;
            --tok-tag: #c7254e;
            --tok-attr: #e65100;
        }
        * { box-sizing: border-box; }
        html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; background: #f6f9f7; color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; -webkit-font-smoothing: antialiased; }
        * { scrollbar-width: none; -ms-overflow-style: none; }
        *::-webkit-scrollbar { display: none; }
        button, input, select, textarea { font: inherit; }
        button { border: 0; }
        svg { display: block; }
        .hidden { display: none !important; }

        #app { width: 100vw; height: 100vh; display: flex; flex-direction: column; background: white; }
        .topbar { height: 58px; flex: 0 0 58px; display: flex; align-items: center; padding: 0 17px; background: white; border-bottom: 1px solid var(--border); }
        .location { min-width: 0; font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .search { position: relative; width: min(300px, 34vw); margin-left: auto; }
        .search svg { position: absolute; left: 11px; top: 50%; width: 16px; height: 16px; transform: translateY(-50%); }
        .search input { width: 100%; height: 36px; padding: 0 12px 0 34px; color: var(--text); background: #fafcfb; border: 1px solid var(--border); border-radius: 9px; outline: none; }
        .search input:focus { border-color: var(--green); box-shadow: 0 0 0 3px rgba(23,134,83,0.08); }
        .body { min-height: 0; flex: 1; display: flex; }
        .sidebar { width: 210px; flex: 0 0 210px; display: flex; flex-direction: column; padding: 17px 10px 11px; background: #fafcfb; border-right: 1px solid var(--border); }
        .sidebar-heading { margin: 0 9px 8px; color: var(--muted); font-size: 10px; font-weight: 750; letter-spacing: 0.08em; text-transform: uppercase; }
        .nav { width: 100%; height: 37px; display: flex; align-items: center; gap: 9px; padding: 0 10px; margin-bottom: 2px; color: var(--muted); background: transparent; border-radius: 8px; cursor: pointer; text-align: left; transition: 0.14s; }
        .nav svg { width: 18px; height: 18px; }
        .nav:hover, .nav.active { color: var(--green); background: var(--green-soft); }
        .nav.active { font-weight: 600; }
        .sidebar-bottom { margin-top: auto; padding-top: 11px; border-top: 1px solid var(--border); }
        #trash.drag-hover { color: var(--danger); background: var(--danger-soft); }
        .workspace { min-width: 0; min-height: 0; flex: 1; display: flex; }
        .center { min-width: 0; min-height: 0; flex: 1; display: flex; flex-direction: column; }
        .toolbar { height: 51px; flex: 0 0 51px; display: flex; align-items: center; gap: 7px; padding: 0 15px; border-bottom: 1px solid var(--border); }
        .spacer { flex: 1; }
        .count { color: var(--muted); font-size: 11px; }
        .button { height: 34px; display: inline-flex; align-items: center; justify-content: center; padding: 0 11px; color: var(--text); background: white; border: 1px solid var(--border); border-radius: 8px; cursor: pointer; transition: 0.13s; }
        .button:hover { background: var(--green-soft); border-color: #bfdaca; transform: translateY(-1px); }
        .button.primary { color: white; background: var(--green); border-color: var(--green); }
        .button.primary:hover { background: var(--green-dark); border-color: var(--green-dark); }
        .file-area { position: relative; min-width: 0; min-height: 0; flex: 1; overflow: auto; padding: 18px; }
        .file-area.drag-hover { background: rgba(23,134,83,0.025); box-shadow: inset 0 0 0 2px rgba(23,134,83,0.13); }
        .grid { min-height: 100%; display: grid; grid-template-columns: repeat(auto-fill, minmax(148px, 1fr)); grid-auto-rows: 142px; gap: 10px; align-content: start; }
        .card { min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; padding: 13px; background: white; border: 1px solid transparent; border-radius: 11px; transition: 0.15s; }
        .card:hover { background: var(--green-soft); border-color: #c8e4d3; box-shadow: 0 8px 24px rgba(23,67,44,0.07); transform: translateY(-2px); }
        .card.selected { background: var(--green-hover); border-color: rgba(23,134,83,0.3); }
        .card.dragging { opacity: 0.35; }
        .card-icon { width: 58px; height: 58px; }
        .card-name { width: 100%; font-size: 13px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .card-meta { color: var(--muted); font-size: 10px; }
        .empty { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
        .empty-icon { width: 62px; height: 62px; opacity: 0.75; margin-bottom: 13px; }
        .empty-title { font-size: 15px; font-weight: 650; }
        .empty-subtitle { max-width: 380px; margin-top: 7px; color: var(--muted); font-size: 12px; line-height: 1.55; }
        .editor { min-width: 0; min-height: 0; flex: 1; display: none; flex-direction: column; }
        .editor.visible { display: flex; }
        .editor-header { height: 51px; flex: 0 0 51px; display: flex; align-items: center; padding: 0 12px; border-bottom: 1px solid var(--border); }
        .back { width: 32px; height: 32px; display: grid; place-items: center; color: var(--muted); background: transparent; border-radius: 8px; cursor: pointer; font-size: 21px; }
        .back:hover { color: var(--green); background: var(--green-soft); }
        .editor-name { margin-left: 6px; font-size: 13px; font-weight: 650; }
        .editor-status { margin-left: 8px; color: var(--muted); font-size: 10px; }
        .editor-actions { margin-left: auto; display: flex; gap: 7px; }
        .editor-body { min-height: 0; flex: 1; display: flex; overflow: hidden; }
        .line-column { width: 54px; flex: 0 0 54px; overflow: hidden; background: #fafcfb; border-right: 1px solid var(--border); }
        .line-numbers { margin: 0; padding: 18px 10px 18px 0; color: #9aa69f; font: 13px/1.7 Menlo, Monaco, Consolas, monospace; text-align: right; white-space: pre; user-select: none; }
        .editor-code-wrap { position: relative; min-width: 0; min-height: 0; flex: 1; overflow: hidden; background: white; }
        .editor-highlight { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 18px; overflow: auto; pointer-events: none; background: white; color: var(--text); font: 13px/1.7 Menlo, Monaco, Consolas, monospace; white-space: pre; z-index: 0; }
        .editor-highlight code { display: block; font: inherit; color: var(--text); }
        .editor-text { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 18px; color: transparent; -webkit-text-fill-color: transparent; caret-color: #000; background: transparent; border: 0; outline: 0; resize: none; overflow: auto; font: 13px/1.7 Menlo, Monaco, Consolas, monospace; tab-size: 4; white-space: pre; z-index: 1; }
        .tok-keyword { color: var(--tok-keyword); font-weight: 600; }
        .tok-string { color: var(--tok-string); }
        .tok-comment { color: var(--tok-comment); font-style: italic; }
        .tok-number { color: var(--tok-number); }
        .tok-builtin { color: var(--tok-builtin); }
        .tok-identifier { color: var(--tok-identifier); }
        .tok-tag { color: var(--tok-tag); }
        .tok-attr { color: var(--tok-attr); }
        .runner { height: 190px; flex: 0 0 190px; display: none; flex-direction: column; border-top: 1px solid var(--border); background: #fbfdfc; }
        .runner.visible { display: flex; }
        .runner.fullscreen { position: fixed; inset: 0; height: auto; z-index: 3000; background: white; border-top: none; }
        .runner-header { height: 42px; flex: 0 0 42px; display: flex; align-items: center; padding: 0 12px; border-bottom: 1px solid var(--border); background: white; }
        .runner-title { font-size: 12px; font-weight: 650; }
        .runner-status { margin-left: auto; color: var(--muted); font-size: 10px; }
        .runner-status.success { color: var(--green); }
        .runner-status.failure { color: var(--danger); }
        .runner-exit { margin-left: 8px; width: 30px; height: 30px; display: grid; place-items: center; background: transparent; border-radius: 7px; cursor: pointer; color: var(--muted); font-size: 18px; font-weight: 700; }
        .runner-exit:hover { background: var(--danger-soft); color: var(--danger); }
        .runner-output { min-height: 0; flex: 1; padding: 10px 12px; overflow: auto; font: 11px/1.5 Menlo, Monaco, Consolas, monospace; white-space: pre-wrap; }
        .ai { width: 340px; flex: 0 0 340px; display: none; flex-direction: column; background: var(--panel); border-left: 1px solid var(--border); }
        .ai.visible { display: flex; }
        .ai-header { height: 51px; flex: 0 0 51px; display: flex; align-items: center; padding: 0 14px; border-bottom: 1px solid var(--border); }
        .ai-title { font-size: 13px; font-weight: 650; }
        .ai-status { margin-left: auto; display: flex; align-items: center; gap: 6px; color: var(--muted); font-size: 10px; }
        .ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #b9c4bd; }
        .ai-dot.connected { background: var(--green); }
        .ai-file { padding: 11px 14px; color: var(--muted); font-size: 10px; border-bottom: 1px solid var(--border); }
        .ai-file strong { color: var(--text); }
        .ai-body { min-height: 0; flex: 1; overflow: auto; padding: 12px; }
        .ai-setup { padding: 13px; background: white; border: 1px solid var(--border); border-radius: 10px; }
        .ai-info { margin-top: 6px; color: var(--muted); font-size: 10px; line-height: 1.5; }
        .ai-input, .ai-select { width: 100%; height: 37px; margin-top: 8px; padding: 0 9px; color: var(--text); background: white; border: 1px solid var(--border); border-radius: 8px; outline: none; font-size: 10.5px; }
        .ai-input:focus, .ai-select:focus { border-color: var(--green); box-shadow: 0 0 0 3px rgba(23,134,83,0.07); }
        .ai-row { display: flex; gap: 6px; margin-top: 8px; }
        .ai-help { margin-top: 10px; padding: 9px; color: var(--muted); background: #f8fbf9; border: 1px solid var(--border); border-radius: 8px; font-size: 9.5px; line-height: 1.5; }
        .ai-help code { display: block; margin-top: 4px; padding: 5px 6px; color: var(--text); background: #eef4f0; border-radius: 6px; overflow: auto; }
        .ai-messages { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
        .ai-message { max-width: 95%; padding: 9px 10px; color: var(--text); background: white; border: 1px solid var(--border); border-radius: 9px; font-size: 10.5px; line-height: 1.55; white-space: pre-wrap; }
        .ai-message.user { margin-left: auto; color: white; background: var(--green); border-color: var(--green); }
        .ai-message.system { color: var(--muted); background: transparent; border: 0; padding: 3px 0; }
        .ai-composer { padding: 11px; border-top: 1px solid var(--border); }
        .ai-thinking { display: none; align-items: center; gap: 7px; margin-bottom: 6px; color: var(--muted); font-size: 10px; }
        .ai-thinking.visible { display: flex; }
        .dots { display: flex; gap: 3px; }
        .dots i { width: 4px; height: 4px; border-radius: 50%; background: var(--green); animation: typing-dot 1s infinite; }
        .dots i:nth-child(2) { animation-delay: 0.12s; }
        .dots i:nth-child(3) { animation-delay: 0.24s; }
        @keyframes typing-dot { 0%,60%,100% { opacity: 0.2; transform: translateY(0); } 30% { opacity: 1; transform: translateY(-2px); } }
        .ai-text { width: 100%; min-height: 72px; max-height: 160px; padding: 9px; resize: vertical; color: var(--text); background: white; border: 1px solid var(--border); border-radius: 8px; outline: none; font-size: 10.5px; line-height: 1.45; }
        .modal-overlay { position: fixed; inset: 0; z-index: 1500; display: none; align-items: center; justify-content: center; background: rgba(20,42,30,0.13); backdrop-filter: blur(5px); }
        .modal-overlay.visible { display: flex; }
        .modal { width: min(460px, calc(100vw - 40px)); padding: 20px; background: white; border: 1px solid var(--border); border-radius: 14px; box-shadow: 0 24px 70px rgba(20,68,43,0.15); }
        .modal h2 { margin: 0 0 16px; font-size: 17px; }
        .modal label { display: block; margin-bottom: 6px; color: var(--muted); font-size: 11px; font-weight: 650; }
        .modal input, .modal select { width: 100%; height: 42px; padding: 0 11px; border: 1px solid var(--border); border-radius: 8px; outline: none; }
        .modal-actions { margin-top: 17px; display: flex; justify-content: flex-end; gap: 7px; }
        .context-menu { position: fixed; z-index: 1700; width: 220px; display: none; padding: 6px; background: white; border: 1px solid var(--border); border-radius: 10px; box-shadow: 0 15px 45px rgba(20,68,43,0.10); }
        .context-menu.visible { display: block; }
        .context-item { width: 100%; height: 35px; padding: 0 10px; color: var(--text); background: transparent; border-radius: 7px; cursor: pointer; text-align: left; font-size: 11px; }
        .context-item:hover { color: var(--green); background: var(--green-soft); }
        .context-item.danger:hover { color: var(--danger); background: var(--danger-soft); }
        .watermark { position: fixed; left: 50%; bottom: 10px; z-index: 2; pointer-events: none; transform: translateX(-50%); color: rgba(30,65,48,0.07); font-size: 19px; font-weight: 650; letter-spacing: 0.14em; }
        .toast { position: fixed; left: 50%; bottom: 22px; z-index: 2000; padding: 10px 14px; color: white; background: #18251d; border-radius: 9px; opacity: 0; transform: translate(-50%, 15px); pointer-events: none; transition: 0.15s; font-size: 11px; }
        .toast.visible { opacity: 1; transform: translate(-50%, 0); }
        @media (max-width: 900px) { .sidebar { display: none; } .ai { position: absolute; top: 0; right: 0; bottom: 0; z-index: 100; box-shadow: -12px 0 35px rgba(0,0,0,0.08); } }
        .ollama-status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
        .ollama-status-dot.online { background: var(--green); }
        .ollama-status-dot.offline { background: var(--danger); }
        .ollama-status-dot.unknown { background: var(--muted); }
        .model-tag { display: inline-block; background: var(--green-soft); color: var(--green); padding: 1px 8px; border-radius: 12px; font-size: 9px; font-weight: 600; }
        .diff-label { font-size: 10px; font-weight: 650; margin-top: 10px; }
        .diff-box { border: 1px solid var(--border); border-radius: 8px; overflow: auto; max-height: 260px; margin: 4px 0 8px; font: 11px/1.5 Menlo, Monaco, Consolas, monospace; white-space: pre-wrap; }
        .diff-line { display: block; padding: 4px 8px; }
        .diff-old { background: var(--danger-soft); color: var(--danger); }
        .diff-new { background: var(--green-soft); color: var(--green); }
    </style>
</head>
<body>

<div id="app">

    <header class="topbar">
        <div class="location" id="location">Home</div>
        <div class="search">
            <svg viewBox="0 0 64 64">
                <circle cx="27" cy="27" r="17" fill="none" stroke="#178653" stroke-width="4" />
                <path d="M40 40l15 15" fill="none" stroke="#178653" stroke-width="4" stroke-linecap="round" />
            </svg>
            <input id="search" placeholder="Search files..." autocomplete="off" />
        </div>
    </header>

    <main class="body">

        <aside class="sidebar">
            <div>
                <div class="sidebar-heading">Places</div>
                <button class="nav active" data-path="Home">
                    <svg viewBox="0 0 64 64"><path d="M6 17a7 7 0 0 1 7-7h15l7 8h16a7 7 0 0 1 7 7v23a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7z" fill="#e7f7ef" stroke="#178653" stroke-width="3"/></svg>
                    Home
                </button>
                <button class="nav" data-path="Home/Projects">
                    <svg viewBox="0 0 64 64"><path d="M6 17a7 7 0 0 1 7-7h15l7 8h16a7 7 0 0 1 7 7v23a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7z" fill="#e7f7ef" stroke="#178653" stroke-width="3"/></svg>
                    Projects
                </button>
                <button class="nav" data-path="Home/Documents">
                    <svg viewBox="0 0 64 64"><path d="M6 17a7 7 0 0 1 7-7h15l7 8h16a7 7 0 0 1 7 7v23a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7z" fill="#e7f7ef" stroke="#178653" stroke-width="3"/></svg>
                    Documents
                </button>
                <button class="nav" data-path="Home/Downloads">
                    <svg viewBox="0 0 64 64"><path d="M6 17a7 7 0 0 1 7-7h15l7 8h16a7 7 0 0 1 7 7v23a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7z" fill="#e7f7ef" stroke="#178653" stroke-width="3"/></svg>
                    Downloads
                </button>
            </div>
            <div class="sidebar-bottom">
                <button class="nav" id="trash">
                    <svg viewBox="0 0 64 64"><path d="M13 17h38M24 10h16M18 17l3 37h22l3-37" fill="none" stroke="#178653" stroke-width="3" stroke-linecap="round"/></svg>
                    Trash
                </button>
            </div>
        </aside>

        <section class="workspace">

            <div class="center">

                <div class="toolbar" id="toolbar">
                    <button class="button primary" id="new-button">+ New</button>
                    <button class="button" id="import-button">Import</button>
                    <button class="button" id="save-data-button">Save Data</button>
                    <button class="button" id="load-data-button">Load Data</button>
                    <button class="button" id="assistant-button">Assistant</button>
                    <div class="spacer"></div>
                    <div class="count" id="item-count">0 items</div>
                </div>

                <div class="file-area" id="file-area">
                    <div class="grid" id="file-grid"></div>
                </div>

                <section class="editor" id="editor">
                    <div class="editor-header">
                        <button class="back" id="back-button">‹</button>
                        <div class="editor-name" id="editor-name">File</div>
                        <div class="editor-status" id="editor-status">Saved</div>
                        <div class="editor-actions">
                            <button class="button" id="run-button">Run Test</button>
                            <button class="button" id="download-button" disabled>Download</button>
                            <button class="button primary" id="save-button">Save</button>
                        </div>
                    </div>
                    <div class="editor-body">
                        <div class="line-column">
                            <pre class="line-numbers" id="line-numbers">1</pre>
                        </div>
                        <div class="editor-code-wrap">
                            <pre class="editor-highlight" id="editor-highlight" aria-hidden="true"><code id="editor-highlight-code"></code></pre>
                            <textarea class="editor-text" id="editor-text" wrap="off" spellcheck="false"></textarea>
                        </div>
                    </div>
                </section>

                <div class="runner" id="runner">
                    <div class="runner-header">
                        <div class="runner-title">Run / Test</div>
                        <div class="runner-status" id="runner-status">Ready</div>
                        <button class="runner-exit" id="runner-exit" title="Exit running mode">✕</button>
                    </div>
                    <div class="runner-output" id="runner-output">Run a test to see the result.</div>
                </div>

            </div>

            <aside class="ai" id="ai-panel">

                <div class="ai-header">
                    <div class="ai-title">Assistant</div>
                    <div class="ai-status">
                        <span class="ai-dot" id="ai-dot"></span>
                        <span id="ai-status">Not connected</span>
                    </div>
                </div>

                <div class="ai-file" id="ai-file">No file open</div>

                <div class="ai-body">

                    <div class="ai-setup" id="ai-setup-panel">
                        <div style="font-size:12px;font-weight:650;">Ollama (local)</div>
                        <div class="ai-info">Connect to your local Ollama instance.</div>

                        <div class="ai-info" style="margin-top:8px;">Server URL</div>
                        <input class="ai-input" id="ollama-url" placeholder="http://localhost:11434" value="http://localhost:11434" autocomplete="off" />

                        <input class="ai-input" id="ollama-model" placeholder="Model name, e.g. gemma3" value="gemma3" autocomplete="off" />

                        <div class="ai-row">
                            <button class="button primary" id="connect-ollama" style="flex:1">Connect</button>
                        </div>

                        <div class="ai-info" id="ollama-status">
                            <span class="ollama-status-dot unknown"></span> Not checked yet.
                        </div>

                        <div class="ai-help">
                            <strong>💡 Need help?</strong><br />
                            Make sure Ollama is running with CORS enabled:
                            <code>OLLAMA_ORIGINS="*" ollama serve</code>
                            Then pull a model (e.g. gemma3):
                            <code>ollama pull gemma3</code>
                            <br /><br />
                            <span class="model-tag">gemma3</span>
                            <span class="model-tag">qwen3</span>
                            <span class="model-tag">llama3.2</span>
                            <span class="model-tag">phi4</span>
                        </div>
                    </div>

                    <div class="ai-messages" id="ai-messages"></div>

                </div>

                <div class="ai-composer" id="ai-composer">
                    <div class="ai-thinking" id="ai-thinking">
                        <div class="dots"><i></i><i></i><i></i></div>
                        Thinking
                    </div>
                    <textarea class="ai-text" id="ai-text" placeholder="Ask the assistant to edit this file…"></textarea>
                    <button class="button primary" id="send-ai" style="width:100%;margin-top:7px;">Send</button>
                    <button class="button" id="disconnect-ai" style="width:100%;margin-top:6px;">Disconnect</button>
                </div>

            </aside>

        </section>

    </main>

</div>

<!-- CREATE MODAL -->
<div class="modal-overlay" id="create-overlay">
    <div class="modal">
        <h2 id="create-title">New File</h2>
        <label>Type</label>
        <select id="create-type">
            <option value=".txt">Text</option>
            <option value=".md">Markdown</option>
            <option value=".py">Python</option>
            <option value=".js">JavaScript</option>
            <option value=".ts">TypeScript</option>
            <option value=".html">HTML</option>
            <option value=".css">CSS</option>
            <option value=".json">JSON</option>
            <option value=".yaml">YAML</option>
            <option value=".csv">CSV</option>
            <option value=".sh">Shell</option>
            <option value=".d">D-language</option>
            <option value=".xml">XML</option>
            <option value=".sql">SQL</option>
            <option value=".c">C</option>
            <option value=".cpp">C++</option>
            <option value=".java">Java</option>
            <option value=".swift">Swift</option>
            <option value=".rs">Rust</option>
            <option value=".go">Go</option>
        </select>
        <label style="margin-top:14px;">Name</label>
        <input id="create-name" placeholder="Enter a name…" autocomplete="off" />
        <div class="modal-actions">
            <button class="button" id="cancel-create">Cancel</button>
            <button class="button primary" id="confirm-create">Create</button>
        </div>
    </div>
</div>

<!-- AI PATCH APPROVAL MODAL -->
<div class="modal-overlay" id="patch-overlay">
    <div class="modal">
        <h2>AI wants to edit this file</h2>
        <div id="patch-details"></div>
        <div class="modal-actions">
            <button class="button" id="deny-patch">Deny</button>
            <button class="button primary" id="apply-patch">Apply</button>
        </div>
    </div>
</div>

<div class="context-menu" id="context-menu"></div>

<input type="file" id="file-input" multiple hidden />
<input type="file" id="backup-input" accept=".json,application/json" hidden />

<div class="watermark">dinus</div>
<div class="toast" id="toast"></div>

<script>
"use strict";

    let ollamaEndpoint = localStorage.getItem("dinus.ollama.endpoint") || "http://localhost:11434";
    const STORAGE_WORKSPACE = "dinus.workspace.stable";
    const STORAGE_OLLAMA = "dinus.ollama.model";

let workspace = loadWorkspace();
let currentPath = "Home";
let selectedId = null;
let editingId = null;
let createMode = "file";

    let ollamaModel = localStorage.getItem(STORAGE_OLLAMA) || "";
    let aiBusy = false;
    let testPassed = false;
    let pendingPatches = [];

/* =========================================================
   STORAGE
========================================================= */

function defaultWorkspace() {
    return {
        items: [
            { id: makeId(), name: "Projects", kind: "folder", parent: "Home", builtin: true },
            { id: makeId(), name: "Documents", kind: "folder", parent: "Home", builtin: true },
            { id: makeId(), name: "Downloads", kind: "folder", parent: "Home", builtin: true },
            { id: makeId(), name: "README.md", kind: "file", parent: "Home", builtin: false, size: "1 KB", content: "# Welcome to Dinus\n\nDouble-click a file to edit it.\nSingle-click selects it.\nRight-click gives actions.\n" },
            { id: makeId(), name: "main.js", kind: "file", parent: "Home", builtin: false, size: "1 KB", content: "function main() {\n    console.log(\"Hello from Dinus\");\n}\n\nmain();\n" }
        ],
        trash: []
    };
}

function loadWorkspace() {
    try {
        const raw = localStorage.getItem(STORAGE_WORKSPACE);
        if (!raw) return defaultWorkspace();
        const data = JSON.parse(raw);
        if (!data || !Array.isArray(data.items)) return defaultWorkspace();
        if (!Array.isArray(data.trash)) data.trash = [];
        return data;
    } catch { return defaultWorkspace(); }
}

function saveWorkspace() {
    localStorage.setItem(STORAGE_WORKSPACE, JSON.stringify(workspace));
}

function makeId() { return Date.now().toString(36) + Math.random().toString(36).slice(2); }

function findItem(id) { return workspace.items.find(item => item.id === id); }
    function findItemByName(name, parentPath = currentPath) {
        return workspace.items.find(item => item.parent === parentPath && item.name === name);
    }

function isBuiltin(item) { return item && item.builtin === true; }

function escapeHTML(v) { return String(v).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"); }

function readableSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + " KB";
    return (bytes/(1024*1024)).toFixed(1) + " MB";
}

function isEditable(name) {
    return /\.(txt|md|py|js|ts|jsx|tsx|html|css|json|yaml|yml|csv|sh|bash|zsh|d|xml|sql|c|h|cpp|hpp|java|swift|rs|go|php|rb)$/i.test(String(name));
}

function toast(msg) {
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.classList.add("visible");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => el.classList.remove("visible"), 2000);
}

    /* =========================================================
       TEXT CLEANER – removes markdown, makes text formal & readable
    ========================================================= */

function cleanText(text) {
    if (!text) return text;
    text = text.replace(/\*\*(.+?)\*\*/g, '$1');
    text = text.replace(/\*(.+?)\*/g, '$1');
    text = text.replace(/__(.+?)__/g, '$1');
    text = text.replace(/_(.+?)_/g, '$1');
    text = text.replace(/^#+\s*/gm, '');
    text = text.replace(/^[\-\*]\s+/gm, '• ');
    text = text.replace(/\n{3,}/g, '\n\n');
    return text.trim();
}

/* =========================================================
   ICONS
========================================================= */

function folderIcon() {
    return `<svg viewBox="0 0 64 64"><path d="M6 17a7 7 0 0 1 7-7h15l7 8h16a7 7 0 0 1 7 7v23a7 7 0 0 1-7 7H13a7 7 0 0 1-7-7z" fill="#e7f7ef" stroke="#178653" stroke-width="3"/></svg>`;
}

function codeIcon() {
    return `<svg viewBox="0 0 64 64"><rect x="5" y="5" width="54" height="54" rx="11" fill="#effaf4" stroke="#178653" stroke-width="3"/><path d="M18 22l10 10-10 10M33 42h14" fill="none" stroke="#178653" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

function fileIcon() {
    return `<svg viewBox="0 0 64 64"><path d="M16 5h23l13 13v41H16z" fill="#fff" stroke="#178653" stroke-width="3"/><path d="M39 5v14h13" fill="#e7f7ef" stroke="#178653" stroke-width="3"/><path d="M25 34h18M25 43h18M25 52h12" fill="none" stroke="#178653" stroke-width="3" stroke-linecap="round"/></svg>`;
}

function itemIcon(item) {
    if (item.kind === "folder") return folderIcon();
    if (isEditable(item.name)) return codeIcon();
    return fileIcon();
}

/* =========================================================
   NAVIGATION
========================================================= */

function navigate(path) {
    currentPath = path;
    selectedId = null;
    document.getElementById("location").textContent = path.replaceAll("/", " / ");
    document.querySelectorAll(".nav").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.path === path);
    });
    closeEditor();
    renderFiles();
}

function getVisibleItems() {
    if (currentPath === "Trash") return workspace.trash.slice();
    return workspace.items.filter(item => item.parent === currentPath);
}

/* =========================================================
   RENDER FILES
========================================================= */

function renderFiles() {
    const grid = document.getElementById("file-grid");
    grid.innerHTML = "";
    let items = getVisibleItems();

    items.sort((a,b) => {
        if (a.kind !== b.kind) return a.kind === "folder" ? -1 : 1;
        return a.name.localeCompare(b.name, undefined, { numeric: true });
    });

    document.getElementById("item-count").textContent = items.length + " " + (items.length === 1 ? "item" : "items");

    if (items.length === 0) {
        grid.innerHTML = `
            <div class="empty">
                <div class="empty-icon">${folderIcon()}</div>
                <div class="empty-title">This folder is empty</div>
                <div class="empty-subtitle">Create a project, folder, or file to start building your workspace.</div>
                <button class="button primary" id="empty-new" style="margin-top:16px">+ New</button>
            </div>
        `;
        document.getElementById("empty-new").onclick = () => openCreate("file");
        return;
    }

    items.forEach((item, index) => {
        const card = document.createElement("div");
        card.className = "card";
        if (selectedId === item.id) card.classList.add("selected");
        card.style.animationDelay = Math.min(index*12, 100) + "ms";
        card.innerHTML = `
            <div class="card-icon">${itemIcon(item)}</div>
            <div class="card-name">${escapeHTML(item.name)}</div>
            <div class="card-meta">${item.kind === "folder" ? "Folder" : (item.size || "File")}</div>
        `;

        card.onclick = (e) => {
            e.stopPropagation();
            document.querySelectorAll(".card.selected").forEach(c => c.classList.remove("selected"));
            card.classList.add("selected");
            selectedId = item.id;
        };

        card.ondblclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            openItem(item);
        };

        card.oncontextmenu = (e) => {
            e.preventDefault();
            e.stopPropagation();
            selectedId = item.id;
            showContextMenu(e.clientX, e.clientY, true);
        };

        if (!isBuiltin(item) && currentPath !== "Trash") {
            card.draggable = true;
            card.ondragstart = (e) => {
                e.dataTransfer.setData("text/plain", item.id);
                card.classList.add("dragging");
            };
            card.ondragend = () => card.classList.remove("dragging");
        }

        if (item.kind === "folder") {
            card.ondragover = (e) => { e.preventDefault(); card.style.background = "var(--green-hover)"; };
            card.ondragleave = () => { card.style.background = ""; };
            card.ondrop = (e) => {
                e.preventDefault();
                card.style.background = "";
                moveItem(e.dataTransfer.getData("text/plain"), item);
            };
        }

        grid.appendChild(card);
    });
}

/* =========================================================
   OPEN ITEM
========================================================= */

function openItem(item) {
    if (item.kind === "folder") {
        navigate(item.parent + "/" + item.name);
        return;
    }
    if (isEditable(item.name)) {
        openEditor(item);
        return;
    }
    showAIPanel(item);
}

/* =========================================================
   EDITOR
========================================================= */

function openEditor(item) {
    editingId = item.id;
    selectedId = item.id;
    document.getElementById("file-area").classList.add("hidden");
    document.getElementById("toolbar").classList.add("hidden");
    document.getElementById("editor").classList.add("visible");
    document.getElementById("editor-name").textContent = item.name;
    document.getElementById("editor-status").textContent = "Saved";
    document.getElementById("editor-text").value = item.content || "";
    testPassed = false;
    document.getElementById("download-button").disabled = true;
    updateLineNumbers();
    updateHighlight();
    showAIPanel(item);
    document.getElementById("editor-text").focus();
}

function closeEditor() {
    document.getElementById("editor").classList.remove("visible");
    document.getElementById("file-area").classList.remove("hidden");
    document.getElementById("toolbar").classList.remove("hidden");
    document.getElementById("runner").classList.remove("visible", "fullscreen");
    document.getElementById("ai-panel").classList.remove("visible");
    editingId = null;
}

document.getElementById("back-button").onclick = closeEditor;
document.getElementById("save-button").onclick = saveEditorFile;

let autosaveTimer = null;
document.getElementById("editor-text").addEventListener("input", () => {
    document.getElementById("editor-status").textContent = "Unsaved";
    testPassed = false;
    document.getElementById("download-button").disabled = true;
    updateLineNumbers();
    updateHighlight();
    clearTimeout(autosaveTimer);
    autosaveTimer = setTimeout(saveEditorSilently, 350);
});

document.getElementById("editor-text").addEventListener("scroll", syncLineScroll);
document.getElementById("editor-text").addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
        e.preventDefault();
        const el = e.currentTarget;
        const start = el.selectionStart;
        const end = el.selectionEnd;
        el.value = el.value.slice(0, start) + "    " + el.value.slice(end);
        el.selectionStart = el.selectionEnd = start + 4;
        updateLineNumbers();
        updateHighlight();
    }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "s") {
        e.preventDefault();
        saveEditorFile();
    }
});

function updateLineNumbers() {
    const text = document.getElementById("editor-text").value;
    const count = text.split("\n").length;
    document.getElementById("line-numbers").textContent = Array.from({ length: count }, (_,i) => i+1).join("\n");
    syncLineScroll();
}

function syncLineScroll() {
    const ta = document.getElementById("editor-text");
    const hl = document.getElementById("editor-highlight");
    document.getElementById("line-numbers").style.transform = "translateY(-" + ta.scrollTop + "px)";
    hl.scrollTop = ta.scrollTop;
    hl.scrollLeft = ta.scrollLeft;
}

function saveEditorSilently() {
    const item = findItem(editingId);
    if (!item) return;
    item.content = document.getElementById("editor-text").value;
    item.size = readableSize(new Blob([item.content]).size);
    saveWorkspace();
}

function saveEditorFile() {
    saveEditorSilently();
    document.getElementById("editor-status").textContent = "Saved";
    renderFiles();
    toast("Saved");
}

/* =========================================================
   SYNTAX HIGHLIGHTING
========================================================= */

function getLanguageFromName(name) {
    const ext = (name.match(/\.[^.]+$/) || [""])[0].toLowerCase();
    const map = {
        ".py": "python",
        ".js": "javascript",
        ".mjs": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".html": "html",
        ".htm": "html",
        ".xml": "xml",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".markdown": "markdown",
        ".sh": "shell",
        ".bash": "shell",
        ".zsh": "shell",
        ".sql": "sql",
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".swift": "swift"
    };
    return map[ext] || "plain";
}

function getLanguagePatterns(lang) {
    if (lang === "python") {
        return [
            { type: "comment", re: /#[^\n]*/y },
            { type: "string", re: /(?:\x22\x22\x22(?:[^"\\]|\\.|"(?!""))*\x22\x22\x22|\x27\x27\x27(?:[^'\\]|\\.|'(?!''))*\x27\x27\x27|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')/y },
            { type: "number", re: /\b(?:0x[0-9a-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[jJ]?)\b/y },
            { type: "identifier", re: /[A-Za-z_]\w*/y }
        ];
    }
    if (lang === "javascript" || lang === "typescript" || lang === "jsx" || lang === "tsx") {
        return [
            { type: "comment", re: /\/\/[^\n]*|\/\*[\s\S]*?\*\//y },
            { type: "string", re: /`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/y },
            { type: "number", re: /\b(?:0x[0-9a-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?n?)\b/y },
            { type: "identifier", re: /[A-Za-z_$][\w$]*/y }
        ];
    }
    if (lang === "html" || lang === "xml") {
        return [
            { type: "comment", re: /<!--[\s\S]*?-->/y },
            { type: "string", re: /"[^"]*"|'[^']*'/y },
            { type: "tag", re: /<\/?[a-zA-Z][^>]*>/y },
            { type: "identifier", re: /[A-Za-z_]\w*/y }
        ];
    }
    if (lang === "css") {
        return [
            { type: "comment", re: /\/\*[\s\S]*?\*\//y },
            { type: "string", re: /"[^"]*"|'[^']*'/y },
            { type: "number", re: /\b\d+(?:\.\d+)?(?:[a-z%]*)\b/y },
            { type: "identifier", re: /[A-Za-z_-][\w-]*/y }
        ];
    }
    if (lang === "json") {
        return [
            { type: "string", re: /"(?:\\.|[^"\\])*"/y },
            { type: "number", re: /\b-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b/y },
            { type: "identifier", re: /[A-Za-z_]\w*/y }
        ];
    }
        // fallback / plain / markdown / shell / sql / etc.
    return [
        { type: "comment", re: /\/\/[^\n]*|\/\*[\s\S]*?\*\//y },
        { type: "string", re: /"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|`(?:\\.|[^`\\])*`/y },
        { type: "number", re: /\b\d+(?:\.\d+)?\b/y },
        { type: "identifier", re: /[A-Za-z_$][\w$]*/y }
    ];
}

const JS_KEYWORDS = new Set("break case catch class const continue debugger default delete do else export extends finally for function if import in instanceof let new return super switch this throw try typeof var void while with yield async await static get set of".split(" "));
const TS_KEYWORDS = new Set([...JS_KEYWORDS, "interface", "type", "enum", "namespace", "declare", "abstract", "public", "private", "protected", "implements", "readonly", "keyof", "infer", "never", "unknown", "any"]);
const PY_KEYWORDS = new Set("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" "));
const C_KEYWORDS = new Set("auto break case char const continue default do double else enum extern float for goto if inline int long register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while".split(" "));
const CPP_KEYWORDS = new Set([...C_KEYWORDS, "class", "namespace", "template", "typename", "new", "delete", "this", "public", "private", "protected", "virtual", "override", "final", "constexpr", "nullptr", "try", "catch", "throw", "using", "operator"]);
const JAVA_KEYWORDS = new Set("abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while".split(" "));
const GO_KEYWORDS = new Set("break case chan const continue default defer else fallthrough for func go goto if import interface map package range return select struct switch type var".split(" "));
const RUST_KEYWORDS = new Set("as break const continue crate dyn else enum extern false fn for if impl in let loop match mod move mut pub ref return self Self static struct super trait true type unsafe use where while async await".split(" "));
const SWIFT_KEYWORDS = new Set("associatedtype class deinit enum extension fileprivate func import init inout internal let open operator private protocol public rethrows static struct subscript typealias var break case continue default defer do else fallthrough for guard if in repeat return switch where while as Any false is nil self Self super throws true try".split(" "));

const KEYWORDS = {
    javascript: JS_KEYWORDS,
    typescript: TS_KEYWORDS,
    python: PY_KEYWORDS,
    c: C_KEYWORDS,
    cpp: CPP_KEYWORDS,
    java: JAVA_KEYWORDS,
    go: GO_KEYWORDS,
    rust: RUST_KEYWORDS,
    swift: SWIFT_KEYWORDS
};

const BUILTINS = {
    javascript: new Set("console document window Math JSON Promise Array Object Function String Number Boolean Symbol Set Map WeakMap WeakSet Date RegExp Error TypeError SyntaxError parseInt parseFloat isNaN isFinite".split(" ")),
    python: new Set("print len range str int float list dict set tuple type isinstance super open input dir help min max sum sorted reversed enumerate zip map filter".split(" "))
};

function matchAt(re, str, pos) {
    re.lastIndex = pos;
    return re.exec(str);
}

function tokenize(code, lang) {
    const patterns = getLanguagePatterns(lang);
    const tokens = [];
    let i = 0;
    while (i < code.length) {
        let best = null;
        for (const pat of patterns) {
            const m = matchAt(pat.re, code, i);
            if (m && m.index === i) {
                best = { pat, m };
                break;
            }
        }
        if (best) {
            tokens.push({ type: best.pat.type, text: best.m[0] });
            i += best.m[0].length;
        } else {
            tokens.push({ type: null, text: code[i] });
            i++;
        }
    }
    return tokens;
}

function classifyIdentifier(name, lang) {
    if (KEYWORDS[lang] && KEYWORDS[lang].has(name)) return "keyword";
    if (BUILTINS[lang] && BUILTINS[lang].has(name)) return "builtin";
    return "identifier";
}

function highlightCode(code, lang) {
    const tokens = tokenize(code, lang);
    return tokens.map(t => {
        if (!t.type) return escapeHTML(t.text);
        if (t.type === "identifier") {
            const cls = classifyIdentifier(t.text, lang);
            return `<span class="tok-${cls}">${escapeHTML(t.text)}</span>`;
        }
        return `<span class="tok-${t.type}">${escapeHTML(t.text)}</span>`;
    }).join("");
}

function updateHighlight() {
    const code = document.getElementById("editor-text").value;
    const name = document.getElementById("editor-name").textContent;
    const lang = getLanguageFromName(name);
    document.getElementById("editor-highlight-code").innerHTML = highlightCode(code, lang);
    syncLineScroll();
}

/* =========================================================
   CREATE
========================================================= */

function openCreate(mode) {
    createMode = mode;
    document.getElementById("create-title").textContent = mode === "file" ? "New File" : mode === "folder" ? "New Folder" : "New Project";
    document.getElementById("create-type").style.display = mode === "file" ? "block" : "none";
    document.getElementById("create-name").value = "";
    document.getElementById("create-overlay").classList.add("visible");
    setTimeout(() => document.getElementById("create-name").focus(), 50);
}

function closeCreate() {
    document.getElementById("create-overlay").classList.remove("visible");
}

document.getElementById("cancel-create").onclick = closeCreate;
document.getElementById("create-overlay").onclick = (e) => { if (e.target.id === "create-overlay") closeCreate(); };
document.getElementById("create-name").addEventListener("keydown", (e) => {
    if (e.key === "Enter") document.getElementById("confirm-create").click();
    if (e.key === "Escape") closeCreate();
});

document.getElementById("confirm-create").onclick = () => {
    let name = document.getElementById("create-name").value.trim();
    if (!name) { toast("Enter a name."); return; }
    if (workspace.items.some(item => item.parent === currentPath && item.name.toLowerCase() === name.toLowerCase())) {
        toast("That name already exists.");
        return;
    }

    if (createMode === "file") {
        const ext = document.getElementById("create-type").value;
        if (!name.includes(".")) name += ext;
        const item = {
            id: makeId(),
            name,
            kind: "file",
            parent: currentPath,
            builtin: false,
            content: starterContent(ext),
            size: "0 B"
        };
        workspace.items.push(item);
        saveWorkspace();
        closeCreate();
        renderFiles();
        setTimeout(() => openEditor(item), 80);
        return;
    }

    workspace.items.push({
        id: makeId(),
        name,
        kind: "folder",
        parent: currentPath,
        builtin: false,
        project: createMode === "project"
    });
    saveWorkspace();
    closeCreate();
    renderFiles();
};

function starterContent(ext) {
    const map = {
        ".js": "function main() {\n    console.log(\"Hello from Dinus\");\n}\n\nmain();\n",
        ".ts": "function main(): void {\n    console.log(\"Hello from Dinus\");\n}\n\nmain();\n",
        ".py": "def main():\n    print(\"Hello from Dinus\")\n\nif __name__ == \"__main__\":\n    main()\n",
        ".html": "<!doctype html>\n<html>\n<head>\n    <meta charset=\"utf-8\">\n    <title>Dinus</title>\n</head>\n<body>\n    <h1>Hello from Dinus</h1>\n</body>\n</html>\n",
        ".css": "body {\n    margin: 0;\n}\n",
        ".json": "{\n    \"name\": \"Dinus\"\n}\n",
        ".md": "# New Document\n\nStart writing here.\n",
        ".sh": "#!/bin/zsh\n\necho \"Hello from Dinus\"\n",
        ".d": "let name = \"Dinus\"\n\nsay \"Hello, {name}\"\n"
    };
    return map[ext] || "";
}

/* =========================================================
   DELETE / MOVE / TRASH
========================================================= */

function deleteItemById(id) {
    const idx = workspace.items.findIndex(item => item.id === id);
    if (idx === -1) return null;
    const item = workspace.items[idx];
    if (isBuiltin(item)) return null;
    workspace.items.splice(idx, 1);
    item.previousParent = item.parent;
    workspace.trash.push(item);
    saveWorkspace();
    return item;
}

function deleteSelected() {
    if (!selectedId) return;
    const item = deleteItemById(selectedId);
    if (!item) { toast("Cannot delete built-in item."); return; }
    selectedId = null;
    renderFiles();
    toast("Moved to trash: " + item.name);
}

function moveItem(id, folder) {
    const item = findItem(id);
    if (!item || !folder || isBuiltin(item) || item.id === folder.id) return;
    item.parent = folder.parent + "/" + folder.name;
    saveWorkspace();
    renderFiles();
}

document.getElementById("trash").ondragover = (e) => { e.preventDefault(); document.getElementById("trash").classList.add("drag-hover"); };
document.getElementById("trash").ondragleave = () => { document.getElementById("trash").classList.remove("drag-hover"); };
document.getElementById("trash").ondrop = (e) => {
    e.preventDefault();
    document.getElementById("trash").classList.remove("drag-hover");
    const id = e.dataTransfer.getData("text/plain");
    const item = deleteItemById(id);
    if (item) { toast("Moved to trash: " + item.name); renderFiles(); }
};
document.getElementById("trash").onclick = () => navigate("Trash");

function restoreSelected() {
    if (!selectedId) { toast("Select a file first."); return; }
    const idx = workspace.trash.findIndex(item => item.id === selectedId);
    if (idx === -1) return;
    const item = workspace.trash.splice(idx, 1)[0];
    item.parent = item.previousParent || item.parent || "Home";
    delete item.previousParent;
    workspace.items.push(item);
    selectedId = null;
    saveWorkspace();
    renderFiles();
    toast("Restored " + item.name);
}

function permanentlyDeleteSelected() {
    if (!selectedId) { toast("Select a file first."); return; }
    const idx = workspace.trash.findIndex(item => item.id === selectedId);
    if (idx === -1) return;
    workspace.trash.splice(idx, 1);
    selectedId = null;
    saveWorkspace();
    renderFiles();
    toast("Deleted permanently");
}

function emptyTrash() {
    if (workspace.trash.length === 0) return;
    if (!confirm("Permanently delete all items in Trash?")) return;
    workspace.trash = [];
    selectedId = null;
    saveWorkspace();
    renderFiles();
    toast("Trash emptied");
}

/* =========================================================
   CONTEXT MENU
========================================================= */

function hideContextMenu() {
    document.getElementById("context-menu").classList.remove("visible");
}

function addContextItem(text, cb, danger = false) {
    const btn = document.createElement("button");
    btn.className = "context-item" + (danger ? " danger" : "");
    btn.textContent = text;
    btn.onclick = () => { hideContextMenu(); cb(); };
    document.getElementById("context-menu").appendChild(btn);
}

function showContextMenu(x, y, selected, forceCreate = false) {
    const menu = document.getElementById("context-menu");
    menu.innerHTML = "";

    if (currentPath === "Trash" && !forceCreate) {
        if (selectedId) {
            addContextItem("Restore", restoreSelected);
            addContextItem("Delete Permanently", permanentlyDeleteSelected, true);
        } else {
            addContextItem("Empty Trash", emptyTrash, true);
        }
    } else if (selected && !forceCreate) {
        const item = findItem(selectedId);
        if (item) {
            addContextItem("Open", () => openItem(item));
            if (!isBuiltin(item)) addContextItem("Delete", deleteSelected, true);
        }
    } else {
        addContextItem("New File", () => openCreate("file"));
        addContextItem("New Folder", () => openCreate("folder"));
        addContextItem("New Project", () => openCreate("project"));
    }

    menu.style.left = Math.min(x, window.innerWidth - 230) + "px";
    menu.style.top = Math.min(y, window.innerHeight - 220) + "px";
    menu.classList.add("visible");
}

document.getElementById("file-area").oncontextmenu = (e) => {
    if (e.target.closest(".card")) return;
    e.preventDefault();
    selectedId = null;
    showContextMenu(e.clientX, e.clientY, false);
};

document.addEventListener("click", (e) => {
    if (!e.target.closest("#context-menu")) hideContextMenu();
});

/* =========================================================
   IMPORT
========================================================= */

document.getElementById("import-button").onclick = () => document.getElementById("file-input").click();
document.getElementById("file-input").onchange = async (e) => {
    const files = Array.from(e.target.files);
    for (const file of files) {
        let content = "";
        if (file.type.startsWith("text/") || isEditable(file.name)) {
            try { content = await file.text(); } catch { content = ""; }
        }
        workspace.items.push({
            id: makeId(),
            name: file.name,
            kind: "file",
            parent: currentPath,
            builtin: false,
            size: readableSize(file.size),
            content
        });
    }
    saveWorkspace();
    renderFiles();
    e.target.value = "";
};

/* =========================================================
   DATA BACKUP
========================================================= */

document.getElementById("save-data-button").onclick = () => {
    const blob = new Blob([JSON.stringify({ version: 1, workspace }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "dinus-workspace-backup.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast("Backup downloaded");
};

document.getElementById("load-data-button").onclick = () => document.getElementById("backup-input").click();
document.getElementById("backup-input").onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
        const data = JSON.parse(await file.text());
        if (!data.workspace || !Array.isArray(data.workspace.items)) throw new Error("Invalid backup");
        workspace = data.workspace;
        saveWorkspace();
        navigate("Home");
        toast("Workspace restored");
    } catch {
        toast("Invalid Dinus backup");
    }
    e.target.value = "";
};

/* =========================================================
   SEARCH
========================================================= */

document.getElementById("search").oninput = (e) => {
    const query = e.target.value.trim().toLowerCase();
    const grid = document.getElementById("file-grid");
    if (!query) { renderFiles(); return; }
    const matches = workspace.items.filter(item => item.name.toLowerCase().includes(query));
    grid.innerHTML = "";
    document.getElementById("item-count").textContent = matches.length + " " + (matches.length === 1 ? "item" : "items");
    matches.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <div class="card-icon">${itemIcon(item)}</div>
            <div class="card-name">${escapeHTML(item.name)}</div>
            <div class="card-meta">${item.kind === "folder" ? "Folder" : (item.size || "File")}</div>
        `;
        card.onclick = () => { selectedId = item.id; document.querySelectorAll(".card.selected").forEach(c => c.classList.remove("selected")); card.classList.add("selected"); };
        card.ondblclick = () => openItem(item);
        grid.appendChild(card);
    });
};

/* =========================================================
   TOOLBAR
========================================================= */

document.getElementById("new-button").onclick = (e) => {
    showContextMenu(e.clientX, e.currentTarget.getBoundingClientRect().bottom + 4, false, true);
};

document.getElementById("assistant-button").onclick = () => {
    const panel = document.getElementById("ai-panel");
    if (panel.classList.contains("visible")) { panel.classList.remove("visible"); return; }
    const item = findItem(editingId || selectedId);
    if (item) showAIPanel(item);
    else { panel.classList.add("visible"); updateAIUI(); }
};

/* =========================================================
       AI - only Ollama
========================================================= */

function showAIPanel(item) {
    document.getElementById("ai-panel").classList.add("visible");
    document.getElementById("ai-file").innerHTML = "File: <strong>" + escapeHTML(item.name) + "</strong>";
    updateAIUI();
}

function updateAIUI() {
    const connected = Boolean(ollamaModel);
    document.getElementById("ai-setup-panel").classList.toggle("hidden", connected);
    document.getElementById("ai-dot").classList.toggle("connected", connected);
    document.getElementById("ai-status").textContent = connected ? "Ollama (" + ollamaModel + ")" : "Not connected";
    document.getElementById("ai-composer").classList.toggle("hidden", !connected);
    document.getElementById("ollama-model").value = ollamaModel || "gemma3";
        document.getElementById("ollama-url").value = ollamaEndpoint;
    if (!connected) {
        refreshOllama();
    }
}

    /* =========================================================
       OLLAMA
    ========================================================= */

async function refreshOllama() {
    const status = document.getElementById("ollama-status");
        status.innerHTML = `<span class="ollama-status-dot unknown"></span> Checking Ollama…`;

    try {
            const resp = await fetch(ollamaEndpoint + "/api/tags", {
                method: "GET",
                headers: { "Accept": "application/json" },
                mode: "cors"
            });

        if (!resp.ok) throw new Error("HTTP " + resp.status);

        const data = await resp.json();
        const models = Array.isArray(data.models) ? data.models : [];

        if (models.length === 0) {
            status.innerHTML = `<span class="ollama-status-dot online"></span> Ollama is running but no models are installed.`;
            return;
        }

        const modelNames = models.map(m => m.name).join(", ");
        status.innerHTML = `<span class="ollama-status-dot online"></span> ${models.length} model${models.length === 1 ? "" : "s"} available. <span style="opacity:0.6;font-size:9px;">${modelNames}</span>`;

        if (ollamaModel && !models.some(m => m.name === ollamaModel)) {
            const gemma = models.find(m => m.name.includes("gemma"));
            ollamaModel = gemma ? gemma.name : models[0].name;
            localStorage.setItem(STORAGE_OLLAMA, ollamaModel);
            document.getElementById("ollama-model").value = ollamaModel;
        }

    } catch (err) {
        const msg = err.message || String(err);
            if (msg.includes("Failed to fetch") || msg.includes("NetworkError") || msg.includes("CORS")) {
                status.innerHTML = `<span class="ollama-status-dot offline"></span> ⚠️ Cannot reach Ollama. Make sure it's running with CORS enabled: <code style="background:#eef4f0;padding:2px 6px;border-radius:4px;">OLLAMA_ORIGINS="*" ollama serve</code>`;
            } else {
        status.innerHTML = `<span class="ollama-status-dot offline"></span> Error: ${escapeHTML(msg)}`;
            }
    }
}

document.getElementById("connect-ollama").onclick = async () => {
    let model = document.getElementById("ollama-model").value.trim();
        const urlInput = document.getElementById("ollama-url").value.trim();
    if (!model) { toast("Enter a model name."); return; }

        ollamaEndpoint = urlInput.replace(/\/+$/, "") || "http://localhost:11434";
        localStorage.setItem("dinus.ollama.endpoint", ollamaEndpoint);

    const status = document.getElementById("ollama-status");

    try {
            const tagsResp = await fetch(ollamaEndpoint + "/api/tags", {
                method: "GET",
                headers: { "Accept": "application/json" },
                mode: "cors"
            });
            if (!tagsResp.ok) throw new Error("Ollama not reachable (HTTP " + tagsResp.status + ")");

        const tagsData = await tagsResp.json();
        const installed = Array.isArray(tagsData.models) ? tagsData.models : [];
        const found = installed.find(m => m.name === model);

        if (!found) {
            const partial = installed.find(m => m.name.includes(model) || model.includes(m.name));
            if (partial) {
                model = partial.name;
                document.getElementById("ollama-model").value = model;
            } else {
                const available = installed.map(m => m.name).join(", ");
                toast("Model not found. Available: " + (available || "none"));
                status.innerHTML = `<span class="ollama-status-dot offline"></span> Model "${escapeHTML(model)}" not installed. Available: ${escapeHTML(available || "none")}`;
                return;
            }
        }

            const testResp = await fetch(ollamaEndpoint + "/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: model,
                messages: [{ role: "user", content: "Hello" }],
                stream: false,
                options: { num_predict: 5 }
            })
        });

            if (!testResp.ok) {
                const errData = await testResp.json().catch(() => ({}));
                throw new Error(errData.error || "Model failed to respond (HTTP " + testResp.status + ")");
        }

        ollamaModel = model;
        localStorage.setItem(STORAGE_OLLAMA, ollamaModel);
        updateAIUI();
        addAIMessage("system", "✅ Ollama connected: " + model);
        toast("Connected to " + model);
        status.innerHTML = `<span class="ollama-status-dot online"></span> Connected to ${escapeHTML(model)}. Ready.`;

    } catch (err) {
        const msg = err.message || String(err);
            if (msg.includes("Failed to fetch") || msg.includes("NetworkError") || msg.includes("CORS")) {
                status.innerHTML = `<span class="ollama-status-dot offline"></span> ⚠️ CORS / network error. Start Ollama with: <code style="background:#eef4f0;padding:2px 6px;border-radius:4px;">OLLAMA_ORIGINS="*" ollama serve</code>`;
            } else {
        status.innerHTML = `<span class="ollama-status-dot offline"></span> Error: ${escapeHTML(msg)}`;
            }
        toast("Ollama error: " + msg);
    }
};

document.getElementById("disconnect-ai").onclick = () => {
    ollamaModel = "";
    localStorage.removeItem(STORAGE_OLLAMA);
    document.getElementById("ai-messages").innerHTML = "";
    updateAIUI();
    toast("Disconnected");
};

/* =========================================================
       AI CHAT – patch approval flow
========================================================= */

function addAIMessage(type, text) {
    const msg = document.createElement("div");
    msg.className = "ai-message" + (type === "user" ? " user" : "") + (type === "system" ? " system" : "");
    msg.textContent = text;
    document.getElementById("ai-messages").appendChild(msg);
    const body = document.querySelector(".ai-body");
    body.scrollTop = body.scrollHeight;
}

function buildAIPrompt(item, request) {
    const fileSnippet = item && item.content ? item.content.slice(0, 8000) : "";
    return `You are the AI assistant inside Dinus Workspace.

You can ONLY edit the currently open file. Do NOT create, delete, rename, or move any files or folders.

CURRENT FILE:
${item ? item.name : "None (no file is open)"}

${item ? `CURRENT FILE CONTENT (truncated if needed):\n${fileSnippet}\n` : ""}

HOW TO EDIT:
- Use one or more <DINUS_PATCH>{"old":"exact old text","new":"new text"}</DINUS_PATCH> tags.
- The "old" text must match EXACTLY, including spaces and line breaks. Use \n escapes for newlines in the JSON strings.
- Only target specific parts of the file. Never output the whole file.
- If no file is open, do not output <DINUS_PATCH> tags.

USER REQUEST:
${request}`;
}

    function parseAIPatches(text) {
    const patches = [];
        const cleaned = text.replace(/<DINUS_PATCH>([\s\S]*?)<\/DINUS_PATCH>/g, (match, dataStr) => {
        try {
            const data = JSON.parse(dataStr.trim());
            if (data && typeof data.old === "string" && typeof data.new === "string") {
                patches.push({ old: data.old, new: data.new });
            }
        } catch (e) {}
        return "";
    }).trim();
        return { patches, cleanedMessage: cleaned };
}

function applyPatches(content, patches) {
    let result = content;
    for (const p of patches) {
        if (!result.includes(p.old)) {
            return { ok: false, content, error: "Could not find old text: " + p.old.slice(0, 80) };
        }
        result = result.replace(p.old, p.new);
    }
    return { ok: true, content: result };
}

function showPatchApproval(patches) {
    const details = document.getElementById("patch-details");
    details.innerHTML = "";
    patches.forEach((p, i) => {
        const entry = document.createElement("div");
            const oldLines = p.old.split("\n");
        const newLines = p.new.split("\n");
            let html = `<div class="diff-label">Edit ${i + 1}</div><div class="diff-box">`;
            oldLines.forEach(line => { html += `<span class="diff-line diff-old">- ${escapeHTML(line)}</span>`; });
        newLines.forEach(line => { html += `<span class="diff-line diff-new">+ ${escapeHTML(line)}</span>`; });
        html += '</div>';
        entry.innerHTML = html;
        details.appendChild(entry);
    });
    pendingPatches = patches;
    document.getElementById("patch-overlay").classList.add("visible");
}

function denyPendingPatch() {
    if (pendingPatches.length) {
        addAIMessage("system", "AI edit denied.");
    }
    pendingPatches = [];
    document.getElementById("patch-overlay").classList.remove("visible");
}

function applyPendingPatch() {
    const item = findItem(editingId);
    if (!item || !pendingPatches.length) {
        denyPendingPatch();
        return;
    }
    const result = applyPatches(item.content, pendingPatches);
    if (!result.ok) {
        toast(result.error);
        addAIMessage("system", "Edit was not applied: " + result.error);
        denyPendingPatch();
        return;
    }
    item.content = result.content;
    item.size = readableSize(new Blob([item.content]).size);
    saveWorkspace();
    document.getElementById("editor-text").value = item.content;
    document.getElementById("editor-status").textContent = "Saved (AI edit)";
    updateLineNumbers();
    updateHighlight();
    testPassed = false;
    document.getElementById("download-button").disabled = true;
    renderFiles();
    addAIMessage("system", "AI edit applied.");
    toast("Edit applied");
    pendingPatches = [];
    document.getElementById("patch-overlay").classList.remove("visible");
}

document.getElementById("apply-patch").onclick = applyPendingPatch;
document.getElementById("deny-patch").onclick = denyPendingPatch;
document.getElementById("patch-overlay").onclick = (e) => {
    if (e.target.id === "patch-overlay") denyPendingPatch();
};

document.getElementById("send-ai").onclick = sendAI;
document.getElementById("ai-text").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendAI(); }
});

async function sendAI() {
    if (aiBusy) return;
    const item = findItem(editingId || selectedId);

    const request = document.getElementById("ai-text").value.trim();
    if (!request) return;

    addAIMessage("user", request);
    document.getElementById("ai-text").value = "";
    aiBusy = true;
    document.getElementById("ai-thinking").classList.add("visible");

    try {
        const response = await askOllama(item, request);
            const parsed = parseAIPatches(response);
        if (parsed.cleanedMessage) {
            const cleaned = cleanText(parsed.cleanedMessage);
            await typeAIMessage(cleaned);
        }
            if (parsed.patches.length > 0) {
            if (item && editingId) {
                showPatchApproval(parsed.patches);
            } else {
                addAIMessage("system", "AI suggested edits but no file is open to apply them.");
            }
        }
    } catch (err) {
        addAIMessage("system", "AI request failed: " + err.message);
    } finally {
        aiBusy = false;
        document.getElementById("ai-thinking").classList.remove("visible");
    }
}

async function askOllama(item, request) {
    if (!ollamaModel) throw new Error("Ollama model not connected.");
        const resp = await fetch(ollamaEndpoint + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            model: ollamaModel,
            stream: false,
            messages: [{ role: "user", content: buildAIPrompt(item, request) }],
            options: { temperature: 0.2, num_predict: 1024 }
        })
    });
    const data = await resp.json();
        if (!resp.ok) throw new Error(data?.error || "HTTP " + resp.status);
        return data?.message?.content || "";
}

async function typeAIMessage(text) {
    const msg = document.createElement("div");
    msg.className = "ai-message";
    document.getElementById("ai-messages").appendChild(msg);
    for (let i = 0; i < text.length; i += 3) {
        msg.textContent += text.slice(i, i+3);
        const body = document.querySelector(".ai-body");
        body.scrollTop = body.scrollHeight;
        await new Promise(r => setTimeout(r, 7));
    }
}

/* =========================================================
       RUN / TEST (unchanged)
========================================================= */

document.getElementById("run-button").onclick = runTest;
document.getElementById("runner-exit").onclick = exitRunningMode;

function exitRunningMode() {
    const runner = document.getElementById("runner");
    runner.classList.remove("fullscreen");
    runner.classList.remove("visible");
}

async function runTest() {
    const item = findItem(editingId);
    if (!item) return;
    const code = document.getElementById("editor-text").value;
    const ext = (item.name.match(/\.[^.]+$/) || [""])[0].toLowerCase();
    const runner = document.getElementById("runner");
    const status = document.getElementById("runner-status");
    const output = document.getElementById("runner-output");

    runner.classList.add("visible");
    runner.classList.add("fullscreen");
    status.className = "runner-status";
    status.textContent = "Testing…";
    output.innerHTML = "";
    testPassed = false;
    document.getElementById("download-button").disabled = true;

    try {
        if (ext === ".js") {
            await runJavaScriptSafe(code, output);
        } else if (ext === ".ts") {
            throw new Error("TypeScript requires a compiler. Save/download the file and run it with tsc.");
        } else if (ext === ".html") {
            runHTML(code, output);
        } else if (ext === ".css") {
            runCSS(code, output);
        } else if (ext === ".json") {
            JSON.parse(code);
            output.textContent = "JSON check passed.";
        } else if (ext === ".py") {
            staticPythonCheck(code, output);
        } else {
            staticGeneralCheck(code, output);
        }
        testPassed = true;
        status.textContent = "Passed";
        status.classList.add("success");
        document.getElementById("download-button").disabled = false;
    } catch (err) {
        status.textContent = "Failed";
        status.classList.add("failure");
        output.textContent = "Error: " + err.message;
    }
}

function runJavaScriptSafe(code, output) {
    return new Promise((resolve, reject) => {
        const id = "dinus-" + Math.random().toString(36).slice(2);
        let done = false;

        function receive(e) {
            if (e.source !== frame.contentWindow) return;
            if (!e.data || e.data.id !== id) return;
            if (done) return;
            done = true;
            window.removeEventListener("message", receive);
            frame.remove();
            URL.revokeObjectURL(url);
            if (e.data.type === "error") { reject(new Error(e.data.message)); return; }
            output.textContent = e.data.output || "JavaScript ran successfully.";
            resolve();
        }

        window.addEventListener("message", receive);

        const escapedCode = JSON.stringify(code);
        const html = '<!doctype html>\n<html>\n<head><meta charset="utf-8"></head>\n<body>\n<script>\n(function() {\n    const id = ' + JSON.stringify(id) + ';\n    let output = "";\n    const orig = console.log;\n    console.log = function() {\n        output += Array.from(arguments).map(String).join(" ") + "\\n";\n        orig.apply(console, arguments);\n    };\n    window.onerror = function(msg, src, line) {\n        parent.postMessage({id, type:"error", message: String(msg) + " at line " + line}, "*");\n        return true;\n    };\n    try {\n        (new Function(' + escapedCode + '))();\n        parent.postMessage({id, type:"success", output}, "*");\n    } catch(e) {\n        parent.postMessage({id, type:"error", message: e && e.stack ? e.stack : String(e)}, "*");\n    }\n})();\n<\/script>\n</body>\n</html>';

        const blob = new Blob([html], { type: "text/html;charset=utf-8" });
        const url = URL.createObjectURL(blob);

        const frame = document.createElement("iframe");
        frame.sandbox = "allow-scripts allow-same-origin";
        frame.style.display = "none";
        frame.src = url;
        document.body.appendChild(frame);

        setTimeout(() => {
            if (!done) {
                done = true;
                window.removeEventListener("message", receive);
                frame.remove();
                URL.revokeObjectURL(url);
                reject(new Error("JavaScript test timed out."));
            }
        }, 5000);
    });
}

function runHTML(code, output) {
    output.innerHTML = "";
    const title = document.createElement("div");
    title.textContent = "HTML preview:";
    title.style.marginBottom = "8px";
    output.appendChild(title);
    const frame = document.createElement("iframe");
    frame.style.width = "100%";
    frame.style.height = "calc(100% - 20px)";
    frame.style.border = "1px solid #dfe9e3";
    frame.srcdoc = code;
    output.appendChild(frame);
}

function runCSS(code, output) {
    output.innerHTML = "";
    const frame = document.createElement("iframe");
    frame.style.width = "100%";
    frame.style.height = "calc(100% - 20px)";
    frame.style.border = "1px solid #dfe9e3";
    frame.srcdoc = `<!doctype html><html><style>${code}</style><body><div class="dinus-test">CSS test preview</div></body></html>`;
    output.appendChild(frame);
}

function staticPythonCheck(code, output) {
    if (!code.trim()) throw new Error("Python file is empty.");
    const lines = code.split("\n");
    let brackets = 0;
    lines.forEach((line, idx) => {
        const clean = line.split("#")[0];
        const quotes = (clean.match(/["']/g) || []).length;
        if (quotes % 2 !== 0) throw new Error("Possible unmatched quote on line " + (idx+1));
        for (const ch of clean) {
            if ("([{".includes(ch)) brackets++;
            if (")]}".includes(ch)) { brackets--; if (brackets < 0) throw new Error("Unexpected closing bracket on line " + (idx+1)); }
        }
    });
    if (brackets !== 0) throw new Error("Unbalanced brackets.");
    output.textContent = "Python static check passed.\n\nThis browser-only workspace does not execute Python itself.\nDownload the .py file to run it with Python on your Mac.";
}

function staticGeneralCheck(code, output) {
    if (!code.trim()) throw new Error("File is empty.");
    output.textContent = "Basic file check passed.\n\nThis language needs its own compiler/interpreter to execute.";
}

/* =========================================================
   DOWNLOAD
========================================================= */

document.getElementById("download-button").onclick = () => {
    if (!testPassed) { toast("Run Test successfully first."); return; }
    const item = findItem(editingId);
    if (!item) return;
    const content = document.getElementById("editor-text").value;
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = item.name;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast("Download started.");
};

/* =========================================================
   SIDEBAR NAV
========================================================= */

document.querySelectorAll(".nav").forEach(btn => {
    if (btn.id === "trash") return;
    btn.onclick = () => navigate(btn.dataset.path);
});

/* =========================================================
   DRAG TO AREA
========================================================= */

document.getElementById("file-area").ondragover = (e) => {
    e.preventDefault();
    document.getElementById("file-area").classList.add("drag-hover");
};
document.getElementById("file-area").ondragleave = () => {
    document.getElementById("file-area").classList.remove("drag-hover");
};
document.getElementById("file-area").ondrop = (e) => {
    e.preventDefault();
    document.getElementById("file-area").classList.remove("drag-hover");
    const id = e.dataTransfer.getData("text/plain");
    const item = findItem(id);
    if (!item || isBuiltin(item)) return;
    item.parent = currentPath;
    saveWorkspace();
    renderFiles();
};

/* =========================================================
   KEYBOARD
========================================================= */

document.addEventListener("keydown", (e) => {
    const isTyping = e.target.closest('input, textarea, select, [contenteditable="true"]');
    if (e.key === "Escape") { hideContextMenu(); closeCreate(); }
    if (e.key === "Delete" && selectedId && !editingId && currentPath !== "Trash" && !isTyping) deleteSelected();
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); document.getElementById("search").focus(); }
});

/* =========================================================
   INIT
========================================================= */

window.addEventListener('error', function(e) {
    toast('Error: ' + e.message);
});

document.getElementById("location").textContent = "Home";
renderFiles();
updateAIUI();

if (!ollamaModel) {
    refreshOllama();
}
</script>

</body>
</html>'''

def run_server():
    handler = http.server.SimpleHTTPRequestHandler
    class CustomHandler(handler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving Dinus Workspace at http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()