# EngiSummary Backend - Quick Reference

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Gemini API
```bash
copy .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

### Step 3: Run Backend
```bash
python run.py
```

### Step 4: Test
```bash
# Visit API docs: http://localhost:8000/docs
# Or run tests: pytest tests/
```

---

## 📡 API Usage Examples

### Upload PDF
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@drawing.pdf"
```
Response: `{"success": true, "job_id": "abc-123", ...}`

### Process Drawing
```bash
curl -X POST "http://localhost:8000/api/process/abc-123"
```
Response: `{"status": "processing", "progress": 25, ...}`

### Check Status
```bash
curl "http://localhost:8000/api/status/abc-123"
```
Response: `{"status": "completed", "progress": 100, ...}`

### Download PDF
```bash
curl -o summary.pdf "http://localhost:8000/api/download/abc-123"
```

### Get JSON Results
```bash
curl "http://localhost:8000/api/result/abc-123"
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── api/routes/          # API endpoints
│   ├── services/            # Business logic
│   ├── models/              # Data models
│   ├── core/                # Config, logging
│   └── utils/               # Helpers
├── tests/                   # Test suite
├── uploads/                 # Uploaded PDFs
├── outputs/                 # Generated PDFs
├── requirements.txt         # Dependencies
├── run.py                   # Entry point
└── .env                     # Configuration
```

---

## 🔧 Configuration

Edit `.env`:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
FRONTEND_URL=http://localhost:3000
MAX_FILE_SIZE_MB=25
STEEL_DENSITY=7850
DEBUG=True
LOG_LEVEL=INFO
```

---

## 📊 Weight Calculation Formulas

| Component | Formula | Required |
|-----------|---------|----------|
| **PLATE** | V = L × W × T | L, W, T |
| **ANGLE** | A = t × (2a - t) | Leg, Thickness, L |
| **PIPE** | A = π/4 × (OD² - ID²) | OD, ID, L |
| **ROUND** | A = π × r² | Diameter, L |
| **SQUARE** | A = s² | Side, L |
| **UB/BEAM** | Uses standard mass/m | Section designation |

Weight: W = Area × Density × Length

---

## 🧪 Testing

```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_weight_calculation.py

# With coverage
pytest tests/ --cov=app

# Verbose
pytest tests/ -v
```

---

## 📝 Processing Stages

```
uploaded
  ↓ (POST /process)
processing → "Extracting BOM from PDF"
  ↓
  → "Calculating weights"
  ↓
  → "Generating output PDF"
  ↓
completed (progress=100)
  ↓
Output available at /download and /result
```

---

## ⚠️ Common Issues

### "Gemini API Key not configured"
- Add GEMINI_API_KEY to .env
- Restart application

### "No BOM could be detected"
- Ensure PDF contains BOM table/information
- Check if text is rasterized

### "File not a valid PDF"
- Verify file starts with `%PDF`
- Check file isn't corrupted

### Port 8000 already in use
```bash
uvicorn app.main:app --port 8001
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application |
| `app/services/weight_calculator.py` | Weight formulas |
| `app/services/gemini_service.py` | AI integration |
| `app/services/output_pdf_service.py` | PDF generation |
| `app/api/routes/` | API endpoints |
| `tests/` | Test suite |

---

## 🔗 Links

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Info**: http://localhost:8000/

---

## 🎯 Component Types Supported

Pipe · Plate · Angle · Channel · I-Beam · UB · Flat Bar · Round Bar · Square Bar · Bracket · Gusset · Other

---

## 💾 Data Storage

- **Uploads**: `uploads/{job_id}/`
- **Outputs**: `outputs/drawing_summary_{job_id}.pdf`
- **Temp Files**: `app/temp/{job_id}/`
- **Logs**: `app.log`

---

## 🔐 Security

- ✅ File validation (PDF only, max 25MB)
- ✅ Safe filename generation
- ✅ No hardcoded secrets
- ✅ CORS configured
- ✅ Path traversal prevention
- ✅ Input validation (Pydantic)

---

## 📊 Typical Response Times

| Operation | Time |
|-----------|------|
| PDF Upload | <1 sec |
| PDF Rendering | 2-3 sec |
| Gemini API | 5-10 sec |
| Weight Calc | <1 sec |
| PDF Gen | <2 sec |
| **Total** | **20-30 sec** |

---

## 🚢 For Production

1. Set `DEBUG=False`
2. Use Gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
3. Add database for persistence
4. Use Redis for job queue
5. Configure logging properly
6. Set up monitoring
7. Use HTTPS

---

## 📞 Support

See `README.md` for complete documentation.

Version: **1.0.0** | Ready: **✅**
