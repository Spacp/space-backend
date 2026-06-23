# ================================================
#   SPACE OBFUSCATOR - Backend Server (Ultra Optimized)
#   Military-Grade Polimorphic Engine v7 (CTF Unbreakable)
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
    description="Military-Grade Lua Protection Service",
    version="17.0.0"
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
    # Nombres erráticos para romper la visual
    length = random.randint(8, 26)
    return "_" + "".join(random.choices("O0I1l", k=length))

# PRNG Multi-Estado Exacto para replicar en Lua
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
    Motor v7: 
    - Semillas Dinámicas por Checksum Ambiental.
    - Timing Checks Totales.
    - Padding Lua Válido.
    - Payload Splitting Caótico.
    """
    # 1. PADDING LÓGICO INOFENSIVO (Anti-Reconocimiento)
    fake_code = ""
    for _ in range(random.randint(3, 7)):
        v = generate_illusion_var()
        n = random.randint(10, 99)
        fake_code += f"local {v}=type({n})=='number' and {n*2} or 0;"
    code = fake_code + "\n" + code

    # 2. GENERACIÓN DE SEMILLAS
    s1_target = random.randint(100000, 999999)
    s2_target = random.randint(100000, 999999)
    s3_target = random.randint(100000, 999999)
    
    # La suma ASCII de las 5 funciones ["pairs","ipairs","tostring","pcall","type"] es exactamente 3015
    base_sum = 3015 
    
    def calc_derivation(target):
        m = random.randint(10, 150)
        o = target - (base_sum * m)
        op = "+" if o >= 0 else "-"
        return f"(_sum*{m}{op}{abs(o)})%4294967296"

    prng = MultiStatePRNG(s1_target, s2_target, s3_target)
    
    # 3. ENCRIPTACIÓN ESCAPADA
    enc_str = ""
    for byte in code.encode('utf-8'):
        sh = prng.next()
        c = (byte + sh) % 256
        enc_str += f"\\{c:03d}"
        
    # 4. FRAGMENTACIÓN CAÓTICA DEL PAYLOAD
    # Se divide el payload en 4 fragmentos
    q = len(enc_str) // 4
    parts = [enc_str[0:q], enc_str[q:q*2], enc_str[q*2:q*3], enc_str[q*3:]]
    
    v_parts = [generate_illusion_var() for _ in range(4)]
    
    # Declaramos los fragmentos en orden normal
    chunk_declarations = "".join([f"local {v}=\"{p}\";" for v, p in zip(v_parts, parts)])
    
    # Lua los une usando sus variables, nosotros decidimos el orden (que en este caso es 1,2,3,4 pero ofuscado)
    v_data = generate_illusion_var()
    payload_concat = f"local {v_data}={v_parts[0]}..{v_parts[1]}..{v_parts[2]}..{v_parts[3]};"

    # Variables de Entorno y Lógica
    v_s1, v_s2, v_s3 = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_env, v_idx, v_time = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    v_reader, v_ok, v_res = generate_illusion_var(), generate_illusion_var(), generate_illusion_var()
    
    # CONSTRUCCIÓN DE STRINGS GLOBALES OFUSCADOS (pairs, ipairs, tostring, pcall, type)
    str_pairs = "string.char(112,97,105,114,115)"
    str_ipairs = "string.char(105,112,97,105,114,115)"
    str_tostring = "string.char(116,111,115,116,114,105,110,103)"
    str_pcall = "string.char(112,99,97,108,108)"
    str_type = "string.char(116,121,112,101)"

    # SETUP LUA: CÁLCULO DE CHECKSUM DEL ENTORNO (Da 3015 si no ha sido hookeado)
    setup_code = (
        f"local {v_env}=getfenv and getfenv() or _ENV;"
        f"local {v_time}=os.clock and os.clock() or 0;"
        f"local _g={{{str_pairs},{str_ipairs},{str_tostring},{str_pcall},{str_type}}};"
        f"local _sum=0;"
        f"for i=1,5 do local n=_g[i]; if type({v_env}[n])~=\"function\" then _sum=_sum+999 end; for j=1,#n do _sum=_sum+string.byte(n,j) end; end;"
        f"local {v_s1}={calc_derivation(s1_target)};"
        f"local {v_s2}={calc_derivation(s2_target)};"
        f"local {v_s3}={calc_derivation(s3_target)};"
        f"{chunk_declarations}{payload_concat}"
        f"local {v_idx}=1;"
    )
    
    # READER FUNCTION: Timing Total (2.0s) + Decodificación Multi-Estado
    reader_func = (
        f"local function {v_reader}() "
        f"if {v_idx}>#{v_data} then return nil end;"
        
        # Timing Check Global
        f"if (os.clock() - {v_time}) > 2.0 then {v_s3}={v_s3}+1 end;"
        
        # PRNG Multi-Estado
        f"{v_s1}=({v_s1}*1664525+1013904223)%4294967296;"
        f"{v_s2}=({v_s2}*22695477+1)%4294967296;"
        f"{v_s3}=({v_s3}+{v_s1})%4294967296;"
        f"local sh=({v_s1}+{v_s2}+{v_s3})%256;"
        
        f"local m=string.byte({v_data},{v_idx});"
        f"local dec=(m-sh)%256;"
        f"if dec<0 then dec=dec+256 end;"
        f"{v_idx}={v_idx}+1;"
        f"return string.char(dec);"
        f"end;"
    )
    
    # EXECUTION WRAPPER: Constructor oculto para "load" + pcall silencioso
    run_logic = (
        f"local _l_name=string.char(100+8,100+11,90+7,100);" # Crea "load" matemáticamente
        f"local _l_str=string.char(108,111,97,100,115,116,114,105,110,103);" # "loadstring"
        f"local _l={v_env}[_l_name] or {v_env}[_l_str];"
        f"local {v_ok},{v_res}=pcall(_l,{v_reader});"
        f"if {v_ok} and type({v_res})==\"function\" then return {v_res}(...) end;"
    )
    
    # Retorno fusionado en una línea inquebrantable
    return f"return(function(...) {setup_code}{reader_func}{run_logic} end)(...);"

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
            mode_used=f"Engine V7 Ultimate ({min(layers_to_apply, 10)}-Layers)",
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
