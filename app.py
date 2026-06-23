# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Encryption (Opaque Predicates & Multi-Layer)
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
    version="11.0.0"
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

# SISTEMA ANTI-SUEÑO (KEEP-ALIVE)
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

# Ocultación de variables
def generate_illusion_var(length=14):
    return "_" + "".join(random.choices("O0I1l", k=length))

# Derivación matemática compleja para las llaves
def math_obf(n: int) -> str:
    choice = random.randint(1, 3)
    if choice == 1:
        a = random.randint(100, 999)
        return f"({a + n}-{a})"
    elif choice == 2:
        a = random.randint(2, 7)
        return f"({n * a}/{a})"
    else:
        elements = random.randint(2, 6)
        table_str = "{" + ",".join(["1"] * elements) + "}"
        return f"({n - elements}+#{table_str})"

def obfuscate_single_layer(code: str) -> str:
    """
    Motor de Ofuscación Avanzado con protección anti-IA y anti-descompiladores.
    """
    key_base = random.randint(20, 200)
    
    # 1. MÚLTIPLES CAPAS DE CIFRADO
    encoded_bytes = bytearray()
    for i, byte in enumerate(code.encode('utf-8')):
        c1 = (byte + (i % 256)) % 256   # Capa A: Desplazamiento posicional
        c2 = (255 - c1)                 # Capa B: Inversión de bits
        c3 = (c2 + key_base) % 256      # Capa C: Desplazamiento de llave estática
        encoded_bytes.append(c3)
        
    hex_str = encoded_bytes.hex()
    
    # STRING SPLITTING (Fragmentación del payload hex)
    sp1 = len(hex_str) // 3
    sp2 = sp1 * 2
    part1, part2, part3 = hex_str[:sp1], hex_str[sp1:sp2], hex_str[sp2:]
    
    # Variables fantasma
    v_data, v_out, v_key, v_state, v_idx = (generate_illusion_var() for _ in range(5))
    f_sub, f_tonum, f_char, f_insert, f_concat = (generate_illusion_var() for _ in range(5))
    v_env, v_exec = (generate_illusion_var() for _ in range(2))
    
    # SETUP - Reconstrucción tardía
    setup_code = (
        f"local {f_sub},{f_tonum},{f_char},{f_insert},{f_concat}=string.sub,tonumber,string.char,table.insert,table.concat;"
        f"local {v_data}=\"{part1}\"..\"{part2}\"..\"{part3}\";"
        f"local {v_out}={{}};"
        f"local {v_state}=1;"
        f"local {v_idx}=1;"
        f"local {v_key}={math_obf(key_base)};"
    )
    
    # LOOP DE DESCIFRADO - Opaque Predicates integrados
    loop_code = (
        f"while {v_state}~=0 do "
        f"if {v_state}==1 then "
        f"if {v_idx}>#{v_data} then {v_state}=4 else {v_state}=2 end;"
        f"elseif {v_state}==2 then "
        f"local s={f_sub}({v_data},{v_idx},{v_idx}+1);"
        f"if s==\"\" then {v_state}=4;else "
        f"if ({v_idx}*({v_idx}+1))%2==0 then " # <--- OPAQUE PREDICATE (Siempre True)
        f"local m={f_tonum}(s,16);"
        f"local c3=(m-{v_key})%256;"
        f"local c2=255-c3;"
        f"local r_idx=math.floor(({v_idx}-1)/2);"
        f"local dec=(c2-(r_idx%256))%256;"
        f"{f_insert}({v_out},{f_char}(dec));"
        f"{v_idx}={v_idx}+2;"
        f"{v_state}=1;"
        f"else {v_state}=0 end;"
        f"end;"
        f"elseif {v_state}==4 then "
        f"{v_state}=0;"
        f"end;"
        f"end;"
    )
    
    # EXECUÇÃO ANTI-HOOK
    run_logic = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_exec}={v_env}[{f_char}(108,111,97,100)] or {v_env}[{f_char}(108,111,97,100,115,116,114,105,110,103)];"
        f"local f,e={v_exec}({f_concat}({v_out}));"
        f"if type(f)=='function' then return f(...) else error(tostring(e)) end;"
    )
    
    return f"return(function(...) {setup_code}{loop_code}{run_logic} end)(...);"

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    actual_layers = max(1, min(requested_layers, 10))
    
    current_code = code
    for _ in range(actual_layers):
        current_code = obfuscate_single_layer(current_code)
        
    # BANNER ORIGINAL RESTAURADO COMPLETAMENTE
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
            return ObfuscateResponse(success=False, error="El código está vacío")
        
        max_size = 15 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="El código original excede el límite permitido")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        obfuscated = obfuscate_code(request.code, request.mode, layers_to_apply)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used=f"Military Core ({min(layers_to_apply, 10)}-Layers)",
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
        return {"error": "Frontend não encontrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
