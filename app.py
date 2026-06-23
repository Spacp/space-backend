# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Version 19.0.0: Environment-Locked & Anti-Tamper Engine
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
import base64

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Environment-Locked Lua Protection Service",
    version="19.0.0"
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

def generate_chaotic_var():
    # Evita patrones fijos como _O0I1l generando nombres alfanuméricos caóticos de longitud variable
    length = random.randint(7, 16)
    prefix = random.choice(["ctx", "slot", "stk", "reg", "var", "pt", "l"])
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    return f"_{prefix}_" + "".join(random.choices(chars, k=length))

class MultiStatePRNG:
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.m = 4294967296

    def next(self):
        self.s1 = (self.s1 * 1664525 + 1013904223) % self.m
        self.s2 = (self.s2 * 22695477 + 1) % self.m
        self.s3 = (self.s3 + self.s1) % self.m
        return (self.s1 + self.s2 + self.s3) % 256

def obfuscate_single_layer(code: str) -> str:
    """
    Motor v9 (Anti-Tamper & Environment Cryptolock):
    - Autopadding preventivo contra ataques de fuerza bruta.
    - Semillas dinámicas vinculadas a la integridad del Script.
    - Ocultación total de firmas nativas de Lua 5.1/Luau.
    """
    
    # 1. AUTO-PADDING (Previene criptoanálisis de payloads cortos)
    if len(code) < 600:
        padding_lines = []
        for _ in range(random.randint(25, 40)):
            v1 = generate_chaotic_var()
            v2 = generate_chaotic_var()
            padding_lines.append(f"local {v1} = function() return math.sin({random.randint(1,100)}) end; local {v2} = {v1}() and true or false;")
        code = "\n".join(padding_lines) + "\n" + code

    # 2. PROCESAMIENTO CRIPTOGRÁFICO DE SEMILLAS MÓVILES
    # Definimos desplazamientos secretos en lugar de semillas estáticas directas
    offset_1 = random.randint(200000, 800000)
    offset_2 = random.randint(100000, 900000)
    offset_3 = random.randint(300000, 700000)
    
    # Simulamos el valor base esperado del Checksum ambiental en ejecución (entorno estándar ~3000)
    assumed_base = 3015 
    s1_target = (assumed_base + offset_1) % 4294967296
    s2_target = (assumed_base ^ offset_2) % 4294967296
    s3_target = (assumed_base + offset_3) % 4294967296
    
    prng = MultiStatePRNG(s1_target, s2_target, s3_target)
    
    # Encriptación del Stream
    enc_bytes = bytearray()
    integrity_checksum = 0
    for byte in code.encode('utf-8'):
        sh = prng.next()
        c = (byte + sh) % 256
        enc_bytes.append(c)
        integrity_checksum = (integrity_checksum + c) % 65535
        
    # Agregamos la firma de integridad al final del payload binario
    enc_bytes.append(integrity_checksum // 256)
    enc_bytes.append(integrity_checksum % 256)
        
    b64_payload = base64.b64encode(enc_bytes).decode('utf-8')
    
    # 3. APALANAMIENTO POLIMÓRFICO DE PARÁMETROS
    params_real = ["string.byte", "string.char", "string.sub", "table.insert", "os.clock", "type", "pcall", "string.find", "math.floor", "string.gsub"]
    params_fake = [generate_chaotic_var() for _ in params_real]
    
    v_byte, v_char, v_sub, v_insert, v_clock, v_type, v_pcall, v_find, v_floor, v_gsub = params_fake

    # Asignación de variables de control
    v_data, v_b64, v_enc_bytes = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_s1, v_s2, v_s3 = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_dec_idx, v_t_start, v_t_last = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_reader, v_env, v_l, v_ok, v_res = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_src, v_shash, v_sum = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_check, v_calc_check = generate_chaotic_var(), generate_chaotic_var()

    # Ocultación de palabras clave críticas de entorno
    str_load = '"\\108\\111\\97\\100"'
    str_loadstring = '"\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103"'
    str_getfenv = 'string.char(103,101,116,102,101,110,118)'

    inner_code = (
        # RECONSTRUCCIÓN DINÁMICA DEL ENTORNO (Sin delatar Lua 5.1 explícitamente)
        f"local {v_env} = (_ENV or (function() local f = _G[{str_getfenv}]; if f then return f() else return _G end end)());"
        
        # CHECKSUM DE INTEGRIDAD DEL SCRIPT (Previene parches de analistas)
        f"local {v_src} = (debug and debug.getinfo) and debug.getinfo(1,'S').source or 'stealth';"
        f"local {v_shash} = 0; for i=1, #{v_src} do {v_shash} = ({v_shash} * 31 + {v_byte}({v_src}, i)) % 4294967296 end;"
        
        # ANALISIS DEL ENTORNO GLOBAL
        f"local {v_sum} = 0; for k, v in pairs({v_env}) do if {v_type}(v) == 'function' then {v_sum} = ({v_sum} + #{k}) % 5000 end end;"
        f"if {v_sum} == 0 then {v_sum} = {assumed_base} end;" # Fallback de estabilidad
        
        # DERIVACIÓN MATEMÁTICA DE SEMILLAS (No existen constantes en el código)
        f"local {v_s1} = ({v_sum} + {offset_1} + ({v_shash} % 1000)) % 4294967296;"
        f"local {v_s2} = (({v_sum} ~ {offset_2}) + ({v_shash} % 500)) % 4294967296;"
        f"local {v_s3} = ({v_sum} + {offset_3} - ({v_shash} % 2000)) % 4294967296;"
        
        # EXTRACCIÓN DEL STRING DE DATOS
        f"local {v_b64} = \"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\";"
        f"local {v_data} = [=[{b64_payload}]=];"
        f"{v_data} = {v_gsub}({v_data}, '[^%w%+/=]', '');"
        
        # DECODIFICADOR INTERNO DE ALTA VELOCIDAD
        f"local {v_enc_bytes} = {{}};"
        f"for i=1, #{v_data}, 4 do "
        f"local n = ({v_find}({v_b64}, {v_sub}({v_data},i,i), 1, true)-1)*262144+"
        f"({v_find}({v_b64}, {v_sub}({v_data},i+1,i+1), 1, true)-1)*4096+"
        f"({v_sub}({v_data},i+2,i+2)=='=' and 0 or ({v_find}({v_b64}, {v_sub}({v_data},i+2,i+2), 1, true)-1)*64)+"
        f"({v_sub}({v_data},i+3,i+3)=='=' and 0 or ({v_find}({v_b64}, {v_sub}({v_data},i+3,i+3), 1, true)-1));"
        f"{v_insert}({v_enc_bytes}, {v_floor}(n/65536)%256);"
        f"if {v_sub}({v_data},i+2,i+2) ~= '=' then {v_insert}({v_enc_bytes}, {v_floor}(n/256)%256) end;"
        f"if {v_sub}({v_data},i+3,i+3) ~= '=' then {v_insert}({v_enc_bytes}, n%256) end;"
        f"end;"
        
        # VERIFICACIÓN DE INTEGRIDAD DEL PAYLOAD (Punto 3)
        f"if #{v_enc_bytes} < 3 then return nil end;"
        f"local {v_check} = {v_enc_bytes}[#{v_enc_bytes}-1]*256 + {v_enc_bytes}[#{v_enc_bytes}];"
        f"local {v_calc_check} = 0; for i=1, #{v_enc_bytes}-2 do {v_calc_check} = ({v_calc_check} + {v_enc_bytes}[i]) % 65535 end;"
        f"if {v_check} ~= {v_calc_check} then {v_s3} = {v_s3} + 999999 end;" # Envenena las llaves si hay manipulación
        
        # CONFIGURACIÓN DEL ITERADOR Y ANTI-TIMING INCREMENTAL
        f"local {v_dec_idx} = 1;"
        f"local {v_t_start} = {v_clock}();"
        f"local {v_t_last} = {v_t_start};"
        
        f"local function {v_reader}() "
        f"if {v_dec_idx} > (#{v_enc_bytes}-2) then return nil end;"
        
        # Anti-Timing Check Distribuido por Ciclo (Detecta desincronizaciones de debuggers)
        f"local now = {v_clock}();"
        f"local delta = now - {v_t_last};"
        f"if delta > 0.3 or (now - {v_t_start}) > 4.0 then {v_s1} = ({v_s1} + 7) % 4294967296 end;"
        f"{v_t_last} = now;"
        
        # EVOLUCIÓN DE ESTADOS DEL PRNG MULTI-ESTADO
        f"{v_s1} = ({v_s1} * 1664525 + 1013904223) % 4294967296;"
        f"{v_s2} = ({v_s2} * 22695477 + 1) % 4294967296;"
        f"{v_s3} = ({v_s3} + {v_s1}) % 4294967296;"
        f"local sh = ({v_s1} + {v_s2} + {v_s3}) % 256;"
        
        f"local m = {v_enc_bytes}[{v_dec_idx}];"
        f"local dec = (m - sh) % 256;"
        f"if dec < 0 then dec = dec + 256 end;"
        f"{v_dec_idx} = {v_dec_idx} + 1;"
        f"return {v_char}(dec);"
        f"end;"
        
        # EJECUCIÓN DINÁMICA ULTRA SEGURA
        f"local {v_l} = {v_env}[{str_load}] or {v_env}[{str_loadstring}];"
        f"local {v_ok}, {v_res} = {v_pcall}({v_l}, {v_reader});"
        f"if {v_ok} and {v_type}({v_res}) == 'function' then return {v_res}(...) end;"
    )

    # Empaquetado final con Parameter Flattening
    params_fake_str = ",".join(params_fake)
    params_real_str = ",".join(params_real)
    
    wrapper = f"return (function({params_fake_str})\n{inner_code}\nend)({params_real_str})"
    return wrapper

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
            return ObfuscateResponse(success=False, error="El código excede el límite permitido")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        obfuscated = obfuscate_code(request.code, request.mode, layers_to_apply)
        
        return ObfuscateResponse(
            success=True,
            obfuscated_code=obfuscated,
            original_size=len(request.code),
            obfuscated_size=len(obfuscated),
            mode_used=f"Crypto VM Engine v19 ({min(layers_to_apply, 10)}-Layers)",
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
