# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Polimorphic Encryption v3 (PRNG & CFF)
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
    version="13.0.0"
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

def generate_illusion_var(length=14):
    return "_" + "".join(random.choices("O0I1l", k=length))

# Generador Congruencial Lineal (LCG) en Python para replicar en Lua
class LCG:
    def __init__(self, seed):
        self.seed = seed
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

def obfuscate_single_layer(code: str) -> str:
    """
    Motor v3:
    - LCG PRNG para Polimorfismo Real (Caos matemático).
    - CFF Avanzado con ramas trampa.
    - Anti-Hooking de Entorno Nativo.
    """
    base_seed = random.randint(100000, 999999)
    prng = LCG(base_seed)
    
    encoded_blocks = []
    
    # POLIMORFISMO CAÓTICO: La operación cambia aleatoriamente según el PRNG
    for byte in code.encode('utf-8'):
        rand_val = prng.next()
        op_type = rand_val % 4
        shift = (rand_val // 100) % 256
        
        if op_type == 0:
            c = (byte + shift) % 256
        elif op_type == 1:
            c = (255 - byte)
        elif op_type == 2:
            c = (byte ^ (shift % 128)) # XOR básico simimulado
        else:
            c = (byte - shift) % 256
            if c < 0: c += 256
            
        encoded_blocks.append(f'"{c:02x}"')
    
    payload_array = ",".join(encoded_blocks)
    
    # Variables de ilusión
    v_data, v_out, v_state, v_idx, v_seed = (generate_illusion_var() for _ in range(5))
    f_tonum, f_char, f_insert, f_concat, f_type = (generate_illusion_var() for _ in range(5))
    v_env, v_exec, v_math_floor = (generate_illusion_var() for _ in range(3))
    
    # Estados de CFF
    S_INIT = random.randint(100, 199)
    S_FAKE = random.randint(200, 299)
    S_DECODE = random.randint(300, 399)
    S_ADVANCE = random.randint(400, 499)
    S_END = random.randint(500, 599)
    
    # LCG y Setup en Lua
    setup_code = (
        f"local {f_tonum},{f_char},{f_insert},{f_concat},{f_type}=tonumber,string.char,table.insert,table.concat,type;"
        f"local {v_math_floor}=math.floor;"
        f"local {v_data}={{{payload_array}}};"
        f"local {v_out}={{}};"
        f"local {v_state}={S_INIT};"
        f"local {v_idx}=1;"
        f"local {v_seed}={base_seed};"
    )
    
    # LOOP DE DESCIFRADO (CFF CAÓTICO + PRNG)
    loop_code = (
        f"while {v_state}~={S_END} do "
        # ESTADO INICIAL
        f"if {v_state}=={S_INIT} then "
        f"if {v_idx}>#{v_data} then {v_state}={S_END} else {v_state}={S_FAKE} end;"
        # ESTADO FALSO (Ramas Muertas y cálculos basura para desviar la atención)
        f"elseif {v_state}=={S_FAKE} then "
        f"local _junk = {v_seed} % 2;"
        f"if _junk == 5 then {v_state}={S_END} else {v_state}={S_DECODE} end;"
        # ESTADO DE DECODIFICACIÓN (Usando el LCG)
        f"elseif {v_state}=={S_DECODE} then "
        f"{v_seed}=({v_seed} * 1664525 + 1013904223) % 4294967296;"
        f"local op={v_seed} % 4;"
        f"local sh=({v_math_floor}({v_seed} / 100)) % 256;"
        f"local m={f_tonum}({v_data}[{v_idx}], 16);"
        f"local d;"
        f"if op==0 then d=(m-sh)%256; if d<0 then d=d+256 end;"
        f"elseif op==1 then d=(255-m);"
        f"elseif op==2 then "
        # Lógica XOR básica compatible con Lua 5.1 sin bit32
        f"local a,b,p,r=m,sh%128,1,0;"
        f"while a>0 or b>0 do local ax,bx=a%2,b%2; if ax~=bx then r=r+p end; a={v_math_floor}(a/2); b={v_math_floor}(b/2); p=p*2; end;"
        f"d=r;"
        f"else d=(m+sh)%256; end;"
        f"{f_insert}({v_out},{f_char}(d));"
        f"{v_state}={S_ADVANCE};"
        # ESTADO DE AVANCE
        f"elseif {v_state}=={S_ADVANCE} then "
        f"{v_idx}={v_idx}+1;"
        f"{v_state}={S_INIT};"
        f"end;"
        f"end;"
    )
    
    # ANTI-HOOKING: Detectar si load/table.concat han sido modificados por un depurador
    run_logic = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_exec}={v_env}[{f_char}(108,111,97,100)] or {v_env}[{f_char}(108,111,97,100,115,116,114,105,110,103)];"
        f"if not tostring({v_exec}):match('function') then return end;" # Anti-Hook Básico
        f"local f,e={v_exec}({f_concat}({v_out}));"
        f"if {f_type}(f)=='function' then return f(...) else error(tostring(e)) end;"
    )
    
    return f"return(function(...) {setup_code}{loop_code}{run_logic} end)(...);"

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
            mode_used=f"Polymorphic Engine v3 ({min(layers_to_apply, 10)}-Layers)",
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
