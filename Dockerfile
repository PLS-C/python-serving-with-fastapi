# ใช้ Python 3.10 แบบ Slim เพื่อลดขนาด Image
FROM python:3.10-slim

# กำหนดโฟลเดอร์ทำงานภายใน Container
WORKDIR /workspace

# ก๊อปปี้ไฟล์ requirements.txt และติดตั้ง Library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ก๊อปปี้โฟลเดอร์ app/ ทั้งหมดเข้าไปใน Container
COPY app/ ./app/

# กำหนด Port (Cloud Run มักจะใช้พอร์ต 8080 นี้เป็นค่าเริ่มต้น)
ENV PORT=8080

# คำสั่งเริ่มต้นเมื่อ Container รัน (ชี้ไปที่โฟลเดอร์ app และไฟล์ main)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]