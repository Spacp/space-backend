<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPACE OBFUSCATOR - Premium Lua Protection</title>
    
    <link class="favicon" rel="icon" type="image/png" href="Space.png">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/cascadia-code@4.2.1/index.min.css">
    
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        :root {
            --bg-panel: rgba(10, 10, 14, 0.45);
            --bg-header: rgba(5, 5, 8, 0.3);
            --border-color: rgba(255, 255, 255, 0.15);
            --text-main: #f3f4f6;
            --btn-white: #ffffff;
            --btn-white-hover: #e5e5e5;
            --font-title: 'Syne', sans-serif;
            --font-ui: 'Inter', system-ui, sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-image: url('OMG.png'); 
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #050508; 
            color: var(--text-main);
            font-family: var(--font-ui);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            user-select: none;
        }

        .app-container {
            display: flex;
            flex-direction: column;
            max-width: 1100px; 
            margin: 0 auto;
            width: 100%;
            padding: 0 24px 20px 24px;
            flex: 1;
        }

        .header {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 30px 0 20px 0;
        }

        .logo h1 {
            font-family: var(--font-title);
            font-size: 2.4rem;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 255, 255, 0.5), 0 0 30px rgba(255, 255, 255, 0.3);
            letter-spacing: 1px;
        }

        .subtitle {
            font-size: 0.9rem;
            color: #8b92a5;
            font-weight: 500;
            letter-spacing: 1.5px;
            margin-top: 6px;
        }

        .main-content {
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 100%;
        }

        .panel {
            background: var(--bg-panel);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--border-color);
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.55);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            width: 100%;
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            border-bottom: 1px solid var(--border-color);
            background-color: var(--bg-header);
        }

        .panel-header h2 {
            font-size: 0.85rem;
            font-weight: 600;
            color: #d1d5db;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .editor-container {
            width: 100%;
            height: 420px;
            position: relative;
        }

        .monaco-editor,
        .monaco-editor-background,
        .monaco-editor .margin,
        .monaco-editor .minimap,
        .monaco-editor .minimap-shadow-visible,
        .monaco-editor .minimap-decorations-layer,
        .monaco-editor .minimap canvas {
            background-color: transparent !important;
            background: transparent !important;
        }

        .action-center {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 15px 0;
        }

        button {
            font-family: var(--font-ui);
            cursor: pointer;
            border: none;
            border-radius: 4px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-action-primary {
            background-color: var(--btn-white);
            color: #000000;
            padding: 14px 40px;
            font-size: 0.95rem;
            font-weight: 700;
            border-radius: 6px;
            box-shadow: 0 4px 15px rgba(255, 255, 255, 0.15);
        }

        .btn-action-primary:hover {
            background-color: var(--btn-white-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25);
        }

        .btn-secondary {
            background-color: rgba(255, 255, 255, 0.05);
            color: #d1d5db;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 14px;
            font-size: 0.8rem;
            border-radius: 4px;
        }

        .btn-secondary:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }

        #anti-inspect-container {
            position: fixed;
            bottom: 24px;
            right: 24px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 9999;
            pointer-events: none;
        }

        .security-toast {
            background: var(--bg-panel);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 12px 20px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
            opacity: 0;
            transform: translateX(120%);
            transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .security-toast.show { opacity: 1; transform: translateX(0); }
        .security-toast.fade-out { opacity: 0; transform: translateY(-20px) scale(0.95); transition: opacity 0.4s ease, transform 0.4s ease; }
        .security-toast i { color: #ef4444; }
        .security-toast.info-toast i { color: #10b981; }

        .footer { width: 100%; max-width: 1100px; margin: 40px auto 20px auto; padding: 0 24px; text-align: left; }
        .footer-line { height: 1px; background: linear-gradient(90deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%); width: 100%; margin-bottom: 16px; }
        .footer-content { font-size: 0.85rem; color: #8b92a5; font-weight: 400; line-height: 1.6; }
        .footer-content a { color: #38bdf8; text-decoration: none; font-weight: 500; transition: color 0.2s ease; }
        .footer-content a:hover { color: #7dd3fc; text-decoration: underline; }

        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spin { animation: spin 1s linear infinite; }
    </style>
</head>
<body>

    <div class="app-container">
        <header class="header">
            <div class="logo">
                <h1>SPACE</h1>
            </div>
            <span class="subtitle">Premium Lua Protection</span>
        </header>

        <main class="main-content">
            <div class="panel" id="panelInput">
                <div class="panel-header">
                    <h2><i data-lucide="code" width="16"></i> Script de Entrada</h2>
                    <button id="clearInput" class="btn-secondary"><i data-lucide="trash-2" width="14"></i> Limpiar</button>
                </div>
                <div id="inputEditor" class="editor-container"></div>
            </div>

            <div class="action-center">
                <button id="obfuscateBtn" class="btn-action-primary">
                    <i data-lucide="zap" width="18"></i> Ofuscar Código
                </button>
            </div>

            <div class="panel" id="panelOutput">
                <div class="panel-header">
                    <h2><i data-lucide="shield-check" width="16"></i> Resultado Ofuscado</h2>
                    <button id="copyOutput" class="btn-secondary"><i data-lucide="copy" width="14"></i> Copiar</button>
                </div>
                <div id="outputEditor" class="editor-container"></div>
            </div>
        </main>
    </div>

    <footer class="footer">
        <div class="footer-line"></div>
        <div class="footer-content">
            <div>Para total transparencia, puedes acceder al código fuente de Prometheus aquí: ➡ <a href="https://github.com/wcrddn/Prometheus" target="_blank" rel="noopener noreferrer">Repositorio de GitHub</a></div>
            <div>Para obtener más información sobre la licencia AGPL-3.0, visita: ➡ <a href="https://github.com/prometheus-lua/Prometheus/blob/a4b00a2395e9982298fe76c7b055c755df25e6e9/LICENSE" target="_blank" rel="noopener noreferrer">Detalles de la Licencia GNU AGPL-3.0</a></div>
        </div>
    </footer>

    <div id="anti-inspect-container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js"></script>
    <script>
        const blockKeys = (e) => {
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['I','i','J','j','C','c'].includes(e.key)) || (e.ctrlKey && ['U','u','S','s'].includes(e.key))) {
                e.preventDefault();
                showToast("Acceso denegado. Inspección bloqueada.");
            }
        };
        document.addEventListener('keydown', blockKeys, { capture: true });
        document.addEventListener('contextmenu', e => { e.preventDefault(); showToast("Clic derecho deshabilitado."); }, { capture: true });

        lucide.createIcons();

        const antiInspectContainer = document.getElementById('anti-inspect-container');
        
        function showToast(message, type = 'error') {
            const toast = document.createElement('div');
            toast.className = `security-toast ${type === 'info' ? 'info-toast' : ''}`;
            const icon = type === 'info' ? 'check-circle' : 'shield-alert';
            toast.innerHTML = `<i data-lucide="${icon}" width="16"></i> ${message}`;
            
            antiInspectContainer.appendChild(toast);
            lucide.createIcons();
            
            requestAnimationFrame(() => {
                setTimeout(() => { toast.classList.add('show'); }, 10);
            });

            setTimeout(() => {
                toast.classList.remove('show');
                toast.classList.add('fade-out');
                setTimeout(() => toast.remove(), 400); 
            }, 2500);
        }

        const oldClearBtn = document.getElementById('clearInput');
        const newClearBtn = oldClearBtn.cloneNode(true);
        oldClearBtn.parentNode.replaceChild(newClearBtn, oldClearBtn);
        
        const oldObfuscateBtn = document.getElementById('obfuscateBtn');
        const newObfuscateBtn = oldObfuscateBtn.cloneNode(true);
        oldObfuscateBtn.parentNode.replaceChild(newObfuscateBtn, oldObfuscateBtn);

        require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.38.0/min/vs' }});

        let editorIn;
        let editorOut;

        document.fonts.ready.then(() => {
            require(['vs/editor/editor.main'], function () {
                monaco.languages.registerCompletionItemProvider('lua', {
                    provideCompletionItems: function(model, position) {
                        var suggestions = [
                            { label: 'local', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'local ' },
                            { label: 'function', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'function ' },
                            { label: 'end', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'end' },
                            { label: 'if', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'if ' },
                            { label: 'then', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'then' },
                            { label: 'else', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'else' },
                            { label: 'for', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'for ' },
                            { label: 'while', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'while ' },
                            { label: 'do', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'do' },
                            { label: 'return', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'return ' },
                            { label: 'print', kind: monaco.languages.CompletionItemKind.Function, insertText: 'print("${1:message}")', insertTextRules: 4 },
                            { label: 'loadstring', kind: monaco.languages.CompletionItemKind.Function, insertText: 'loadstring(game:HttpGet("${1:url}"))()', insertTextRules: 4 }
                        ];
                        return { suggestions: suggestions };
                    }
                });

                monaco.editor.defineTheme('PDark', {
                    base: 'vs-dark',
                    inherit: true,
                    rules: [
                        { token: 'keyword', foreground: '#BB9AF7', fontStyle: 'bold' },
                        { token: 'string', foreground: '#9ECE6A' },
                        { token: 'number', foreground: '#FF9E64' },
                        { token: 'comment', foreground: '#666666', fontStyle: 'italic' },
                        { token: 'operator', foreground: '#89DDFF' },
                        { token: 'entity.name.function', foreground: '#7AA2F7' }
                    ],
                    colors: {
                        'editor.background': '#00000000',
                        'editor.lineHighlightBackground': '#1f1f1f50',
                        'editorLineNumber.foreground': '#5a5a6e',
                        'editorIndentGuide.background': '#1a1a1a50',
                    }
                });

                editorIn = monaco.editor.create(document.getElementById('inputEditor'), {
                    value: '', 
                    language: 'lua',
                    theme: 'PDark',
                    fontSize: 14,
                    fontFamily: "'Cascadia Code', Consolas, monospace",
                    padding: { top: 16, bottom: 16 }, 
                    minimap: { enabled: true },
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    scrollbar: { alwaysConsumeMouseWheel: false }
                });

                editorOut = monaco.editor.create(document.getElementById('outputEditor'), {
                    value: '-- El código protegido aparecerá aquí...', 
                    language: 'plaintext', 
                    theme: 'PDark',
                    fontSize: 14,
                    fontFamily: "'Cascadia Code', Consolas, monospace",
                    padding: { top: 16, bottom: 16 }, 
                    minimap: { 
                        enabled: true,
                        renderCharacters: false
                    }, 
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    readOnly: true, 
                    domReadOnly: true,
                    contextmenu: false, 
                    wordWrap: "off" 
                });

                setTimeout(() => monaco.editor.remeasureFonts(), 800);
            });
        });

        newClearBtn.addEventListener('click', () => {
            if(editorIn) editorIn.setValue('');
            if(editorOut) editorOut.setValue('-- El código protegido aparecerá aquí...');
        });

        document.getElementById('copyOutput').addEventListener('click', () => {
            if(editorOut) {
                const outVal = editorOut.getValue();
                if(!outVal || outVal.startsWith('-- El código protegido')) return;
                navigator.clipboard.writeText(outVal);
                showToast("Código copiado al portapapeles.", "info");
            }
        });

        newObfuscateBtn.addEventListener('click', async () => {
            if(!editorIn || !editorOut) return;
            const code = editorIn.getValue();
            if(!code || code.trim() === '') {
                showToast("Por favor introduce un código Lua válido.", "error");
                return;
            }

            try {
                newObfuscateBtn.innerHTML = `<i data-lucide="loader-2" width="18" class="spin"></i> Protegiendo...`;
                lucide.createIcons();
                
                const urlBackend = 'https://space-backend-4k9r.onrender.com/api/obfuscate';
                
                const response = await fetch(urlBackend, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        code: code, 
                        mode: "heavy", 
                        layers: 5 
                    })
                });
                
                const data = await response.json();
                
                if (response.ok && data.obfuscated_code) {
                    editorOut.setValue(data.obfuscated_code);
                    showToast("Ofuscación completada.", "info");
                } else {
                    const errorDetail = data.error || data.detail || 'El servidor denegó la petición.';
                    editorOut.setValue(`-- [ERROR DEL SERVIDOR LUA]\n-- ${errorDetail}`);
                    showToast("Error al procesar el código.", "error");
                }
            } catch (err) {
                editorOut.setValue(`-- [ERROR DE CONEXIÓN]\n-- No se pudo conectar con el servidor backend en Render.\n-- Detalle: ${err.message}`);
                showToast("Error de red o caída de servidor.", "error");
            } finally {
                newObfuscateBtn.innerHTML = `<i data-lucide="zap" width="18"></i> Ofuscar Código`;
                lucide.createIcons();
            }
        });
    </script>
</body>
</html>
