# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Version 19.0.3: Environment-Locked Engine + Async Load Balancer
# ================================================

from fastapi import FastAPI, Request
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
import time
import asyncio

app = FastAPI(
    title="SPACE OBFUSCATOR API",
    description="Environment-Locked Lua Protection Service",
    version="19.0.3"
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
    length = random.randint(7, 16)
    prefix = random.choice(["ctx", "slot", "stk", "reg", "var", "pt", "l"])
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    return "_" + prefix + "_" + "".join([random.choice(chars) for _ in range(length)])

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
    # 1. AUTO-PADDING
    if len(code) < 600:
        padding_lines = []
        for _ in range(random.randint(25, 40)):
            v1 = generate_chaotic_var()
            v2 = generate_chaotic_var()
            padding_lines.append("local " + v1 + " = function() return math.sin(" + str(random.randint(1,100)) + ") end; local " + v2 + " = " + v1 + "() and true or false;")
        code = "\n".join(padding_lines) + "\n" + code

    # 2. PROCESAMIENTO CRIPTOGRÁFICO DE SEMILLAS
    offset_1 = random.randint(200000, 800000)
    offset_2 = random.randint(100000, 900000)
    offset_3 = random.randint(300000, 700000)
    
    assumed_base = 3015 
    s1_target = (assumed_base + offset_1) % 4294967296
    s2_target = (assumed_base ^ offset_2) % 4294967296
    s3_target = (assumed_base + offset_3) % 4294967296
    
    prng = MultiStatePRNG(s1_target, s2_target, s3_target)
    
    enc_bytes = bytearray()
    integrity_checksum = 0
    for byte in code.encode('utf-8'):
        sh = prng.next()
        c = (byte + sh) % 256
        enc_bytes.append(c)
        integrity_checksum = (integrity_checksum + c) % 65535
        
    enc_bytes.append(integrity_checksum // 256)
    enc_bytes.append(integrity_checksum % 256)
        
    b64_payload = base64.b64encode(enc_bytes).decode('utf-8')
    
    # 3. APLANAMIENTO POLIMÓRFICO DE PARÁMETROS
    params_real = ["string.byte", "string.char", "string.sub", "table.insert", "os.clock", "type", "pcall", "string.find", "math.floor", "string.gsub"]
    params_fake = [generate_chaotic_var() for _ in params_real]
    
    v_byte, v_char, v_sub, v_insert, v_clock, v_type, v_pcall, v_find, v_floor, v_gsub = params_fake

    v_data, v_b64, v_enc_bytes = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_s1, v_s2, v_s3 = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_dec_idx, v_t_start, v_t_last = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_reader, v_env, v_l, v_ok, v_res = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_src, v_shash, v_sum = generate_chaotic_var(), generate_chaotic_var(), generate_chaotic_var()
    v_check, v_calc_check = generate_chaotic_var(), generate_chaotic_var()

    str_load = '"\\108\\111\\97\\100"'
    str_loadstring = '"\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103"'
    str_getfenv = 'string.char(103,101,116,102,101,110,118)'

    inner_code = (
        "local " + v_env + " = (_ENV or (function() local f = _G[" + str_getfenv + "]; if f then return f() else return _G end end)());\n"
        "local " + v_src + " = (debug and debug.getinfo) and debug.getinfo(1,'S').source or 'stealth';\n"
        "local " + v_shash + " = 0; for i=1, #" + v_src + " do " + v_shash + " = (" + v_shash + " * 31 + " + v_byte + "(" + v_src + ", i)) % 4294967296 end;\n"
        
        "local " + v_sum + " = 0; for _k, _v in pairs(" + v_env + ") do if " + v_type + "(_v) == 'function' then " + v_sum + " = (" + v_sum + " + #_k) % 5000 end end;\n"
        "if " + v_sum + " == 0 then " + v_sum + " = " + str(assumed_base) + " end;\n"
        
        "local " + v_s1 + " = (" + v_sum + " + " + str(offset_1) + " + (" + v_shash + " % 1000)) % 4294967296;\n"
        "local " + v_s2 + " = ((" + v_sum + " ~ " + str(offset_2) + ") + (" + v_shash + " % 500)) % 4294967296;\n"
        "local " + v_s3 + " = (" + v_sum + " + " + str(offset_3) + " - (" + v_shash + " % 2000)) % 4294967296;\n"
        
        "local " + v_b64 + " = \"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\";\n"
        "local " + v_data + " = [=[" + b64_payload + "]=];\n"
        v_data + " = " + v_gsub + "(" + v_data + ", '[^%w%+/=]', '');\n"
        
        "local " + v_enc_bytes + " = {};\n"
        "for i=1, #" + v_data + ", 4 do\n"
        "  local n = (" + v_find + "(" + v_b64 + ", " + v_sub + "(" + v_data + ",i,i), 1, true)-1)*262144+"
        "(" + v_find + "(" + v_b64 + ", " + v_sub + "(" + v_data + ",i+1,i+1), 1, true)-1)*4096+"
        "(" + v_sub + "(" + v_data + ",i+2,i+2)=='=' and 0 or (" + v_find + "(" + v_b64 + ", " + v_sub + "(" + v_data + ",i+2,i+2), 1, true)-1)*64)+"
        "(" + v_sub + "(" + v_data + ",i+3,i+3)=='=' and 0 or (" + v_find + "(" + v_b64 + ", " + v_sub + "(" + v_data + ",i+3,i+3), 1, true)-1));\n"
        "  " + v_insert + "(" + v_enc_bytes + ", " + v_floor + "(n/65536)%256);\n"
        "  if " + v_sub + "(" + v_data + ",i+2,i+2) ~= '=' then " + v_insert + "(" + v_enc_bytes + ", " + v_floor + "(n/256)%256) end;\n"
        "  if " + v_sub + "(" + v_data + ",i+3,i+3) ~= '=' then " + v_insert + "(" + v_enc_bytes + ", n%256) end;\n"
        "end;\n"
        
        "if #" + v_enc_bytes + " < 3 then return nil end;\n"
        "local " + v_check + " = " + v_enc_bytes + "[#" + v_enc_bytes + "-1]*256 + " + v_enc_bytes + "[#" + v_enc_bytes + "];\n"
        "local " + v_calc_check + " = 0; for i=1, #" + v_enc_bytes + "-2 do " + v_calc_check + " = (" + v_calc_check + " + " + v_enc_bytes + "[i]) % 65535 end;\n"
        "if " + v_check + " ~= " + v_calc_check + " then " + v_s3 + " = " + v_s3 + " + 999999 end;\n"
        
        "local " + v_dec_idx + " = 1;\n"
        "local " + v_t_start + " = " + v_clock + "();\n"
        "local " + v_t_last + " = " + v_t_start + ";\n"
        
        "local function " + v_reader + "()\n"
        "  if " + v_dec_idx + " > (#" + v_enc_bytes + "-2) then return nil end;\n"
        "  local now = " + v_clock + "();\n"
        "  local delta = now - " + v_t_last + ";\n"
        "  if delta > 0.3 or (now - " + v_t_start + ") > 4.0 then " + v_s1 + " = (" + v_s1 + " + 7) % 4294967296 end;\n"
        "  " + v_t_last + " = now;\n"
        
        "  " + v_s1 + " = (" + v_s1 + " * 1664525 + 1013904223) % 4294967296;\n"
        "  " + v_s2 + " = (" + v_s2 + " * 22695477 + 1) % 4294967296;\n"
        "  " + v_s3 + " = (" + v_s3 + " + " + v_s1 + ") % 4294967296;\n"
        "  local sh = (" + v_s1 + " + " + v_s2 + " + " + v_s3 + ") % 256;\n"
        
        "  local m = " + v_enc_bytes + "[" + v_dec_idx + "];\n"
        "  local dec = (m - sh) % 256;\n"
        "  if dec < 0 then dec = dec + 256 end;\n"
        "  " + v_dec_idx + " = " + v_dec_idx + " + 1;\n"
        "  return " + v_char + "(dec);\n"
        "end;\n"
        
        "local " + v_l + " = " + v_env + "[" + str_load + "] or " + v_env + "[" + str_loadstring + "];\n"
        "local " + v_ok + ", " + v_res + " = " + v_pcall + "(" + v_l + ", " + v_reader + ");\n"
        "if " + v_ok + " and " + v_type + "(" + v_res + ") == 'function' then return " + v_res + "(...) end;\n"
    )

    params_fake_str = ",".join(params_fake)
    params_real_str = ",".join(params_real)
    
    wrapper = "return (function(" + params_fake_str + ")\n" + inner_code + "\nend)(" + params_real_str + ")"
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

# Diccionario en memoria para rastrear IPs y limitar spam
user_requests = {}

@app.post("/api/obfuscate", response_model=ObfuscateResponse)
async def obfuscate(request: ObfuscateRequest, fastapi_req: Request):
    try:
        # ANTI-SPAM BÁSICO: Limita a 1 petición cada 3 segundos por IP
        client_ip = fastapi_req.client.host
        current_time = time.time()
        
        if client_ip in user_requests:
            if current_time - user_requests[client_ip] < 3.0:
                return ObfuscateResponse(success=False, error="Por favor, espera unos segundos entre cada ofuscación.")
        user_requests[client_ip] = current_time

        if not request.code or not request.code.strip():
            return ObfuscateResponse(success=False, error="El código está vacío")
        
        # Límite de 5MB para no reventar la memoria RAM del servidor
        max_size = 5 * 1024 * 1024 
        if len(request.code) > max_size:
            return ObfuscateResponse(success=False, error="El código excede el límite permitido (5MB)")
        
        layers_to_apply = request.layers if request.layers is not None else 5
        
        # MAGIA ASÍNCRONA: Envía el trabajo pesado a otro hilo (evita que se caiga la página para otros usuarios)
        obfuscated = await asyncio.to_thread(obfuscate_code, request.code, request.mode, layers_to_apply)
        
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
