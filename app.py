# ================================================
#   SPACE OBFUSCATOR - Backend Server (One-Line VM)
#   Servidor FastAPI (Anti-AI & Single-Line Output)
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
    description="Anti-AI Lua Protection Service - One Line Edition",
    version="11.5.0"
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

def generate_illusion_var(length=8):
    # Genera nombres difíciles de distinguir visualmente
    return "_" + "".join(random.choices("O0I1", k=length))

def compile_to_single_line_vm(source_code: str) -> str:
    """
    Cifra el código fuente completo como una secuencia de bytes protegida,
    generando un entorno de ejecución dinámica en memoria (RAM) optimizado
    para ejecutarse estrictamente en UNA SOLA LÍNEA de código.
    """
    # Generar una clave de cifrado aleatoria
    key_shift = random.randint(10, 80)
    
    # Convertir todo el script original del usuario en un array de bytes cifrados
    encrypted_bytes = [(ord(char) + key_shift) % 256 for char in source_code]
    bytes_string = ",".join(map(str, encrypted_bytes))
    
    # Generar identificadores aleatorios para los componentes del intérprete
    v_bytecode = generate_illusion_var()
    v_result = generate_illusion_var()
    v_char_code = generate_illusion_var()
    v_loader = generate_illusion_var()
    v_env = generate_illusion_var()
    
    # Construcción de las partes del decodificador en memoria
    # Usamos sintaxis compacta de Lua que permite omitir saltos de línea
    step_1_init = f"local {v_bytecode}={{ {bytes_string} }} "
    step_2_env = f"local {v_env}=getfenv and getfenv() or _ENV "
    step_3_decode = f"local {v_result}='' for i=1,#{v_bytecode} do {v_result}={v_result}..string.char(({v_bytecode}[i]-{key_shift})%256) end "
    step_4_execute = f"local {v_loader}=loadstring or load if {v_loader} then {v_loader}({v_result})() end"
    
    # Combinar todas las instrucciones separadas únicamente por espacios o estructuras válidas
    full_vm_logic = f"do {step_1_init}{step_2_env}{step_3_decode}{step_4_execute} end"
    
    return full_vm_logic

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    # Generar la estructura limpia en una sola línea
    single_line_code = compile_to_single_line_vm(code)
    
    # Banner opcional en una sola línea usando comentarios de bloque de Lua
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
]]--\n"""
    
    return f"{banner}{single_line_code}"

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
            mode_used="Anti-AI Dynamic One-Line VM",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return ObfuscateResponse(success=False, error=f"Error inesperado: {str(e)}")

@app.get("/")
async def root():
    return {"status": "online", "engine": "OneLineVM"}

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
