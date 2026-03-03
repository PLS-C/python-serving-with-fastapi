*Read this in other languages: [English](README.md)*

# 🚀 python-serving-with-fastapi

โปรเจกต์นี้สร้างด้วย Python และ FastAPI เพื่อให้บริการคำนวณทางคณิตศาสตร์และประมวลผลสัญญาณ (Signal Processing) แก่โปรแกรมภายนอก เช่น **LabVIEW**, Web Application หรือซอฟต์แวร์ทางวิศวกรรมอื่นๆ

## 📌 วัตถุประสงค์ของโครงการ
* เรียนรู้การเปลี่ยนสคริปต์ Python ให้เป็น API Service ที่พร้อมใช้งาน.
* ฝึกการใช้งาน **Docker** เพื่อจัดการสภาพแวดล้อม (Environment) ให้ทำงานได้เหมือนกันทุกที่.
* เข้าใจพื้นฐานการรับ-ส่งข้อมูลรูปแบบ **JSON** ระหว่างภาษาที่ต่างกัน.
* ปูพื้นฐานสู่การทำ Model Serving สำหรับงาน Deep Learning ในอนาคต.

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
2.  **Build Docker Image**: สร้าง "กล่อง" สำหรับรันโค้ดของเรา
    ```bash
    docker build -t py-serving-app .
    ```
    * *หมายเหตุ: 
3.  **Run Container (Developer Mode)**: รันโค้ดโดยผูกโฟลเดอร์ในเครื่องเข้ากับ Docker เพื่อให้แก้ไขโค้ดได้สดๆ
    ```powershell
    docker run -d --name py-serving-container -p 8080:8080 -v "${PWD}:/workspace" py-serving-app uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    ```
    * *หมายเหตุ: คำสั่ง `-v` จะทำการ Mount โฟลเดอร์ `app` และ `--reload` จะรีสตาร์ทเซิร์ฟเวอร์ให้อัตโนมัติเมื่อมีการเซฟไฟล์* ${PWD} คือ เส้นทาง (Path) ของโฟลเดอร์ปัจจุบันที่คุณกำลังเปิด Terminal/PowerShell
4.  **ตรวจสอบสถานะ**: เปิดเบราว์เซอร์ไปที่ `http://localhost:8080/docs` เพื่อทดสอบ API ผ่านหน้าเว็บ Swagger UI

---

## ☁️ 3. ตัวอย่างที่ 2: การทดสอบบน Google Cloud Run (Step-by-Step)

วิธีนี้คือนำโปรเจกต์ขึ้นสู่ระบบคลาวด์จริง เพื่อให้โปรแกรมจากภายนอก (เช่น LabVIEW จากเครื่องอื่น) สามารถเรียกใช้งานผ่านอินเทอร์เน็ตได้ โดยใช้เครื่องมือ **Cloud Shell** บนเว็บเบราว์เซอร์

### ✅ สิ่งที่ต้องเตรียม (Prerequisites)
- **Google Account**: บัญชี Gmail ทั่วไป
- **Google Cloud Console**: เข้าใช้งานได้ที่ [console.cloud.google.com](https://console.cloud.google.com)
- **Billing**: ต้องทำการเปิดการเรียกเก็บเงิน (Enable Billing) สำหรับโปรเจกต์นั้นๆ (เพื่อยืนยันตัวตนการใช้โควต้าฟรี)

---

### Step 1: เลือกหรือสร้าง Project
1. เข้าไปที่ Google Cloud Console
2. คลิกที่แถบเลือกโปรเจกต์ด้านบน แล้วกด **"New Project"**
3. ตั้งชื่อโปรเจกต์ให้เรียบร้อย (เช่น `python-serving-project`) และจดบันทึก **Project ID** ไว้

### Step 2: เปิดใช้งาน APIs ที่จำเป็น
ไปที่ **Navigation Menu > APIs & Services > Library** จากนั้นค้นหาและกด **"Enable"** 3 บริการดังนี้:
1.  ✅ **Cloud Run API** (Cloud Run Admin API)
2.  ✅ **Artifact Registry API**
3.  ✅ **Cloud Build API**
*ตรวจสอบให้มั่นใจว่าทั้ง 3 สถานะขึ้นว่า "Enabled" เรียบร้อยแล้ว*

### Step 3: อัปโหลดโค้ดสู่ Cloud Shell Editor
1. คลิกไอคอน **Cloud Shell** (รูป Terminal `>_`) ที่มุมขวาบนของหน้าจอ
2. เมื่อหน้าต่าง Terminal ปรากฏขึ้น ให้คลิกปุ่ม **"Open Editor"**
3. สร้างโฟลเดอร์สำหรับโปรเจกต์ใน Terminal ด้วยคำสั่ง:
   ```bash
   mkdir python-serving-app
   cd python-serving-app
   
4.  **ทำการอัปโหลดไฟล์**: 
  * คลิกขวาที่โฟลเดอร์ `python-serving-app` ในหน้าต่าง Editor แล้วเลือก **Upload Files**
  * เลือกไฟล์ทั้ง 3 ไฟล์จากเครื่องของคุณ: `main.py`, `Dockerfile`, และ `requirements.txt`
  * *ตรวจสอบให้แน่ใจว่าไฟล์ทั้งหมดอยู่ในโฟลเดอร์เดียวกัน*
    
### Step 4: สร้าง Artifact Registry repository
ไปที่: 🔗 [console.cloud.google.com/artifacts](https://console.cloud.google.com/artifacts)
1.  คลิก **"Create Repository"**
2.  ตั้งค่าดังนี้:
    * **Name**: `serving-repo`
    * **Format**: `Docker`
    * **Mode**: `Standard`
    * **Location type**: `Region`
    * **Region**: `asia-southeast1` (Singapore)
3.  คลิก **Create**

### Step 5: กำหนดค่าตัวแปร (Environment Variables)
คัดลอกคำสั่งด้านล่างนี้ไปวางใน **Cloud Shell Terminal** เพื่อความสะดวกในการพิมพ์คำสั่งถัดไป (ช่วยลดความผิดพลาดในการพิมพ์ชื่อซ้ำๆ):

```batch
export PROJECT_ID=$(gcloud config get-value project)
export REGION=asia-southeast1           # ต้องตรงกับ Region ใน Artifact Registry
export REPO_NAME=serving-repo           # ชื่อ Repository ที่สร้างใน Step 4
export IMAGE_NAME=serving-api           # ชื่อ Image ที่จะใช้เรียกในระบบ
```

### Step 6: ทำการ Build Image
  ใน Cloud Shell Terminal (ตรวจสอบว่าอยู่ในโฟลเดอร์ที่มีไฟล์ `Dockerfile` โดยใช้คำสั่ง `ls`) ให้รันคำสั่งเพื่อสร้าง Docker Image บนระบบคลาวด์:
  ```batch
  gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} .
```
### Step 7: Deploy the image ไปยัง Cloud Run
รันคำสั่งสุดท้ายใน Cloud Shell Terminal เพื่อนำ Docker Image ที่เรา Build ไว้ขึ้นไปเปิดให้บริการเป็น API บนระบบคลาวด์:

```batch
gcloud run deploy serving-api \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} \
  --platform=managed \
  --region=${REGION} \
  --allow-unauthenticated \
  --port=8080
```
## 🧹 4. การจัดการค่าใช้จ่ายและการลบโปรเจกต์ (Project Cleanup)

เพื่อให้การใช้งานอยู่ในงบประมาณที่จำกัด (หรือฟรี 100% ตามโควต้า) นักศึกษาควรปฏิบัติตามขั้นตอนเหล่านี้อย่างเคร่งครัดเมื่อสิ้นสุดการใช้งานครับ

### 4.1 การปิดบริการชั่วคราว (Pause Service)
วิธีนี้เหมาะสำหรับกรณีที่คุณต้องการหยุดพักการใช้งาน แต่ยังไม่อยากลบโปรเจกต์ทิ้งเพื่อกลับมาทำต่อในภายหลัง

* **หลักการทำงาน**: โดยธรรมชาติของ Cloud Run จะคิดเงินตามการใช้งานจริง (Pay-per-use). หากไม่มีใครส่ง Request เข้ามาประมวลผล ค่าบริการในส่วนของ CPU และ RAM จะเท่ากับ 0 บาททันทีครับ.
* **ข้อควรระวังเรื่องค่าพื้นที่ (Storage)**: แม้จะไม่มีการรันโค้ด แต่ไฟล์ระบบของคุณยังคงถูกเก็บไว้ในคลัง.
    * Google Cloud มีโควต้าพื้นที่จัดเก็บฟรีรวมประมาณ **5GB** (Standard Storage).
    * หาก Image ของคุณมีขนาดเล็กและไม่เกินจำนวนนี้ จะไม่มีการเรียกเก็บเงินครับ.
* **วิธีตรวจสอบ**: สามารถเข้าไปดูพื้นที่ที่ใช้ไปจริงได้ที่เมนู **Artifact Registry**.

---

### 4.2 การลบทรัพยากรทั้งหมด (Full Cleanup)
หากต้องการลบเพื่อไม่ให้มีค่าใช้จ่ายค้างคา 100% ให้ทำตามลำดับความสำคัญดังนี้ครับ:

#### 1️⃣ ลบ Cloud Run Service
* ไปที่หน้า **Cloud Run** ใน Google Cloud Console.
* เลือก Service ที่ชื่อ `serving-api` แล้วกดปุ่ม **Delete**.
* การทำขั้นตอนนี้จะหยุดการทำงานของเซิร์ฟเวอร์และปิด URL การเข้าถึงทันทีครับ.



#### 2️⃣ ลบ Docker Image ใน Artifact Registry (สำคัญที่สุด!) ⚠️
* **จำไว้ว่า**: การลบ Service ในข้อแรก ไม่ได้เป็นการลบไฟล์ Image ทิ้ง. ไฟล์เหล่านี้ยังคงกินพื้นที่จัดเก็บและอาจทำให้เสียเงินได้หากเกินโควต้า.
* ไปที่ **Artifact Registry** -> เข้าไปที่ Repository ชื่อ `serving-repo`.
* เลือก Image ทั้งหมดที่อยู่ในนั้นแล้วกด **Delete**.



#### 3️⃣ ลบไฟล์ขยะใน Cloud Storage
* เข้าไปที่เมนู **Cloud Storage** -> **Buckets**.
* มองหา Bucket ที่มีชื่อขึ้นต้นด้วย `artifacts.[PROJECT_ID].appspot.com` (ซึ่งเป็นไฟล์ชั่วคราวที่เกิดจากขั้นตอนการ Build).
* กดลบ Bucket หรือลบไฟล์ภายใน Bucket นั้นออกให้หมดเพื่อคืนพื้นที่ครับ.

