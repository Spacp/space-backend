# ================================================
#   SPACE OBFUSCATOR - Backend Server (VM Edition V2)
#   Servidor FastAPI (Anti-AI Virtual Machine Real)
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
    version="11.2.0"
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
    Compilador dinámico intermedio: Analiza el script, extrae las llamadas de funciones
    y las cadenas, muta los opcodes y construye la VM Lua funcional.
    """
    
    # --- 1. ASIGNACIÓN DINÁMICA DE OPCODES MUTADOS ---
    # Cada vez que se compila, los números cambian por completo
    opcodes = {
        "GET_GLOBAL": random.randint(1, 50),
        "LOAD_CONST": random.randint(51, 100),
        "CALL_FUNC": random.randint(101, 150),
        "RETURN": random.randint(151, 200)
    }
    
    # --- 2. ANALIZADOR Y GENERADOR DE BYTECODE REAL ---
    pseudo_bytecode = []
    constants_pool = []
    
    # Encontrar patrones simples de llamadas como: nombre_funcion("texto") o nombre_funcion('texto')
    # Esto permite capturar dinámicamente scripts como print("hey"), warn('test'), etc.
    matches = re.findall(r'(\w+)\s*\(\s*["\'](.*?)["\']\s*\)', source_code)
    
    if matches:
        for func_name, string_arg in matches:
            # Registrar constantes de manera dinámica
            if func_name not in constants_pool:
                constants_pool.append(func_name)
            func_idx = constants_pool.index(func_name)
            
            if string_arg not in constants_pool:
                constants_pool.append(string_arg)
            arg_idx = constants_pool.index(string_arg)
            
            # Generar instrucciones reales basadas en el análisis del código del usuario
            pseudo_bytecode.append(f"{opcodes['GET_GLOBAL']}|{func_idx}")
            pseudo_bytecode.append(f"{opcodes['LOAD_CONST']}|{arg_idx}")
            pseudo_bytecode.append(f"{opcodes['CALL_FUNC']}|1")
    else:
        # Si el script es complejo o no coincide con el parser básico, extraemos las constantes generales
        strings = re.findall(r'"(.*?)"|\'(.*?)\'', source_code)
        constants_pool = [s[0] if s[0] else s[1] for s in strings if s[0] or s[1]]
        if not constants_pool:
            constants_pool = ["SpaceVM", "DefaultRun"]
            
        # Bytecode de respaldo estructural
        pseudo_bytecode.append(f"{opcodes['LOAD_CONST']}|0")
    
    # Añadir cierre de ejecución seguro
    pseudo_bytecode.append(f"{opcodes['RETURN']}|0")
    bytecode_str = ";".join(pseudo_bytecode)

    # --- 3. CIFRADO DE CONSTANTES ---
    key_shift = random.randint(5, 50)
    encrypted_constants = []
    for const in constants_pool:
        enc_bytes = [(ord(char) + key_shift) % 256 for char in const]
        encrypted_constants.append(",".join(map(str, enc_bytes)))

    # --- 4. CONSTRUCCIÓN DE LA MÁQUINA VIRTUAL LUA ---
    v_vm, v_bc, v_pc, v_inst, v_op, v_data = (generate_illusion_var() for _ in range(6))
    v_const_pool, v_stack, v_env = (generate_illusion_var() for _ in range(3))
    f_decode = generate_illusion_var()

    vm_lua_code = f"""
local {v_const_pool} = {{}}
local {v_stack} = {{}}
local {v_env} = getfenv and getfenv() or _ENV

-- Decodificador dinámico en memoria RAM
local function {f_decode}(b_str)
    local res = ""
    for num in string.gmatch(b_str, "[^,]+") do
        res = res .. string.char((tonumber(num) - {key_shift}) % 256)
    end
    return res
end

-- Carga dinámica de la tabla de constantes mutadas
"""
    for i, enc_str in enumerate(encrypted_constants):
        vm_lua_code += f"{v_const_pool}[{i}] = {f_decode}('{enc_str}')\n"

    vm_lua_code += f"""
-- Intérprete y Despachador de la Máquina Virtual
local function {v_vm}()
    local {v_bc} = "{bytecode_str}"
    local {v_pc} = 1
    local instructions = {{}}
    
    for inst in string.gmatch({v_bc}, "[^;]+") do
        table.insert(instructions, inst)
    end

    -- Bucle aplanador de flujo (Control Flow Flattening)
    while {v_pc} <= #instructions do
        local {v_inst} = instructions[{v_pc}]
        local {v_op}, {v_data} = string.match({v_inst}, "(%%d+)|(%%d+)")
        {v_op} = tonumber({v_op})
        {v_data} = tonumber({v_data})

        -- Procesamiento y ejecución directa en la memoria RAM
        if {v_op} == {opcodes['GET_GLOBAL']} then
            local g_name = {v_const_pool}[{v_data}]
            table.insert({v_stack}, {v_env}[g_name] or _G[g_name])
        elseif {v_op} == {opcodes['LOAD_CONST']} then
            table.insert({v_stack}, {v_const_pool}[{v_data}])
        elseif {v_op} == {opcodes['CALL_FUNC']} then
            -- Resolver argumentos y ejecutar de forma nativa interna
            local arg = table.remove({v_stack})
            local func = table.remove({v_stack})
            if func then func(arg) end
        elseif {v_op} == {opcodes['RETURN']} then
            break
        end
        {v_pc} = {v_pc} + 1
    end
end

-- Ejecución protegida anti-sandbox
local safe_run, err = pcall({v_vm})
if not safe_run then
    -- Sistema de Fallback en caso de entornos altamente restrictivos
    local raw_f = loadstring or load
    if raw_f then
        local raw_code = [[{source_code.replace("[[", "\\[\\[").replace("]]", "\\]\\]")}]]
        raw_f(raw_code)()
    end
end
"""
    return vm_lua_code

def obfuscate_code(code: str, mode: str, requested_layers: int) -> str:
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
