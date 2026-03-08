*Read this in other languages: [English](README.md)*

# 🚀 python-serving-with-fastapi

โปรเจกต์นี้สร้างด้วย Python และ FastAPI เพื่อให้บริการคำนวณทางคณิตศาสตร์และประมวลผลสัญญาณ (Signal Processing) แก่โปรแกรมภายนอก เช่น **LabVIEW**, Web Application หรือซอฟต์แวร์ทางวิศวกรรมอื่นๆ

## 📌 วัตถุประสงค์ของโครงการ
* เรียนรู้การเปลี่ยนสคริปต์ Python ให้เป็น API Service ที่พร้อมใช้งาน
* ฝึกการใช้งาน **Docker** เพื่อจัดการสภาพแวดล้อม (Environment) ให้ทำงานได้เหมือนกันทุกที่
* เข้าใจพื้นฐานการรับ-ส่งข้อมูลรูปแบบ **JSON** ระหว่างภาษาที่ต่างกัน
* ปูพื้นฐานสู่การทำ Model Serving สำหรับงาน Deep Learning ในอนาคต

---

## 📂 1. การเตรียมตัวและดาวน์โหลดไฟล์
1.  **ดาวน์โหลดโปรเจกต์**: 
    * คลิกที่ปุ่มสีเขียวด้านบน **"<> Code"** จากนั้นเลือก **Download ZIP** แล้วทำการแตกไฟล์
    * หรือใช้คำสั่ง Git: `git clone https://github.com/PLS-C/python-serving-with-fastapi.git`
2.  **โปรแกรมที่จำเป็นต้องติดตั้ง**:
    * [Docker Desktop](https://www.docker.com/products/docker-desktop/) (สำหรับทดสอบในเครื่อง)
    * [LabVIEW](https://www.ni.com/th-th/support/downloads/software-products/download.labview.html)

---

## 🛠️ 2. ตัวอย่างที่ 1: การทดสอบบน Docker Desktop (Local)
วิธีนี้เหมาะสำหรับการพัฒนาและแก้ไขโค้ดในเครื่องตนเอง

1.  **เปิด Terminal/PowerShell**: เข้าไปยังโฟลเดอร์ของโปรเจกต์
2.  **Build Docker Image**: สร้าง Image สำหรับรันโค้ด
    ```bash
    docker build -t py-serving-app .
    ```
3.  **Run Container (Developer Mode)**: รันโค้ดโดยผูกโฟลเดอร์ในเครื่องเข้ากับ Docker เพื่อให้แก้ไขโค้ดได้สดๆ
    ```powershell
    docker run -d --name py-serving-container -p 8080:8080 -v "${PWD}:/workspace" py-serving-app uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    ```
    * *หมายเหตุ: คำสั่ง `-v` จะทำการ Mount โฟลเดอร์ `app` และ `--reload` จะรีสตาร์ทเซิร์ฟเวอร์ให้อัตโนมัติเมื่อมีการเซฟไฟล์ `${PWD}` คือตำแหน่งโฟลเดอร์ปัจจุบันของคุณ*
4.  **ตรวจสอบสถานะ**: เปิดเบราว์เซอร์ไปที่ `http://localhost:8080/docs` เพื่อทดสอบ API ผ่านหน้าเว็บ Swagger UI

---

## ☁️ 3. ตัวอย่างที่ 2: การทดสอบบน Google Cloud Run (Step-by-Step)

วิธีนี้คือการนำโปรเจกต์ขึ้นสู่ระบบคลาวด์จริง เพื่อให้โปรแกรมภายนอกสามารถเรียกใช้งานผ่านอินเทอร์เน็ตได้ โดยใช้เครื่องมือ **Cloud Shell**

### ✅ สิ่งที่ต้องเตรียม (Prerequisites)
- **Google Account**: บัญชี Gmail ทั่วไป
- **Google Cloud Console**: เข้าใช้งานได้ที่ [console.cloud.google.com](https://console.cloud.google.com)
- **Billing**: ต้องทำการเปิดการเรียกเก็บเงิน (Enable Billing) สำหรับโปรเจกต์นั้นๆ

---

### Step 1: เลือกหรือสร้าง Project
1. เข้าไปที่ Google Cloud Console
2. คลิกที่แถบเลือกโปรเจกต์ด้านบน แล้วกด **"New Project"**
3. ตั้งชื่อโปรเจกต์และจดบันทึก **Project ID** ไว้

### Step 2: เปิดใช้งาน APIs ที่จำเป็น
ไปที่ **Navigation Menu > APIs & Services > Library** จากนั้นค้นหาและกด **"Enable"** บริการดังนี้:
1. ✅ **Cloud Run API**
2. ✅ **Artifact Registry API**
3. ✅ **Cloud Build API**

### Step 3: อัปโหลดโค้ดสู่ Cloud Shell Editor
1. คลิกไอคอน **Cloud Shell** (`>_`) ที่มุมขวาบน
2. คลิกปุ่ม **"Open Editor"**
3. สร้างโฟลเดอร์โปรเจกต์ใน Terminal:
   ```bash
   mkdir python-serving-app
   cd python-serving-app
   ```
4. **ทำการอัปโหลดไฟล์**: คลิกขวาที่โฟลเดอร์เลือก **Upload Files** (อัปโหลด `main.py`, `Dockerfile`, และ `requirements.txt`)

### Step 4: สร้าง Artifact Registry repository
ไปที่: 🔗 [console.cloud.google.com/artifacts](https://console.cloud.google.com/artifacts)
1. คลิก **"Create Repository"**
2. ตั้งค่า: Name=`serving-repo`, Format=`Docker`, Region=`asia-southeast3` (หรือตามที่คุณต้องการ)
3. คลิก **Create**

### Step 5: กำหนดค่าตัวแปร (Environment Variables)

ตรวจสอบ Project ID ด้วยคำสั่ง:
```bash
echo $(gcloud config get-value project)
```
หากค่าว่างเปล่า ให้รันคำสั่ง:
```bash
gcloud config set project <รหัสโปรเจกต์ของคุณ>
```

คัดลอกและวางคำสั่งนี้ใน **Cloud Shell Terminal**:
```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=asia-southeast3           # ต้องตรงกับ Region ใน Step 4
export REPO_NAME=serving-repo           
export IMAGE_NAME=serving-api           
```

### Step 6: ทำการ Build Image
รันคำสั่งเพื่อสร้าง Docker Image บนระบบคลาวด์:
```bash
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} .
```

### Step 7: Deploy the Image ไปยัง Cloud Run
รันคำสั่งนี้เพื่อนำ Image ขึ้นไปให้บริการเป็น API:
```bash
gcloud run deploy serving-api \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:latest \
  --region=${REGION} \
  --allow-unauthenticated \
  --port=8080 \
  --max-instances=2 \
  --memory=512Mi
```

### Step 8: การจัดการสิทธิ์เข้าถึง (เปิด/ปิด บริการ)
ใช้คำสั่งเหล่านี้เพื่อควบคุมการเข้าถึง API ของคุณจากบุคคลภายนอก:

**หากต้องการ "ปิด" การเข้าถึง (ล็อกประตู):**
```bash
gcloud run services remove-iam-policy-binding serving-api \
  --region=$REGION \
  --member="allUsers" \
  --role="roles/run.invoker"
```
**หากต้องการ "เปิด" การเข้าถึง (ปลดล็อก):**
```bash
gcloud run services add-iam-policy-binding serving-api \
  --region=$REGION \
  --member="allUsers" \
  --role="roles/run.invoker"
```

---

## 4. การจัดการค่าใช้จ่ายและการตรวจสอบทรัพยากร

เพื่อให้การใช้งานอยู่ในโควต้าฟรี (**Free Tier**) 100% โปรดตรวจสอบทรัพยากรตามขั้นตอนต่อไปนี้

### 4.1 การควบคุมค่าใช้จ่ายอัตโนมัติ
* **Scale to Zero**: Cloud Run จะปิดเครื่องอัตโนมัติเมื่อไม่มีการใช้งาน คุณจะจ่ายเงินเฉพาะช่วงเวลาที่มีการประมวลผลคำขอจริงๆ
* **Request Quota**: คุณได้สิทธิ์ใช้งานฟรี **2 ล้าน Requests ต่อเดือน** การล็อกบริการใน Step 8 จะช่วยป้องกันไม่ให้เสียโควต้านี้โดยไม่จำเป็น

### 4.2 การตรวจสอบพื้นที่จัดเก็บ (Storage)
คุณต้องจัดการพื้นที่ 2 ส่วนเพื่อให้อยู่ในเกณฑ์ฟรี:

#### **A) Artifact Registry (คลังเก็บ Image)**
* **โควต้าฟรี**: **500 MB** ต่อเดือน
* **ตัวอย่างจริง**: Image ทั่วไปของโปรเจกต์นี้จะอยู่ที่ประมาณ **~117 MB** (คิดเป็น 23% ของโควต้าฟรี)
* **คำสั่งตรวจสอบ**:
```bash
gcloud artifacts docker images list ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}
```

#### **B) Cloud Shell Editor Storage**
* **โควต้าฟรี**: **5 GB** (พื้นที่คงทน)
* **ตัวอย่างจริง**: ไฟล์โค้ดมีขนาดเล็กมาก มักจะอยู่ในระดับ **KB** (เช่น 50 KB)
* **คำสั่งตรวจสอบ**:
```bash
du -sh .
```

### 4.3 ตารางสรุปการใช้ทรัพยากร

| ทรัพยากร | โควต้าฟรีต่อเดือน | การใช้งานโดยประมาณ | สิ่งที่ควรทำเมื่อใกล้เต็ม |
| :--- | :--- | :--- | :--- |
| **Cloud Run Requests** | 2 ล้านครั้ง | ~0 (เมื่อล็อกบริการ) | ใช้ Step 8 เพื่อปิดการเข้าถึง |
| **Artifact Registry** | 500 MB | **~117 MB** | ลบ Image Digest รุ่นเก่าทิ้ง |
| **Cloud Shell Disk** | 5 GB | **~ระดับ KB** | ลบไฟล์หรือโฟลเดอร์ที่ไม่ใช้แล้ว |

---

### 4.4 การลบทรัพยากรทั้งหมด (Full Cleanup)
หากต้องการลบทุกอย่างเพื่อความมั่นใจ 100% ให้ทำตามลำดับดังนี้:

1. **ลบ Cloud Run Service**: ไปที่หน้า Cloud Run เลือก `serving-api` แล้วกด **Delete**
2. **ลบ Image ใน Artifact Registry (สำคัญที่สุด!) ⚠️**: การลบ Service ไม่ได้ลบไฟล์ Image ทิ้ง ให้ไปที่ Artifact Registry -> `serving-repo` แล้วเลือกลบ Image ทั้งหมดเพื่อคืนพื้นที่
3. **ลบไฟล์ชั่วคราวใน Cloud Storage**: ลบ Bucket ที่ขึ้นต้นด้วย `artifacts.[PROJECT_ID].appspot.com` ซึ่งเก็บ Log การ Build ไว้
