# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Servidor FastAPI (Extreme Anti-AI Metatable Virtualization)
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
import asyncio
import urllib.request
import threading

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Anti-AI Lua Protection Service",
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

# ================================================
# TAREA EN SEGUNDO PLANO: EVITAR QUE EL SERVIDOR DUERMA
# ================================================
def ping_self():
    """Hace ping al propio servidor cada 10 minutos para evitar que servicios como Render lo suspendan"""
    while True:
        try:
            # Hace una petición rápida a su propia ruta de salud
            urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=5)
        except:
            pass
        import time
        time.sleep(600)  # Duerme por 10 minutos

@app.on_event("startup")
async def startup_event():
    # Inicia el hilo de auto-ping en segundo plano cuando el servidor arranca
    thread = threading.Thread(target=ping_self, daemon=True)
    thread.start()

# ================================================
# MOTORES DE OFUSCACIÓN ANTI-IA AVANZADOS
# ================================================

def generate_illusion_var(length=random.randint(18, 28)):
    """Genera nombres de variables visualmente confusos y largos"""
    return "_" + "".join(random.choices(["O", "0", "I", "l", "_"], k=length))

def math_obf(n: int) -> str:
    """Oculta números reales detrás de operaciones matemáticas aleatorias para confundir IAs"""
    if random.choice([True, False]):
        a = random.randint(100, 5000)
        b = a - n
        return f"({a} - {b})" if b >= 0 else f"({a} + {abs(b)})"
    else:
        a = random.randint(2, 10)
        b = n * a
        return f"({b} / {a})"

def generate_anti_ai_junk() -> str:
    """Genera bloques de código Lua funcional pero inútil para destruir el contexto de las IAs"""
    junk = ""
    for _ in range(random.randint(2, 4)):
        v1, v2, v3 = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
        
        # Mezcla pcalls, metatables infinitas y math aleatorio
        junk += (
            f"local {v1} = {math_obf(random.randint(10, 9999))}; "
            f"local {v2} = setmetatable({{{math_obf(1)}, {math_obf(2)}}}, {{__index = function(t, k) return k * {math_obf(3)} end}}); "
            f"pcall(function() "
            f"  for {v3} = {math_obf(1)}, {math_obf(random.randint(3, 7))} do "
            f"    {v1} = {v1} + {v2}[{v3}]; "
            f"  end "
            f"end); "
            f"if {v1} == {math_obf(-999999)} then return function() end end; "
        )
    return junk

def obfuscate_single_layer(code: str) -> str:
    """Capa de virtualización y encriptación basada en state-machines y math obfuscation"""
    base_key = random.randint(20, 180)
    multiplier = random.randint(3, 9)
    
    # Cifrado de bytes
    encoded_bytes = bytearray()
    last_val = base_key
    for byte in code.encode('utf-8'):
        cipher_byte = (byte + last_val + multiplier) % 256
        encoded_bytes.append(cipher_byte)
        last_val = cipher_byte
        
    encoded_hex = encoded_bytes.hex()
    
    # Fragmentación segura en tablas
    chunk_size = 2000 
    chunks = [encoded_hex[i:i+chunk_size] for i in range(0, len(encoded_hex), chunk_size)]
    table_elements = ", ".join(f'"{c}"' for c in chunks)
    
    # Variables fantasma
    v_hex, v_proxy, v_res, v_state, v_idx, v_last = (generate_illusion_var() for _ in range(6))
    f_sub, f_tonum, f_char, f_insert, f_concat, f_load = (generate_illusion_var() for _ in range(6))
    
    # Inyección de ruido Anti-IA antes y después
    junk_pre = generate_anti_ai_junk()
    junk_post = generate_anti_ai_junk()
    
    setup_logic = (
        f"{junk_pre} "
        f"local {f_sub},{f_tonum},{f_char},{f_insert},{f_concat},{f_load} = string.sub,tonumber,string.char,table.insert,table.concat,loadstring or load; "
        f"local {v_hex} = {f_concat}({{{table_elements}}}); "
        f"local {v_proxy} = setmetatable({{}}, {{ "
        f"  __index = function(t, k) "
        f"    local s_str = {f_sub}({v_hex}, k, k + {math_obf(1)}); "
        f"    if s_str == \"\" then return nil end; "
        f"    return ({f_tonum}(s_str, {math_obf(16)}) + k) % {math_obf(256)}; "
        f"  end "
        f"}}); "
        f"local {v_res} = {{}}; "
        f"local {v_state} = {math_obf(1)}; "
        f"local {v_idx} = {math_obf(1)}; "
        f"local {v_last} = {math_obf(base_key)}; "
    )
    
    loop_logic = (
        f"while {v_state} ~= {math_obf(0)} do "
            f"if {v_state} == {math_obf(1)} then "
                f"if {v_idx} > #{v_hex} then {v_state} = {math_obf(4)} else {v_state} = {math_obf(2)} end; "
            f"elseif {v_state} == {math_obf(2)} then "
                f"local m_val = {v_proxy}[{v_idx}]; "
                f"if not m_val then {v_state} = {math_obf(4)}; else "
                f"  local c_byte = (m_val - {v_idx}) % {math_obf(256)}; "
                f"  local dec_b = (c_byte - {v_last} - {math_obf(multiplier)}) % {math_obf(256)}; "
                f"  {f_insert}({v_res}, {f_char}(dec_b)); "
                f"  {v_last} = c_byte; {v_state} = {math_obf(3)}; "
                f"end; "
            f"elseif {v_state} == {math_obf(3)} then "
                f"{v_idx} = {v_idx} + {math_obf(2)}; {v_state} = {math_obf(1)}; "
            f"elseif {v_state} == {math_obf(4)} then "
                f"{v_state} = {math_obf(0)}; "
            f"end "
        f"end; "
        f"{junk_post} "
    )
    
    run_logic = (
        f"local f, e = {f_load}({f_concat}({v_res})); "
        f"if not f then pcall(function() error(tostring(e)) end) end; "
        f"return f(...); "
    )
    
    return f"return(function(...) {setup_logic}{loop_logic}{run_logic} end)(...)"

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
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
                
                                            ttps://space.spacecp.workers.dev/
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
        
        max_size = 10 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="El código original excede el límite permitido")
        
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
