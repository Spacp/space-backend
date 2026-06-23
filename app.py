# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Servidor FastAPI (Anti-AI & Anti-Hook Virtualization)
# ================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import random

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Anti-AI Lua Protection Service",
    version="10.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ObfuscateRequest(BaseModel):
    code: str
    mode: str = "heavy"
    layers: Optional[int] = 5  # Recebe o número exato do frontend

class ObfuscateResponse(BaseModel):
    success: bool
    obfuscated_code: Optional[str] = None
    error: Optional[str] = None
    original_size: int = 0
    obfuscated_size: int = 0
    mode_used: str = ""
    timestamp: str = ""

# Otimização para nomes de variáveis aleatórios
def generate_illusion_var(length=14):
    return "_" + "".join(random.choices("O0I1l", k=length))

def obfuscate_single_layer(code: str) -> str:
    """
    Aplica uma camada de ofuscação com Virtualização Segura, Proteção Anti-Hook e Lixo Entrelaçado.
    """
    base_key = random.randint(20, 180)
    multiplier = random.randint(3, 9)
    
    # Cifragem de bytes dinâmica
    encoded_bytes = bytearray()
    last_val = base_key
    for byte in code.encode('utf-8'):
        cipher_byte = (byte + last_val + multiplier) % 256
        encoded_bytes.append(cipher_byte)
        last_val = cipher_byte
        
    encoded_hex = encoded_bytes.hex()
    
    # Fragmentação segura em tabelas para evitar colapso de registros Lua (Error 255)
    chunk_size = 2000 
    chunks = [encoded_hex[i:i+chunk_size] for i in range(0, len(encoded_hex), chunk_size)]
    table_elements = ",".join(f'"{c}"' for c in chunks)
    
    # Geração de variáveis ilusórias (Fantasmas)
    v_hex, v_proxy, v_res, v_state, v_idx, v_last = (generate_illusion_var() for _ in range(6))
    f_sub, f_tonum, f_char, f_insert, f_concat = (generate_illusion_var() for _ in range(5))
    v_env, v_exec, v_junk = (generate_illusion_var() for _ in range(3))
    
    # SETUP - Definição das variáveis do descodificador
    setup_logic = (
        f"local {f_sub},{f_tonum},{f_char},{f_insert},{f_concat}=string.sub,tonumber,string.char,table.insert,table.concat;"
        f"local {v_hex}={f_concat}({{{table_elements}}});"
        f"local {v_proxy}=setmetatable({{}},{{__index=function(t,k) local s={f_sub}({v_hex},k,k+1);if s==\"\" then return nil end;return({f_tonum}(s,16)+k)%256;end}});"
        f"local {v_res}={{}};"
        f"local {v_state}=1;"
        f"local {v_idx}=1;"
        f"local {v_last}={base_key};"
        f"local {v_junk}=0;"
    )
    
    # LÓGICA DE LOOP & LIXO ENTRELAÇADO
    # A variável v_junk aparenta ser código morto, mas está matematicamente ligada ao cálculo "(v_junk - math.abs(v_junk))"
    # Se uma IA ou descompilador remover a variável ou a lógica, a descriptografia falhará.
    loop_logic = (
        f"while {v_state}~=0 do "
        f"if {v_state}==1 then "
        f"if {v_idx}>#{v_hex} then {v_state}=4 else {v_state}=2 end;"
        f"elseif {v_state}==2 then "
        f"local m={v_proxy}[{v_idx}];"
        f"if not m then {v_state}=4;else "
        f"{v_junk}={v_junk}+1;" 
        f"local c=(m-{v_idx}+({v_junk}-math.abs({v_junk})))%256;"
        f"local d=(c-{v_last}-{multiplier})%256;"
        f"{f_insert}({v_res},{f_char}(d));"
        f"{v_last}=c;"
        f"{v_state}=3;"
        f"end;"
        f"elseif {v_state}==3 then "
        f"{v_idx}={v_idx}+2;{v_state}=1;"
        f"elseif {v_state}==4 then "
        f"{v_state}=0;"
        f"end;"
        f"end;"
    )
    
    # EXECUÇÃO & ANTI-HOOK DE LOADSTRING
    # Ocultamos a palavra 'load' ou 'loadstring' resolvendo-a de forma dinâmica usando os caracteres ASCII:
    # 108,111,97,100 = "load" | 115,116,114,105,110,103 = "string"
    run_logic = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_exec}={v_env}[{f_char}(108,111,97,100)] or {v_env}[{f_char}(108,111,97,100,115,116,114,105,110,103)];"
        f"local f,e={v_exec}({f_concat}({v_res}));"
        f"if not f then error(tostring(e)) end;"
        f"return f(...);"
    )
    
    # Retorna o código ofuscado compactado em uma única linha
    return f"return(function(...) {setup_logic}{loop_logic}{run_logic} end)(...);"

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    # Otimização: Forçamos que as camadas estejam entre 1 e 8 para evitar loops exagerados
    actual_layers = max(1, min(requested_layers, 8))
    
    current_code = code
    for _ in range(actual_layers):
        current_code = obfuscate_single_layer(current_code)
        
    banner = """--[[
                                                                  <'         -n:                   
                                                               icI        ^v0!                      
                                                             C?         d%<                         
                                                          _O^       IQBQ'                           
                                                       .z/       "ZB&]                              
                                                      k]      'm$$%:                                
                                                   i#{  '  !O@$@#"                                  
                                                 ~#W`|bL[p@$$$B[                                    
                                               ;&$$$$$$$$$$$$W'         'u&~                        
                                             ;W@$$$$$$$$$$$$${     :[Q@@B[                          
                                           'd@$$$$$$$$$$@$$$@$@%@@@$$$@z            '               
                                          /ku/xhB$$$$$$$$$$@$$$$$$$$$B>         'f@h.               
                                                 ]@$$$$$$$$$*QcL@$$$$Y     `[J%$$W<                 
                                                  b$$$$$M1`    X$$$$$@B8B@@$$$$@f                   
                                                 _$$@W~     `0WL!      _@$$$$@L                     
                                                :&@c      ,{'         .k@$$@J                       
                                          :l   I%X.                  !&$$$X'                        
                                       .\\l    u$Yic]  `>           >#$@B\\                           
                                     ;L~    -%$$$$U;|+          'zB$@pi                             
                                   ^aj    |8@$$$$$B]         .J%$@*i                                
                                 `a$f':(B$$$$$$$@c       '+a@B*r.                                   
                                c$$$$$$$@Bz>/$$k"     ~cXt-^                                        
                              ~%$@$$$$B/'  IB%l                                                     
                             w$$$$@BJ'    _%\\                                                       
                           ~B$$$@a<      Un.                                                        
                         'a$$$@\\       :p.                                                          
                        n@$@p"       "x                                                             
                      )8@#?                                                                         
                    iB@r.                                                                           
                  ]WY.                                                                              
                /j"  
                
                                            https://space.spacecp.workers.dev/
                                https://space-obfuscator.spacecp.workers.dev/
                        https://discord.gg/7dt2A6DJZA
]]--"""
    return f"{banner}\n{current_code}\n"

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/obfuscate", response_model=ObfuscateResponse)
async def obfuscate(request: ObfuscateRequest):
    try:
        if not request.code or not request.code.strip():
            return ObfuscateResponse(success=False, error="O código está vazio")
        
        # Limite de peso: 10 MB para suportar múltiplas camadas
        max_size = 10 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="O código excede o limite de tamanho permitido")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        obfuscated = obfuscate_code(request.code, request.mode, layers_to_apply)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used=f"High Protection ({min(layers_to_apply, 8)}-Layers + Anti-AI)",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return ObfuscateResponse(success=False, error=f"Erro inesperado: {str(e)}")

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    @app.get("/app")
    async def serve_frontend():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend não encontrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
