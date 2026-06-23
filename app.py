# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Polimorphic Engine v4 (Memory-Leak Prevention)
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
    version="14.0.0"
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

def generate_illusion_var(length=16):
    return "_" + "".join(random.choices("O0I1l", k=length))

def generate_math_seed(target_seed: int) -> str:
    """Oculta la semilla hardcodeada usando matemáticas engañosas"""
    offset = random.randint(10000, 99999)
    multiplier = random.randint(2, 5)
    base = (target_seed - offset) / multiplier
    return f"({base}*{multiplier}+{offset})"

# Generador LCG Dinámico y Mutante
class DynamicLCG:
    def __init__(self):
        self.seed = random.randint(100000, 999999)
        # Parámetros aleatorios pero válidos para un LCG (a = impar, c = impar)
        self.a = random.randint(10000, 99999) | 1 
        self.c = random.randint(10000, 99999) | 1
        self.m = 2**32

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

def obfuscate_single_layer(code: str) -> str:
    """
    Motor v4 (Anti-Memory Dump):
    - LCG de parámetros dinámicos.
    - Cifrado Polinómico.
    - Lua 'load()' con Reader Function (Evita table.concat).
    - Anti-Debug con debug.getinfo.
    """
    lcg = DynamicLCG()
    initial_seed = lcg.seed
    
    encoded_blocks = []
    
    # Cifrado Polinómico y LCG
    for i, byte in enumerate(code.encode('utf-8')):
        rand_val = lcg.next()
        shift = (rand_val % 256)
        # Sustitución no lineal: (Byte + Shift + Posición) % 256
        c = (byte + shift + (i % 50)) % 256
        encoded_blocks.append(f'"{c:02x}"')
    
    payload_array = ",".join(encoded_blocks)
    
    # Variables de ilusión
    v_data, v_idx, v_seed = (generate_illusion_var() for _ in range(3))
    f_tonum, f_char, f_math_floor = (generate_illusion_var() for _ in range(3))
    v_reader, v_env, v_exec = (generate_illusion_var() for _ in range(3))
    
    # Setup del Entorno
    setup_code = (
        f"local {f_tonum},{f_char},{f_math_floor}=tonumber,string.char,math.floor;"
        f"local {v_data}={{{payload_array}}};"
        f"local {v_idx}=1;"
        f"local {v_seed}={generate_math_seed(initial_seed)};"
    )
    
    # LA MAGIA: Reader Function para `load`
    # Esto lee y descifra BYTE POR BYTE directamente hacia el compilador de C.
    # NUNCA se usa table.concat, el string original nunca existe en memoria.
    reader_func = (
        f"local function {v_reader}() "
        f"if {v_idx}>#{v_data} then return nil end;"
        # OPAQUE PREDICATE: math.sin(x) * math.cos(x) NUNCA es > 1 (Límite matemático real)
        f"if (math.sin({v_idx})*math.cos({v_idx}))>1 then return {f_char}(0) end;"
        # LCG Dinámico con parámetros únicos generados en Python
        f"{v_seed}=({v_seed}*{lcg.a}+{lcg.c})%4294967296;"
        f"local m={f_tonum}({v_data}[{v_idx}],16);"
        f"local sh={v_seed}%256;"
        f"local dec=(m-sh-(({v_idx}-1)%50))%256;"
        f"if dec<0 then dec=dec+256 end;"
        f"{v_idx}={v_idx}+1;"
        f"return {f_char}(dec);"
        f"end;"
    )
    
    # Ejecución y Anti-Debug Básico
    run_logic = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        # Intentar detectar si alguien está haciendo stepping con un debugger
        f"if debug and debug.getinfo then "
        f"local info=debug.getinfo(1,'l'); if info and info.currentline~=nil and info.currentline<0 then return end;"
        f"end;"
        # Ejecutar usando la función lectora
        f"local {v_exec}={v_env}[{f_char}(108,111,97,100)];"
        f"if not {v_exec} then {v_exec}={v_env}[{f_char}(108,111,97,100,115,116,114,105,110,103)] end;"
        # Si 'load' soporta iteradores (Lua 5.1+), usamos el lector directo. Si no, fallback de seguridad.
        f"local f,e={v_exec}({v_reader});" 
        f"if type(f)=='function' then return f(...) else error(tostring(e)) end;"
    )
    
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
            mode_used=f"Polymorphic Engine v4 ({min(layers_to_apply, 10)}-Layers)",
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
