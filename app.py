# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Polimorphic Engine v6 (CTF Unbreakable)
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
import urllib.request
import threading

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Military-Grade Lua Protection Service",
    version="16.0.0"
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
    layers: Optional[int] = 5

class ObfuscateResponse(BaseModel):
    success: bool
    obfuscated_code: Optional[str] = None
    error: Optional[str] = None
    original_size: int = 0
    obfuscated_size: int = 0
    mode_used: str = ""
    timestamp: str = ""

def ping_self():
    import time
    while True:
        try:
            urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=5)
        except:
            pass
        time.sleep(600)

@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=ping_self, daemon=True)
    thread.start()

def generate_illusion_var():
    # Longitudes erráticas para romper patrones visuales
    length = random.randint(5, 25)
    return "_" + "".join(random.choices("O0I1l", k=length))

# PRNG Multi-Estado (Python Simulator)
class MultiStatePRNG:
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.m = 4294967296

    def next(self):
        self.s1 = (self.s1 * 1664525 + 1013904223) % self.m
        self.s2 = (self.s2 * 22695477 + 1) % self.m
        self.s3 = (self.s3 + self.s1) % self.m
        return (self.s1 + self.s2 + self.s3) % 256

def obfuscate_single_layer(code: str) -> str:
    """
    Motor v6 Supremo (Derrota de Análisis Estático/Dinámico):
    - Padding Dinámico para payloads cortos.
    - PRNG Multi-Estado.
    - Cifrado en cadenas escapadas nativas (\\ddd).
    - Múltiples trampas anti-emulación y corrupción silenciosa.
    """
    # 1. PADDING DE PAYLOAD (Evita ataques a scripts cortos)
    pad_len = random.randint(50, 150)
    padding = "--" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=pad_len)) + "\n"
    code = padding + code

    # 2. SEMILLAS MULTI-ESTADO
    s1 = random.randint(100000, 999999)
    s2 = random.randint(100000, 999999)
    s3 = random.randint(100000, 999999)
    prng = MultiStatePRNG(s1, s2, s3)
    
    # 3. ENCRIPTACIÓN ESCAPADA (Evita tablas HEX legibles)
    enc_str = ""
    for byte in code.encode('utf-8'):
        sh = prng.next()
        c = (byte + sh) % 256
        enc_str += f"\\{c:03d}"
        
    # 4. FRAGMENTACIÓN DE STRINGS (String Splitting)
    # Partimos la mega cadena en fragmentos aleatorios para ensamblarla en Lua
    chunk_size = random.randint(2000, 4000)
    chunks = [enc_str[i:i+chunk_size] for i in range(0, len(enc_str), chunk_size)]
    
    v_chunks = [generate_illusion_var() for _ in chunks]
    chunk_declarations = "".join([f"local {v}=\"{c}\";" for v, c in zip(v_chunks, chunks)])
    payload_concat = "local " + generate_illusion_var() + "=" + "..".join(v_chunks) + ";"
    v_data = payload_concat.split("=")[0].replace("local ", "")
    
    # Variables Opacas
    v_s1, v_s2, v_s3 = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_env, v_idx, v_time = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_reader, v_ok, v_res = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    
    # SETUP LUA & ANTI-DEBUG GLOBAL
    # Se validan globales silenciosamente. Si alguien modificó el entorno, s2 se corrompe.
    setup_code = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_s1},{v_s2},{v_s3}={s1},{s2},{s3};"
        f"local _e={{\"pairs\",\"ipairs\",\"tostring\",\"pcall\",\"type\"}};"
        f"for i=1,5 do if type({v_env}[_e[i]])~=\"function\" then {v_s2}={v_s2}+1 end end;"
        f"{chunk_declarations}{payload_concat}"
        f"local {v_idx}=1;"
        f"local {v_time}=os.clock and os.clock() or 0;"
    )
    
    # READER FUNCTION: Timing Checks dinámicos y Cifrado Multi-estado
    reader_func = (
        f"local function {v_reader}() "
        f"if {v_idx}>#{v_data} then return nil end;"
        
        # Timing Check Distribuido (Corrupción Silenciosa)
        f"local _now=os.clock and os.clock() or 0;"
        f"if (_now-{v_time})>0.5 then {v_s3}={v_s3}+1 end;"
        f"{v_time}=_now;"
        
        # PRNG Matemático
        f"{v_s1}=({v_s1}*1664525+1013904223)%4294967296;"
        f"{v_s2}=({v_s2}*22695477+1)%4294967296;"
        f"{v_s3}=({v_s3}+{v_s1})%4294967296;"
        f"local sh=({v_s1}+{v_s2}+{v_s3})%256;"
        
        f"local m=string.byte({v_data},{v_idx});"
        f"local dec=(m-sh)%256;"
        f"if dec<0 then dec=dec+256 end;"
        f"{v_idx}={v_idx}+1;"
        f"return string.char(dec);"
        f"end;"
    )
    
    # EXECUTION WRAPPER: Ocultamos el load en un pcall silencioso
    run_logic = (
        f"local _l={v_env}[\"\\108\\111\\97\\100\"] or {v_env}[\"\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103\"];"
        f"local {v_ok},{v_res}=pcall(_l,{v_reader});"
        f"if {v_ok} and type({v_res})==\"function\" then return {v_res}(...) end;"
    )
    
    # Retorno en una sola línea continua
    return f"return(function(...) {setup_code}{reader_func}{run_logic} end)(...);"

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    actual_layers = max(1, min(requested_layers, 10))
    
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
    return f"{banner}\n\n\n{current_code}"

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
            return ObfuscateResponse(success=False, error="El código está vacío")
        
        max_size = 15 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="El código excede el límite permitido")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        obfuscated = obfuscate_code(request.code, request.mode, layers_to_apply)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used=f"Polymorphic Engine v6 ({min(layers_to_apply, 10)}-Layers)",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return ObfuscateResponse(success=False, error=f"Error inesperado: {str(e)}")

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    @app.get("/app")
    async def serve_frontend():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend no encontrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
