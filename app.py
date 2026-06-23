# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Polimorphic Encryption (CTF Hardened)
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
    version="12.0.0"
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

# SISTEMA ANTI-SUEÑO
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

def generate_dynamic_key(base_key: int) -> str:
    """Oculta la llave matemática detrás de propiedades nativas del entorno de Lua"""
    choice = random.randint(1, 3)
    if choice == 1:
        # type(math.pi) devuelve "number", su longitud es 6
        offset = base_key - 6
        return f"({offset}+#type(math.pi))"
    elif choice == 2:
        # type(tostring) devuelve "function", su longitud es 8
        offset = base_key - 8
        return f"({offset}+#type(tostring))"
    else:
        # type({}) devuelve "table", su longitud es 5
        offset = base_key - 5
        return f"({offset}+#type({{}}))"

def obfuscate_single_layer(code: str) -> str:
    """
    Polimorfismo Multicapa:
    - 3 Algoritmos entrelazados (Suma, XOR/Suma Inversa, Not lógico).
    - Array disperso en lugar de String Hex Continuo.
    - Máquina de Estados Caótica.
    - Opaque Predicates basados en el entorno Lua.
    """
    key_base = random.randint(30, 200)
    
    encoded_blocks = []
    
    # POLIMORFISMO DE ENCRIPTACIÓN EN PYTHON (Múltiples algoritmos)
    for i, byte in enumerate(code.encode('utf-8')):
        path = i % 3
        if path == 0:
            c = (byte + key_base) % 256
        elif path == 1:
            c = (255 - byte)
        else:
            # Emulamos un XOR básico pero seguro para Lua 5.1 (Suma con offset variable)
            c = (byte + (key_base % 50)) % 256
        
        encoded_blocks.append(f'"{c:02x}"')
    
    # FRAGMENTACIÓN DEL PAYLOAD: El array de Hex se divide aleatoriamente
    # No hay string continuo, es una tabla gigantesca de pares Hex.
    payload_array = ",".join(encoded_blocks)
    
    # Nombres de variables oscurecidas
    v_data, v_out, v_key, v_state, v_idx = (generate_illusion_var() for _ in range(5))
    f_tonum, f_char, f_insert, f_concat, f_type = (generate_illusion_var() for _ in range(5))
    v_env, v_exec = (generate_illusion_var() for _ in range(2))
    
    # Estados aleatorios para la Máquina CFF (Control Flow Flattening)
    S_INIT = random.randint(10, 30)
    S_CHECK = random.randint(40, 60)
    S_DECODE = random.randint(70, 90)
    S_APPEND = random.randint(100, 120)
    S_END = 0
    
    # SETUP - Array Fragmentado
    setup_code = (
        f"local {f_tonum},{f_char},{f_insert},{f_concat},{f_type}=tonumber,string.char,table.insert,table.concat,type;"
        f"local {v_data}={{{payload_array}}};"
        f"local {v_out}={{}};"
        f"local {v_state}={S_INIT};"
        f"local {v_idx}=1;"
        f"local {v_key}={generate_dynamic_key(key_base)};"
    )
    
    # OPAQUE PREDICATE CAÓTICO Y MÁQUINA DE ESTADOS COMPLEJA
    # Predicado opaco: #type(print) siempre es 8. Así que math.abs(8-8) == 0. (True 100%)
    loop_code = (
        f"while {v_state}~={S_END} do "
        f"if {v_state}=={S_INIT} then "
        f"if {v_idx}>#{v_data} then {v_state}={S_END} else {v_state}={S_CHECK} end;"
        f"elseif {v_state}=={S_CHECK} then "
        f"if math.abs(#{f_type}(print)-8)==0 then " # <-- OPAQUE PREDICATE INDETECTABLE
        f"{v_state}={S_DECODE};"
        f"else {v_state}={S_END} end;"              # <-- RAMA MUERTA
        f"elseif {v_state}=={S_DECODE} then "
        f"local h={v_data}[{v_idx}];"
        f"local m={f_tonum}(h,16);"
        f"local d;"
        f"local p=({v_idx}-1)%3;"
        f"if p==0 then d=(m-{v_key})%256;"          # <-- Algoritmo 1
        f"elseif p==1 then d=(255-m);"              # <-- Algoritmo 2
        f"else d=(m-({v_key}%50))%256 end;"         # <-- Algoritmo 3
        f"{f_insert}({v_out},{f_char}(d));"
        f"{v_idx}={v_idx}+1;"
        f"{v_state}={S_INIT};"
        f"end;"
        f"end;"
    )
    
    # ANTI-HOOK & EXECUTION INVISIBLE
    run_logic = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_exec}={v_env}[{f_char}(108,111,97,100)] or {v_env}[{f_char}(108,111,97,100,115,116,114,105,110,103)];"
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
            mode_used=f"CTF Grade ({min(layers_to_apply, 10)}-Layers + Polimorfismo)",
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
