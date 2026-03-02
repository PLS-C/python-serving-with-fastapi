from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import numpy as np
from scipy import signal

# 1. ตั้งค่า Rate Limiter (จำกัด 5 requests/minute/IP)
# เพิ่ม config_filename=None เพื่อสั่งให้ระบบไม่ต้องไปตามหาไฟล์ .env
limiter = Limiter(key_func=get_remote_address, config_filename=None)
app = FastAPI(title="Python Serving API (Math & Signal)")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. ตั้งค่า CORS เผื่อการเรียกใช้จาก Web Frontend หรือ LabVIEW ข้ามโดเมน
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. Pydantic Models สำหรับกำหนดโครงสร้าง JSON ขาเข้า
# ==========================================
class SolvParams(BaseModel):
    A: float
    B: float
    C: float

class WaveParams(BaseModel):
    Amplitude: float
    Frequency: float
    Number_of_Sample: int
    Sampling_Frequency: float
    Shape: int

class PolyFitParams(BaseModel):
    X: list[float]
    Y: list[float]
    Order: int

class PolarParams(BaseModel):
    r: list[float]
    phi: list[float]

# ==========================================
# 4. API Endpoints
# ==========================================

@app.get("/calling")
@limiter.limit("5/minute")
async def calling(request: Request):
    return {"status": "success", "text": "Hello"}

@app.get("/test_numpy")
@limiter.limit("5/minute")
async def test_numpy(request: Request):
    # สุ่มค่าระหว่าง 1.0 ถึง 3.0 จำนวน 3 ค่า
    x = np.random.uniform(1.0, 3.0, 3)
    return {"Data": x.tolist()}

@app.post("/solv")
@limiter.limit("5/minute")
async def solv(request: Request, data: SolvParams):
    coefficient = np.array([data.A, data.B, data.C])
    p = np.poly1d(coefficient)
    sol = p.roots
    sol_real = np.real(sol).tolist()
    sol_angle = np.angle(sol).tolist()
    return {"sol_real": sol_real, "sol_angle": sol_angle}

@app.post("/creating_noisy")
@limiter.limit("5/minute")
async def creating_noisy(request: Request, data: WaveParams):
    delta_t = 1 / data.Sampling_Frequency
    start = 0
    step = delta_t
    stop = data.Number_of_Sample * delta_t
    t = np.arange(start, stop, step)
    
    if data.Shape == 2: # Sine
        y = data.Amplitude * np.sin(2 * np.pi * data.Frequency * t)
    elif data.Shape == 1: # Ramp/Sawtooth
        y = data.Amplitude * signal.sawtooth(2 * np.pi * data.Frequency * t)
    elif data.Shape == 0: # Square
        y = data.Amplitude * signal.square(2 * np.pi * data.Frequency * t, duty=0.5)
    noise = np.random.normal(0, 1, data.Number_of_Sample)
    add_noise = y + noise
    
    return {"t": t.tolist(), "y": add_noise.tolist()}

@app.post("/wave_gen")
@limiter.limit("5/minute")
async def wave_gen(request: Request, data: WaveParams):
    delta_t = 1 / data.Sampling_Frequency
    start = 0
    step = delta_t
    stop = data.Number_of_Sample * delta_t
    t = np.arange(start, stop, step)
    y = np.zeros(t.shape)
    
    if data.Shape == 2: # Sine
        y = data.Amplitude * np.sin(2 * np.pi * data.Frequency * t)
    elif data.Shape == 1: # Ramp/Sawtooth
        y = data.Amplitude * signal.sawtooth(2 * np.pi * data.Frequency * t)
    elif data.Shape == 0: # Square
        y = data.Amplitude * signal.square(2 * np.pi * data.Frequency * t, duty=0.5)
        
    return {"t": t.tolist(), "y": y.tolist()}

@app.post("/poly_fit")
@limiter.limit("5/minute")
async def poly_fit(request: Request, data: PolyFitParams):
    c = np.polyfit(data.X, data.Y, data.Order)
    poly_func = np.poly1d(c)
    z = poly_func(np.array(data.X))
    return {"x": data.X, "z": z.tolist()}

@app.post("/polar_to_rect")
@limiter.limit("5/minute")
async def polar_to_rect(request: Request, data: PolarParams):
    # แปลง input list ให้เป็น numpy array เพื่อคำนวณแบบ Vectorization
    r_arr = np.array(data.r)
    phi_arr = np.array(data.phi)   
    # คำนวณ x และ y รวดเดียวทั้ง array
    # หลักการ: x = r * cos(phi), y = r * sin(phi)
    x = r_arr * np.cos(phi_arr)
    y = r_arr * np.sin(phi_arr)
    
    # แปลง numpy array กลับเป็น list เพื่อส่งออกเป็น JSON
    return {"x": x.tolist(), "y": y.tolist()}