# EngiSummary - Run Commands (शुरू करने के लिए Commands)

## डायरेक्टरी में जाएं (Go to Directory)
```
cd c:\VIT\TY_EDAI\EngiSummary
```

---

## **Option 1: Separate Terminal Windows (आसान तरीका)**

### Terminal 1 - Backend शुरू करें
```bash
cd c:\VIT\TY_EDAI\EngiSummary\backend
venv\Scripts\activate
python run.py
```

Backend चलेगा यहाँ: http://localhost:8000


### Terminal 2 - Frontend शुरू करें
```bash
cd c:\VIT\TY_EDAI\EngiSummary\frontend
npm run dev
```

Frontend चलेगा यहाँ: http://localhost:5173

---

## **Option 2: Single Script (एक command से दोनों चलाएं)**

फाइल बनाएं: `run_all.bat`

```batch
@echo off
echo Starting EngiSummary...

start cmd /k "cd /d c:\VIT\TY_EDAI\EngiSummary\backend && venv\Scripts\activate && python run.py"
timeout /t 3
start cmd /k "cd /d c:\VIT\TY_EDAI\EngiSummary\frontend && npm run dev"

echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
```

फिर यह command चलाएं:
```
c:\VIT\TY_EDAI\EngiSummary\run_all.bat
```

---

## **Option 3: PowerShell से दोनों**

```powershell
# Backend शुरू करें (Background में)
Start-Process powershell -ArgumentList "cd c:\VIT\TY_EDAI\EngiSummary\backend; .\venv\Scripts\activate; python run.py"

# Frontend शुरू करें (Background में)
Start-Process powershell -ArgumentList "cd c:\VIT\TY_EDAI\EngiSummary\frontend; npm run dev"

# Browser खोलें
Start-Process "http://localhost:5173"
```

---

## **Quick Commands (सबसे आसान)**

### Backend के लिए (टर्मिनल 1):
```
cd c:\VIT\TY_EDAI\EngiSummary\backend && venv\Scripts\activate && python run.py
```

### Frontend के लिए (टर्मिनल 2):
```
cd c:\VIT\TY_EDAI\EngiSummary\frontend && npm run dev
```

---

## **URLs खोलें Browser में:**

- **Frontend**: http://localhost:5173
- **Backend Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

---

## **अगर Dependencies नहीं हैं तो:**

### Backend Dependencies Install करें:
```bash
cd c:\VIT\TY_EDAI\EngiSummary\backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Dependencies Install करें:
```bash
cd c:\VIT\TY_EDAI\EngiSummary\frontend
npm install
```

---

## **Process को बंद करने के लिए:**
- Backend Terminal में: `Ctrl + C`
- Frontend Terminal में: `Ctrl + C`

---

## **अगर Port पहले से use हो तो:**

### Backend को दूसरे Port पर चलाएं:
```bash
cd c:\VIT\TY_EDAI\EngiSummary\backend
venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Frontend को दूसरे Port पर चलाएं:
```bash
cd c:\VIT\TY_EDAI\EngiSummary\frontend
npm run dev -- --port 5174
```

---

## **Recommended (सबसे बेहतर तरीका):**

1. एक PowerShell खोलें
2. यह paste करें:
```powershell
cd c:\VIT\TY_EDAI\EngiSummary\backend
.\venv\Scripts\activate
python run.py
```

3. दूसरा PowerShell खोलें
4. यह paste करें:
```powershell
cd c:\VIT\TY_EDAI\EngiSummary\frontend
npm run dev
```

5. Browser में जाएं: http://localhost:5173

---

**बस! 🚀 App चल जाएगा!**
