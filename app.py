# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Enterprise Grade: Parameter Flattening & Base64 Payload (V8)
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
    description="Enterprise-Grade Lua Protection Service",
    version="18.0.0"
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

def generate_illusion_var():
    # Variables de tamaño caótico
    length = random.randint(5, 20)
    return "_" + "".join(random.choices("O0I1l", k=length))

# PRNG Multi-Estado
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
    Motor v8 (Luraph/Prometheus Architecture Clone):
    - Parameter Flattening.
    - Base64 High-Density Encoding (Capa 1).
    - PRNG Encryption (Capa 2).
    """
    
    # GENERACIÓN DE SEMILLAS
    s1 = random.randint(100000, 999999)
    s2 = random.randint(100000, 999999)
    s3 = random.randint(100000, 999999)
    prng = MultiStatePRNG(s1, s2, s3)
    
    # ENCRIPTACIÓN MATEMÁTICA DEL PAYLOAD
    enc_bytes = bytearray()
    for byte in code.encode('utf-8'):
        sh = prng.next()
        c = (byte + sh) % 256
        enc_bytes.append(c)
        
    # CODIFICACIÓN DE ALTA DENSIDAD (BASE64)
    # Esto simula la Capa 1 de Base85 que analizó Claude
    b64_payload = base64.b64encode(enc_bytes).decode('utf-8')
    
    # APLANAMIENTO DE PARÁMETROS (Parameter Flattening)
    # Mapeamos funciones nativas a variables aleatorias
    params_real = ["string.byte", "string.char", "string.sub", "table.insert", "table.concat", "os.clock", "type", "pcall", "string.find", "math.floor", "getfenv", "string.gsub"]
    params_fake = [generate_illusion_var() for _ in params_real]
    
    v_byte, v_char, v_sub, v_insert, v_concat, v_clock, v_type, v_pcall, v_find, v_floor, v_env, v_gsub = params_fake

    # Otras variables internas
    v_data, v_b64, v_out = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_s1, v_s2, v_s3 = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_enc_bytes, v_dec_idx, v_t_start = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_reader, v_env_table, v_l = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_ok, v_res = generate_illusion_var(), generate_illusion_var()
    
    # CÓDIGO INTERNO FLATTENED (Las funciones ahora son "v_sub", "v_find", etc.)
    inner_code = (
        f"local {v_b64}=\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\";"
        f"local {v_data}=[=[{b64_payload}]=];"
        f"{v_data}={v_gsub}({v_data},'[^%w%+/=]','');"
        
        # DECODIFICADOR BASE64 A BYTES EN MEMORIA PRIVADA
        f"local {v_enc_bytes}={{}};"
        f"for i=1,#{v_data},4 do "
        f"local n=({v_find}({v_b64},{v_sub}({v_data},i,i),1,true)-1)*262144+"
        f"({v_find}({v_b64},{v_sub}({v_data},i+1,i+1),1,true)-1)*4096+"
        f"({v_sub}({v_data},i+2,i+2)=='=' and 0 or ({v_find}({v_b64},{v_sub}({v_data},i+2,i+2),1,true)-1)*64)+"
        f"({v_sub}({v_data},i+3,i+3)=='=' and 0 or ({v_find}({v_b64},{v_sub}({v_data},i+3,i+3),1,true)-1));"
        f"{v_insert}({v_enc_bytes},{v_floor}(n/65536)%256);"
        f"if {v_sub}({v_data},i+2,i+2)~='=' then {v_insert}({v_enc_bytes},{v_floor}(n/256)%256) end;"
        f"if {v_sub}({v_data},i+3,i+3)~='=' then {v_insert}({v_enc_bytes},n%256) end;"
        f"end;"
        
        # TIMING CHECK Y PRNG DECRYPTOR
        f"local {v_s1},{v_s2},{v_s3}={s1},{s2},{s3};"
        f"local {v_dec_idx}=1;"
        f"local {v_t_start}={v_clock}();"
        
        f"local function {v_reader}() "
        f"if {v_dec_idx}>#{v_enc_bytes} then return nil end;"
        f"if ({v_clock}()-{v_t_start})>2.0 then {v_s3}={v_s3}+1 end;" # Trampa Anti-Emulación
        
        f"{v_s1}=({v_s1}*1664525+1013904223)%4294967296;"
        f"{v_s2}=({v_s2}*22695477+1)%4294967296;"
        f"{v_s3}=({v_s3}+{v_s1})%4294967296;"
        f"local sh=({v_s1}+{v_s2}+{v_s3})%256;"
        
        f"local m={v_enc_bytes}[{v_dec_idx}];"
        f"local dec=(m-sh)%256;"
        f"if dec<0 then dec=dec+256 end;"
        f"{v_dec_idx}={v_dec_idx}+1;"
        f"return {v_char}(dec);"
        f"end;"
        
        # EJECUCIÓN DINÁMICA OCULTA
        f"local {v_env_table}={v_env} and {v_env}() or _ENV;"
        f"local {v_l}={v_env_table}[\"\\108\\111\\97\\100\"] or {v_env_table}[\"\\108\\111\\97\\100\\115\\116\\114\\105\\110\\103\"];"
        f"local {v_ok},{v_res}={v_pcall}({v_l},{v_reader});"
        f"if {v_ok} and {v_type}({v_res})==\"function\" then return {v_res}(...) end;"
    )

    # UNIMOS EL APLANAMIENTO CON EL CÓDIGO INTERNO
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
            mode_used=f"Enterprise Engine V8 ({min(layers_to_apply, 10)}-Layers)",
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
