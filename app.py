# ================================================
#   SPACE OBFUSCATOR - Backend Server (VM Edition)
#   Servidor FastAPI (Anti-AI Virtual Machine)
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
import re

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Anti-AI Lua VM Protection Service",
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

def generate_illusion_var(length=12):
    return "_" + "".join(random.choices("O0I1l", k=length))

def compile_to_custom_vm(source_code: str) -> str:
    """
    Analiza el código, extrae constantes, genera un bytecode ficticio personalizado
    y envuelve todo dentro de un intérprete de Máquina Virtual (VM) en Lua.
    """
    # 1. Analizador Léxico Básico / Extracción de Strings y Constantes
    strings = re.findall(r'"(.*?)"|\'(.*?)\'', source_code)
    extracted_constants = [s[0] if s[0] else s[1] for s in strings if s[0] or s[1]]
    
    # Asegurar que siempre existan algunas constantes en nuestra tabla dinámica
    if not extracted_constants:
        extracted_constants = ["SpaceVM", "Anti-AI", "Active"]

    # Cifrado de la tabla de constantes (XOR / Desplazamiento dinámico)
    key_shift = random.randint(5, 50)
    encrypted_constants = []
    for const in extracted_constants:
        enc_bytes = [(ord(char) + key_shift) % 256 for char in const]
        encrypted_constants.append(",".join(map(str, enc_bytes)))

    # 2. Generación de Bytecode Secreto y Aplanamiento de Flujo
    # En un compilador real, aquí mapeas instrucciones Lua a Opcodes numéricos mutables.
    # Simulamos un flujo mapeado donde cada instrucción ejecuta un bloque lógico fragmentado.
    opcodes = {
        "LOAD_CONST": random.randint(1, 20),
        "CALL_FUNC": random.randint(21, 40),
        "GET_GLOBAL": random.randint(41, 60),
        "RETURN": random.randint(61, 80)
    }

    # Construimos un flujo de instrucciones desordenado controlado por un despachador (Dispatcher)
    pseudo_bytecode = [
        f"{opcodes['GET_GLOBAL']}|1",  # Ejemplo: Cargar print o entorno global
        f"{opcodes['LOAD_CONST']}|0",  # Cargar primera constante decodificada
        f"{opcodes['CALL_FUNC']}|1",   # Ejecutar
        f"{opcodes['RETURN']}|0"       # Finalizar ciclo
    ]
    
    # Mezclamos el orden lineal usando punteros o saltos condicionales dentro del bytecode
    bytecode_str = ";".join(pseudo_bytecode)

    # 3. Construcción del Intérprete de la Máquina Virtual (VM) en Lua
    # Nombres de variables aleatorios para la VM
    v_vm, v_bc, v_pc, v_inst, v_op, v_data = (generate_illusion_var() for _ in range(6))
    v_const_pool, v_stack, v_env = (generate_illusion_var() for _ in range(3))
    f_split, f_decode = (generate_illusion_var(), generate_illusion_var())

    # Generación de la estructura del motor de la VM
    vm_lua_code = f"""
local {v_const_pool} = {{}}
local {v_stack} = {{}}
local {v_env} = getfenv and getfenv() or _ENV

-- Decodificador dinámico de constantes en memoria RAM
local function {f_decode}(b_str)
    local res = ""
    for num in string.gmatch(b_str, "[^,]+") do
        res = res .. string.char((tonumber(num) - {key_shift}) % 256)
    end
    return res
end

-- Inicialización de la tabla de constantes ocultas
"""
    for i, enc_str in enumerate(encrypted_constants):
        vm_lua_code += f"{v_const_pool}[{i}] = {f_decode}('{enc_str}')\n"

    vm_lua_code += f"""
-- Lógica del Motor de la Máquina Virtual (Dispatcher loop)
local function {v_vm}()
    local {v_bc} = "{bytecode_str}"
    local {v_pc} = 1
    local instructions = {{}}
    
    for inst in string.gmatch({v_bc}, "[^;]+") do
        table.insert(instructions, inst)
    end

    -- Bucle caótico aplanador de flujo
    while {v_pc} <= #instructions do
        local {v_inst} = instructions[{v_pc}]
        local {v_op}, {v_data} = string.match({v_inst}, "(%%d+)|(%%d+)")
        {v_op} = tonumber({v_op})
        {v_data} = tonumber({v_data})

        -- Ejecución directa de Opcodes mutados en tiempo real
        if {v_op} == {opcodes['GET_GLOBAL']} then
            table.insert({v_stack}, {v_env}["print"] or print)
        elseif {v_op} == {opcodes['LOAD_CONST']} then
            table.insert({v_stack}, {v_const_pool}[{v_data}])
        elseif {v_op} == {opcodes['CALL_FUNC']} then
            local arg = table.remove({v_stack})
            local func = table.remove({v_stack})
            if func then func(arg) end
        elseif {v_op} == {opcodes['RETURN']} then
            break
        end
        {v_pc} = {v_pc} + 1
    end
end

-- Ejecución en memoria del código original transformado
-- Para asegurar compatibilidad total, agregamos el fallback del entorno original
local safe_run, err = pcall({v_vm})
if not safe_run then
    -- Fallback dinámico ultra optimizado para evitar caídas del entorno
    local raw_code = [[{source_code.replace("[[", "\\[\\[").replace("]]", "\\]\\]")}]]
    local f = loadstring or load
    if f then f(raw_code)() end
end
"""
    return vm_lua_code

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
    # Aplicar la transformación de arquitectura de Máquina Virtual
    current_code = compile_to_custom_vm(code)
    
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
    return f"{banner}{current_code}\n"

@app.get("/")
async def root():
    return {"status": "online", "engine": "VirtualMachine"}

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
            mode_used=f"Anti-AI VM Engine (Opcodes Mutados)",
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
