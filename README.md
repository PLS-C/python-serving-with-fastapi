*Read this in other languages: [🇹🇭 ภาษาไทย](README_th.md)*

# 🚀 python-serving-with-fastapi

This project is built with Python and FastAPI to provide mathematical calculations and signal processing services to external programs such as **LabVIEW**, web applications, or other engineering software.

## 📌 Project Objectives
* Learn how to turn a Python script into a ready-to-use API Service.
* Practice using **Docker** to manage environments so the code runs consistently anywhere.
* Understand the basics of transmitting data in **JSON** format between different programming languages.
* Lay the foundation for Model Serving in future Deep Learning tasks.

---

## 📂 1. Preparation and Downloading Files
1.  **Download the project**: 
    * Click the green **"<> Code"** button at the top, select **Download ZIP**, and extract the files.
    * Or use the Git command: `git clone https://github.com/PLS-C/python-serving-with-fastapi.git`
2.  **Required Software**:
    * [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for local testing)
    * [LabVIEW](https://www.ni.com/th-th/support/downloads/software-products/download.labview.html)

---

## 🛠️ 2. Example 1: Testing on Docker Desktop (Local)
This method is ideal for developing and editing code on your local machine.

1.  **Open Terminal/PowerShell**: Navigate to the project folder.
2.  **Build Docker Image**: Create the container image for running our code.
    ```bash
    docker build -t py-serving-app .
    ```
3.  **Run Container (Developer Mode)**: Run the code by binding the local folder to Docker for live code editing.
    ```powershell
    docker run -d --name py-serving-container -p 8080:8080 -v "${PWD}:/workspace" py-serving-app uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    ```
    * *Note: The `-v` command mounts the `app` folder, and `--reload` automatically restarts the server when files are saved. `${PWD}` is the path to your current directory in Terminal/PowerShell.*
4.  **Check Status**: Open your browser and go to `http://localhost:8080/docs` to test the API via the Swagger UI.

---

## ☁️ 3. Example 2: Testing on Google Cloud Run (Step-by-Step)

This method deploys the project to the cloud, allowing external programs (like LabVIEW on another machine) to access it over the internet using the **Cloud Shell** tool in your web browser.

### ✅ Prerequisites
- **Google Account**: A standard Gmail account.
- **Google Cloud Console**: Access it at [console.cloud.google.com](https://console.cloud.google.com).
- **Billing**: You must enable billing for the project (to verify your identity for the free tier quota).

---

### Step 1: Select or Create a Project
1. Go to the Google Cloud Console.
2. Click the project drop-down menu at the top and click **"New Project"**.
3. Name your project (e.g., `python-serving-project`) and note down your **Project ID**.

### Step 2: Enable Required APIs
Go to **Navigation Menu > APIs & Services > Library**, then search for and **"Enable"** the following 3 services:
1.  ✅ **Cloud Run API** (Cloud Run Admin API)
2.  ✅ **Artifact Registry API**
3.  ✅ **Cloud Build API**
*Make sure the status for all three shows as "Enabled".*

### Step 3: Upload Code to Cloud Shell Editor
1. Click the **Cloud Shell** icon (Terminal icon `>_`) at the top right of the screen.
2. When the terminal window appears, click the **"Open Editor"** button.
3. Create a project folder in the terminal using these commands:
   ```bash
   mkdir python-serving-app
   cd python-serving-app
   ```
4.  **Upload the files**: 
  * Right-click the `python-serving-app` folder in the Editor and select **Upload Files**.
  * Select these 3 files from your computer: `main.py`, `Dockerfile`, and `requirements.txt`.
  * *Ensure all files are inside the same folder.*
    
### Step 4: Create an Artifact Registry Repository
Go to: 🔗 [console.cloud.google.com/artifacts](https://console.cloud.google.com/artifacts)
1.  Click **"Create Repository"**.
2.  Configure the settings as follows:
    * **Name**: `serving-repo`
    * **Format**: `Docker`
    * **Mode**: `Standard`
    * **Location type**: `Region`
    * **Region**: `asia-southeast1` (Singapore)
3.  Click **Create**.

### Step 5: Set Environment Variables
Copy and paste the commands below into your **Cloud Shell Terminal** to make the next steps easier (this prevents typos when repeating names):

```batch
export PROJECT_ID=$(gcloud config get-value project)
export REGION=asia-southeast1           # Must match the Region in Artifact Registry
export REPO_NAME=serving-repo           # The Repository name created in Step 4
export IMAGE_NAME=serving-api           # The Image name to be used
```

### Step 6: Build the Image
In the Cloud Shell Terminal (ensure you are in the folder containing the `Dockerfile` using the `ls` command), run the following command to build the Docker image on the cloud:
```batch
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} .
```

### Step 7: Deploy the Image to Cloud Run
Run this final command in the Cloud Shell Terminal to deploy the built Docker image and serve it as an API on the cloud:

```batch
gcloud run deploy serving-api \
  --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} \
  --platform=managed \
  --region=${REGION} \
  --allow-unauthenticated \
  --port=8080
```

## 🧹 4. Cost Management and Project Cleanup

To keep your usage within budget (or 100% free under the quota), you should strictly follow these steps when you are done testing.

### 4.1 Pausing the Service Temporarily
This method is suitable if you want to take a break but don't want to delete the project, allowing you to resume later.

* **How it works**: Cloud Run operates on a Pay-per-use basis. If no requests are being processed, the CPU and RAM costs drop to $0 immediately.
* **Storage Warning**: Even when the code isn't running, your system files are still stored in the registry.
    * Google Cloud provides a free storage quota of approximately **5GB** (Standard Storage).
    * If your images are small and do not exceed this limit, you will not be charged.
* **How to check**: You can view your actual storage usage in the **Artifact Registry** menu.

---

### 4.2 Full Cleanup (Delete All Resources)
If you want to completely remove everything to ensure absolutely zero leftover costs, follow these steps in order of importance:

#### 1️⃣ Delete Cloud Run Service
* Go to the **Cloud Run** page in the Google Cloud Console.
* Select the service named `serving-api` and click **Delete**.
* This step immediately stops the server and disables the access URL.

#### 2️⃣ Delete Docker Images in Artifact Registry (Most Important!) ⚠️
* **Remember**: Deleting the service in the first step does *not* delete the image files. These files continue to consume storage space and may incur costs if they exceed the free quota.
* Go to **Artifact Registry** -> click on the repository named `serving-repo`.
* Select all images inside and click **Delete**.

#### 3️⃣ Delete Temp Files in Cloud Storage
* Go to the **Cloud Storage** -> **Buckets** menu.
* Look for the bucket starting with `artifacts.[PROJECT_ID].appspot.com` (these are temporary files generated during the build process).
* Delete this bucket or empty all files inside it to free up space.
