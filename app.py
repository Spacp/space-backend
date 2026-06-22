# ================================================
#   SPACE OBFUSCATOR - Backend Server
#   Servidor FastAPI (Anti-AI Metatable Virtualization)
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
    version="10.0.0"
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
    mode: str = "medium"
    layers: Optional[int] = 1

class ObfuscateResponse(BaseModel):
    success: bool
    obfuscated_code: Optional[str] = None
    error: Optional[str] = None
    original_size: int = 0
    obfuscated_size: int = 0
    mode_used: str = ""
    timestamp: str = ""

def generate_illusion_var(length=14):
    """Genera nombres extremadamente extensos, confusos y repetitivos para saturar el contexto de la IA"""
    chars = "O0I1"
    return "_" + "".join(random.choice(chars) for _ in range(length))

def generate_anti_ai_junk() -> str:
    """
    Genera bloques controlados de código basura con sombreado de variables.
    Mantiene un balance óptimo entre peso final del archivo y alta confusión para LLMs.
    """
    junk = ""
    # Genera de 1 a 2 estructuras ficticias para evitar sobrecargar la memoria de Lua
    for _ in range(random.randint(1, 2)):
        v1 = generate_illusion_var(12)
        v2 = generate_illusion_var(12)
        v3 = generate_illusion_var(14)
        
        junk += (
            f"local {v1} = {random.randint(100, 9999)}; "
            f"local {v2} = function({v3}) "
            f"  local {v1} = {v3} and {random.randint(10, 50)}; "
            f"  for {generate_illusion_var(6)} = 1, {random.randint(3, 8)} do "
            f"    {v1} = ({v1} or 0) + {random.randint(1, 5)}; "
            f"  end "
            f"  return {v1}; "
            f"end; "
            f"if {v2}({v1}) == -99999 then "
            f"  local {v3} = setmetatable({{}}, {{__index = function(t,k) return k end}}); "
            f"  {v1} = {v3}[{random.randint(1, 100)}]; "
            f"end; "
        )
    return junk

def obfuscate_single_layer(code: str) -> str:
    """
    Aplica una capa de ofuscación utilizando virtualización de lectura mediante 
    metatablas interconectadas y operaciones criptográficas dinámicas.
    """
    base_key = random.randint(20, 180)
    multiplier = random.randint(3, 9)
    
    # Cifrado en flujo encadenado
    encoded_bytes = []
    last_val = base_key
    for byte in code.encode('utf-8'):
        cipher_byte = (byte + last_val + multiplier) % 256
        encoded_bytes.append(cipher_byte)
        last_val = cipher_byte
        
    encoded_hex = "".join(f"{b:02x}" for b in encoded_bytes)
    chunk_size = 3000 
    chunks = [encoded_hex[i:i+chunk_size] for i in range(0, len(encoded_hex), chunk_size)]
    super_string = ' .. '.join(f'"{c}"' for c in chunks)
    
    # Identificadores altamente confusos
    v_hex = generate_illusion_var()
    v_proxy = generate_illusion_var()
    v_res = generate_illusion_var()  # Corregido a minúsculas completo
    v_state = generate_illusion_var()
    v_idx = generate_illusion_var()
    v_last = generate_illusion_var()
    
    f_sub = generate_illusion_var()
    f_tonum = generate_illusion_var()
    f_char = generate_illusion_var()
    f_insert = generate_illusion_var()
    f_concat = generate_illusion_var()
    f_load = generate_illusion_var()
    
    # Inyección balanceada de código basura
    junk_pre = generate_anti_ai_junk()
    junk_post = generate_anti_ai_junk()
    
    # Lógica con Metatabla Proxy
    setup_logic = (
        f"{junk_pre} "
        f"local {v_hex} = {super_string}; "
        f"local {f_sub},{f_tonum},{f_char},{f_insert},{f_concat},{f_load} = string.sub,tonumber,string.char,table.insert,table.concat,loadstring or load; "
        f"local {v_proxy} = setmetatable({{}}, {{ "
        f"  __index = function(t, k) "
        f"    local s_str = {f_sub}({v_hex}, k, k + 1); "
        f"    if s_str == \"\" then return nil end; "
        f"    return ({f_tonum}(s_str, 16) + k) % 256; "
        f"  end "
        f"}}); "
        f"local {v_res} = {{}}; "
        f"local {v_state} = 1; "
        f"local {v_idx} = 1; "
        f"local {v_last} = {base_key}; "
    )
    
    # Bucle de Control Desaplanado (Control Flow Flattening)
    loop_logic = (
        f"while {v_state} ~= 0 do "
            f"if {v_state} == 1 then "
                f"if {v_idx} > #{v_hex} then {v_state} = 4 else {v_state} = 2 end; "
            f"elseif {v_state} == 2 then "
                f"local m_val = {v_proxy}[{v_idx}]; "
                f"if not m_val then {v_state} = 4; else "
                f"  local c_byte = (m_val - {v_idx}) % 256; "
                f"  local dec_b = (c_byte - {v_last} - {multiplier}) % 256; "
                f"  {f_insert}({v_res}, {f_char}(dec_b)); "
                f"  {v_last} = c_byte; {v_state} = 3; "
                f"end; "
            f"elseif {v_state} == 3 then "
                f"{v_idx} = {v_idx} + 2; {v_state} = 1; "
            f"elseif {v_state} == 4 then "
                f"{v_state} = 0; "
            f"end "
        f"end; "
        f"{junk_post} "
    )
    
    run_logic = (
        f"local f, e = {f_load}({f_concat}({v_res})); "
        f"if not f then error(tostring(e)) end; "
        f"return f(...); "
    )
    
    return f"return(function(...) {setup_logic}{loop_logic}{run_logic} end)(...)"

def obfuscate_code(code: str, mode: str, layers: int) -> str:
    """
    Fuerza el sistema a procesar el script exactamente 5 veces fijas.
    Garantiza la máxima protección matemática balanceando la carga final del script.
    """
    actual_layers = 5
    
    current_code = code
    for _ in range(actual_layers):
        current_code = obfuscate_single_layer(current_code)
        
    banner = """--[[


                                                                  <\'         -n:                   
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
                
                                                                                               
                                            https://discord.gg/7dt2A6DJZA
                                            https://space.spacecp.workers.dev
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
        
        # Incrementado a 10MB preventivo por el crecimiento exponencial de las 5 capas
        max_size = 10 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="El código original excede el límite permitido")
        
        obfuscated = obfuscate_code(request.code, request.mode, request.layers)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used="High Protection (5-Layers + Anti-AI)",
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
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)