# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Anti-Moonsec & Anti-AI Lightweight Virtualization (No-Lag Edition)
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
    description="Anti-Moonsec & Anti-AI Protection with Editor Lag Fix",
    version="12.1.0"
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
    """Mantiene el servidor web activo haciendo un ping interno cada 10 minutos"""
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
# MOTOR DE OFUSCACIÓN: LIGERO, ANTI-MOONSEC Y SIN LAG
# ================================================

def generate_illusion_var(length=None):
    if length is None: length = random.randint(10, 15)
    return "_" + "".join(random.choices(["O", "0", "I", "l", "_"], k=length))

def math_obf(n: int) -> str:
    if random.choice([True, False]):
        a = random.randint(50, 999)
        b = a - n
        return f"({a} - {b})" if b >= 0 else f"({a} + {abs(b)})"
    else:
        a = random.randint(2, 5)
        b = n * a
        return f"({b} / {a})"

def obfuscate_single_layer(code: str) -> str:
    """
    Capa Ultra-Ligera con Fix de Rendimiento de Editor:
    - Fragmenta la cadena de bytes en múltiples líneas cortas (Evita congelamiento del editor).
    - Mantiene el motor CFF Anti-Moonsec y Anti-AI intacto.
    """
    start_key = random.randint(20, 200)
    step_key = random.randint(11, 77)
    
    curr_key = start_key
    encoded_str = ""
    
    # Encriptación Byte-a-Byte
    for byte in code.encode('utf-8'):
        curr_key = (curr_key + step_key) % 256
        cipher = (byte + curr_key) % 256
        encoded_str += f"\\{cipher:03d}"

    # ========================================================
    # SOLUCIÓN CRÍTICA: FRAGMENTACIÓN PARA EVITAR LAG EN EL EDITOR
    # Dividimos la cadena masiva cada 120 caracteres y la unimos con ' ..\n"'
    # ========================================================
    line_length = 120
    chunks = [encoded_str[i:i+line_length] for i in range(0, len(encoded_str), line_length)]
    lua_string_block = '" ..\n"'.join(chunks)

    # Variables ofuscadas
    v_data = generate_illusion_var()
    v_out = generate_illusion_var()
    v_key = generate_illusion_var()
    v_state = generate_illusion_var()
    v_idx = generate_illusion_var()
    
    # Funciones nativas ensombrecidas
    f_byte = generate_illusion_var()
    f_char = generate_illusion_var()
    f_insert = generate_illusion_var()
    f_concat = generate_illusion_var()
    f_load = generate_illusion_var()
    
    # Control de predicado opaco (Anti-Decompiler)
    m_fake_table = generate_illusion_var()
    v_b = generate_illusion_var()
    v_dec = generate_illusion_var()

    # SETUP (Aquí se inyecta el bloque multi-línea de forma segura)
    setup_code = (
        f"local {f_byte}, {f_char}, {f_insert}, {f_concat} = string.byte, string.char, table.insert, table.concat;\n"
        f"local {f_load} = loadstring or load;\n"
        f"local {v_data} = \"{lua_string_block}\";\n"
        f"local {v_out} = {{}};\n"
        f"local {v_key} = {math_obf(start_key)};\n"
        f"local {v_state} = {math_obf(1)};\n"
        f"local {v_idx} = {math_obf(1)};\n"
    )

    # ANTI-MOONSEC LÓGICA FALSA
    anti_moonsec_code = (
        f"local {m_fake_table} = setmetatable({{}}, {{__index = function() return {v_key} end}});\n"
        f"if not {f_byte} then {v_key} = {m_fake_table}[1] + {math_obf(999)} end;\n"
    )

    # MOTOR MÁQUINA DE ESTADOS (CFF)
    loop_code = (
        f"while {v_state} ~= {math_obf(0)} do\n"
        f"  if {v_state} == {math_obf(1)} then\n"
        f"      if {v_idx} > #{v_data} then {v_state} = {math_obf(0)} else {v_state} = {math_obf(2)} end;\n"
        f"  elseif {v_state} == {math_obf(2)} then\n"
        f"      {v_key} = ({v_key} + {math_obf(step_key)}) % {math_obf(256)};\n"
        f"      local {v_b} = {f_byte}({v_data}, {v_idx}, {v_idx});\n"
        f"      local {v_dec} = ({v_b} - {v_key}) % {math_obf(256)};\n"
        f"      {f_insert}({v_out}, {f_char}({v_dec}));\n"
        f"      {v_idx} = {v_idx} + {math_obf(1)};\n"
        f"      {v_state} = {math_obf(1)};\n"
        f"  end\n"
        f"end;\n"
    )

    # EJECUCIÓN DINÁMICA
    run_code = (
        f"local exec = {f_load}({f_concat}({v_out}));\n"
        f"if type(exec) == 'function' then return exec(...) end;\n"
    )

    return f"return(function(...)\n{setup_code}{anti_moonsec_code}{loop_code}{run_code}\nend)(...)"

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
            mode_used=f"Optimized Core ({min(layers_to_apply, 10)}-Layers + Anti-Lag)",
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
