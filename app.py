# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Anti-Moonsec / One-Line Hexadecimal Virtualization
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
    description="Anti-Moonsec One-Line Protection",
    version="14.1.0"
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

# ================================================
# SISTEMA ANTI-SUEÑO (KEEP-ALIVE)
# ================================================
def ping_self():
    """Mantiene el servidor activo haciendo ping cada 10 minutos"""
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

# ================================================
# MOTOR DE OFUSCACIÓN: HEX-ENGINE (UNA SOLA LÍNEA)
# ================================================

def generate_illusion_var(length=None):
    if length is None: length = random.randint(12, 20)
    return "_" + "".join(random.choices(["O", "0", "I", "l", "_"], k=length))

def math_obf(n: int) -> str:
    if random.choice([True, False]):
        a = random.randint(50, 999)
        b = a - n
        return f"({a}-{b})" if b >= 0 else f"({a}+{abs(b)})"
    else:
        a = random.randint(2, 5)
        b = n * a
        return f"({b}/{a})"

def obfuscate_single_layer(code: str) -> str:
    """
    Capa de virtualización usando Hexadecimal para evitar la explosión de caracteres.
    Se garantiza que todo retorne en UNA sola línea continua.
    """
    start_key = random.randint(20, 200)
    step_key = random.randint(11, 77)
    
    curr_key = start_key
    hex_str = ""
    
    # Encriptación Byte-a-Hexadecimal (Evita usar "\ddd" y previene errores en multicapas)
    for byte in code.encode('utf-8'):
        curr_key = (curr_key + step_key) % 256
        cipher = (byte + curr_key) % 256
        hex_str += f"{cipher:02x}"

    # Nombres de variables incomprensibles
    v_data = generate_illusion_var()
    v_out = generate_illusion_var()
    v_key = generate_illusion_var()
    v_state = generate_illusion_var()
    v_idx = generate_illusion_var()
    
    # Referencias nativas
    f_sub = generate_illusion_var()
    f_char = generate_illusion_var()
    f_insert = generate_illusion_var()
    f_concat = generate_illusion_var()
    f_tonum = generate_illusion_var()
    f_load = generate_illusion_var()
    
    # Lógica Anti-Moonsec
    m_fake_table = generate_illusion_var()
    v_hex = generate_illusion_var()
    v_b = generate_illusion_var()
    v_dec = generate_illusion_var()

    # SETUP (Todo comprimido)
    setup_code = (
        f"local {f_sub},{f_char},{f_insert},{f_concat},{f_tonum}=string.sub,string.char,table.insert,table.concat,tonumber;"
        f"local {f_load}=loadstring or load;"
        f"local {v_data}=\"{hex_str}\";"
        f"local {v_out}={{}};"
        f"local {v_key}={math_obf(start_key)};"
        f"local {v_state}={math_obf(1)};"
        f"local {v_idx}={math_obf(1)};"
    )

    # Lógica basura y predicados opacos para romper Decompiladores
    anti_moonsec_code = (
        f"local {m_fake_table}=setmetatable({{}},{{__index=function()return {v_key} end}});"
        f"if not {f_sub} then {v_key}={m_fake_table}[1]+{math_obf(999)} end;"
    )

    # Máquina de estados (State Machine) unida sin saltos de línea
    loop_code = (
        f"while {v_state}~={math_obf(0)} do "
        f"if {v_state}=={math_obf(1)} then "
        f"if {v_idx}>#{v_data} then {v_state}={math_obf(0)} else {v_state}={math_obf(2)} end;"
        f"elseif {v_state}=={math_obf(2)} then "
        f"{v_key}=({v_key}+{math_obf(step_key)})%{math_obf(256)};"
        f"local {v_hex}={f_sub}({v_data},{v_idx},{v_idx}+{math_obf(1)});"
        f"local {v_b}={f_tonum}({v_hex},{math_obf(16)});"
        f"local {v_dec}=({v_b}-{v_key})%{math_obf(256)};"
        f"{f_insert}({v_out},{f_char}({v_dec}));"
        f"{v_idx}={v_idx}+{math_obf(2)};"
        f"{v_state}={math_obf(1)};"
        f"end "
        f"end;"
    )

    # Ejecución blindada
    run_code = (
        f"local exec,err={f_load}({f_concat}({v_out}));"
        f"if type(exec)=='function' then return exec(...) else return err end;"
    )

    # Retorna absolutamente TODO en una sola línea continua
    return f"return(function(...) {setup_code}{anti_moonsec_code}{loop_code}{run_code} end)(...);"

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    actual_layers = max(1, min(requested_layers, 10))
    
    current_code = code
    # Envuelve la cadena en N capas en una sola línea
    for _ in range(actual_layers):
        current_code = obfuscate_single_layer(current_code)
        
    # BANNER CON LINKS + 2 LÍNEAS VACÍAS
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
                                       .\l    u$Yic]  `>           >#$@B\                           
                                     ;L~    -%$$$$U;|+          'zB$@pi                             
                                   ^aj    |8@$$$$$B]         .J%$@*i                                
                                 `a$f':(B$$$$$$$@c       '+a@B*r.                                   
                                c$$$$$$$@Bz>/$$k"     ~cXt-^                                        
                              ~%$@$$$$B/'  IB%l                                                     
                             w$$$$@BJ'    _%\                                                       
                           ~B$$$@a<      Un.                                                        
                         'a$$$@\       :p.                                                          
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
            return ObfuscateResponse(success=False, error="El código original excede el límite permitido")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        obfuscated = obfuscate_code(request.code, request.mode, layers_to_apply)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used=f"Single-Line Core ({min(layers_to_apply, 10)} Layers)",
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
