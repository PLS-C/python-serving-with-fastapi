from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from scipy import signal
import time
from collections import defaultdict

# ==========================================
# จำกัด 5 requests/minute ต่อ IP
# ==========================================
RATE_LIMIT = 5
WINDOW_SECONDS = 60
request_counts: dict = defaultdict(list)

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    timestamps = request_counts[ip]
    request_counts[ip] = [t for t in timestamps if now - t < WINDOW_SECONDS]
    if len(request_counts[ip]) >= RATE_LIMIT:
        return True
    request_counts[ip].append(now)
    return False

app = FastAPI(title="Python Serving API (Math & Signal)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Pydantic Models
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
# API Endpoints
# ==========================================

@app.get("/calling")
async def calling(request: Request):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    return {"status": "success", "text": "Hello"}

@app.get("/test_numpy")
async def test_numpy(request: Request):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    x = np.random.uniform(1.0, 3.0, 3)
    return {"Data": x.tolist()}

@app.post("/solv")
async def solv(request: Request, data: SolvParams):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    coefficient = np.array([data.A, data.B, data.C])
    p = np.poly1d(coefficient)
    sol = p.roots
    return {"sol_real": np.real(sol).tolist(), "sol_angle": np.angle(sol).tolist()}

@app.post("/creating_noisy")
async def creating_noisy(request: Request, data: WaveParams):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    delta_t = 1 / data.Sampling_Frequency
    t = np.arange(0, data.Number_of_Sample * delta_t, delta_t)

    if data.Shape == 2:
        y = data.Amplitude * np.sin(2 * np.pi * data.Frequency * t)
    elif data.Shape == 1:
        y = data.Amplitude * signal.sawtooth(2 * np.pi * data.Frequency * t)
    elif data.Shape == 0:
        y = data.Amplitude * signal.square(2 * np.pi * data.Frequency * t, duty=0.5)
    else:
        y = np.zeros(t.shape)

    noise = np.random.normal(0, 1, data.Number_of_Sample)
    return {"t": t.tolist(), "y": (y + noise).tolist()}

@app.post("/wave_gen")
async def wave_gen(request: Request, data: WaveParams):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    delta_t = 1 / data.Sampling_Frequency
    t = np.arange(0, data.Number_of_Sample * delta_t, delta_t)
    y = np.zeros(t.shape)

    if data.Shape == 2:
        y = data.Amplitude * np.sin(2 * np.pi * data.Frequency * t)
    elif data.Shape == 1:
        y = data.Amplitude * signal.sawtooth(2 * np.pi * data.Frequency * t)
    elif data.Shape == 0:
        y = data.Amplitude * signal.square(2 * np.pi * data.Frequency * t, duty=0.5)

    return {"t": t.tolist(), "y": y.tolist()}

@app.post("/poly_fit")
async def poly_fit(request: Request, data: PolyFitParams):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    c = np.polyfit(data.X, data.Y, data.Order)
    poly_func = np.poly1d(c)
    z = poly_func(np.array(data.X))
    return {"x": data.X, "z": z.tolist()}

@app.post("/polar_to_rect")
async def polar_to_rect(request: Request, data: PolarParams):
    if is_rate_limited(request.client.host):
        return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})
    r_arr = np.array(data.r)
    phi_arr = np.array(data.phi)
    x = r_arr * np.cos(phi_arr)
    y = r_arr * np.sin(phi_arr)
    return {"x": x.tolist(), "y": y.tolist()}

