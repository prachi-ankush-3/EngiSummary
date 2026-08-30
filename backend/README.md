# EngiSummary Backend

## Overview

EngiSummary is a comprehensive backend system for **Engineering Drawing Data Extraction and Summary Generation**. It processes PDF engineering drawings, extracts Bill of Materials (BOM) information using AI vision, calculates component weights, and generates professional summary PDFs.

### Key Features

- **PDF Upload & Processing**: Accept engineering drawing PDFs up to 25MB
- **AI-Powered BOM Extraction**: Uses Google Gemini Vision to extract BOM data
- **Component Identification**: Automatically classify component types (Pipe, Plate, Angle, etc.)
- **Weight Calculation**: Deterministic weight calculations using engineering formulas
- **Professional PDF Generation**: ReportLab-based summary table PDF generation
- **Job Management**: In-memory job tracking with status updates
- **CORS Support**: Full cross-origin support for frontend integration
- **RESTful API**: Complete API documentation via Swagger/OpenAPI

## Architecture

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── upload.py            # PDF upload endpoint
│   │       ├── processing.py        # Processing endpoint
│   │       ├── status.py            # Status check endpoint
│   │       └── download.py          # Download & result endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration & settings
│   │   └── logging_config.py        # Logging setup
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bom.py                   # BOM and Summary models
│   │   ├── component.py             # Component type models
│   │   └── response.py              # API response models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_service.py           # PDF loading & rendering
│   │   ├── image_service.py         # Image processing
│   │   ├── gemini_service.py        # Gemini Vision integration
│   │   ├── bom_extractor.py         # BOM extraction pipeline
│   │   ├── component_parser.py      # Component identification
│   │   ├── weight_calculator.py     # Weight calculation engine
│   │   ├── summary_service.py       # Summary generation
│   │   ├── output_pdf_service.py    # PDF output generation
│   │   └── job_manager.py           # Job status management
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py            # File validation utilities
│   │   ├── units.py                 # Unit conversion utilities
│   │   └── file_utils.py            # File handling utilities
│   │
│   └── temp/                        # Temporary file storage
│
├── uploads/                         # Uploaded PDF storage
├── outputs/                         # Generated PDF storage
├── tests/                           # Test suite
│   ├── test_upload.py
│   ├── test_bom_extraction.py
│   ├── test_weight_calculation.py
│   └── test_summary_generation.py
│
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
├── run.py                          # Application entry point
└── README.md                       # This file
```

## Installation

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Google Gemini API key

### Step 1: Clone Repository

```bash
cd EngiSummary
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 4: Configure Environment

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create `.env` file from template:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

3. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
FRONTEND_URL=http://localhost:3000
```

## Running the Backend

### Start the Application

```bash
# From backend directory
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### 1. Upload PDF

**Endpoint**: `POST /api/upload`

Upload an engineering drawing PDF for processing.

**Request**:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@drawing.pdf"
```

**Response**:
```json
{
    "success": true,
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "drawing.pdf",
    "message": "File uploaded successfully"
}
```

### 2. Process Drawing

**Endpoint**: `POST /api/process/{job_id}`

Start processing the uploaded PDF.

**Request**:
```bash
curl -X POST "http://localhost:8000/api/process/550e8400-e29b-41d4-a716-446655440000"
```

**Response**:
```json
{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "progress": 100,
    "stage": "Processing complete"
}
```

### 3. Get Processing Status

**Endpoint**: `GET /api/status/{job_id}`

Check the current status of a processing job.

**Request**:
```bash
curl "http://localhost:8000/api/status/550e8400-e29b-41d4-a716-446655440000"
```

**Response**:
```json
{
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "progress": 60,
    "stage": "Calculating component weights"
}
```

Possible statuses:
- `uploaded`: File uploaded successfully
- `processing`: Currently processing
- `completed`: Processing complete
- `failed`: Processing failed

### 4. Download Summary PDF

**Endpoint**: `GET /api/download/{job_id}`

Download the generated summary PDF.

**Request**:
```bash
curl -o summary.pdf "http://localhost:8000/api/download/550e8400-e29b-41d4-a716-446655440000"
```

### 5. Get Summary Result

**Endpoint**: `GET /api/result/{job_id}`

Get the extracted BOM and calculated summary as JSON.

**Response**:
```json
{
    "success": true,
    "data": {
        "job_id": "550e8400-e29b-41d4-a716-446655440000",
        "summary": [
            {
                "part_no": "1",
                "description": "PIPE 100 NB",
                "material": "STEEL",
                "quantity": 10,
                "unit": "M",
                "weight_per_unit": 16.1,
                "total_weight": 161.0,
                "calculation_status": "calculated"
            }
        ],
        "grand_total_weight": 161.0
    }
}
```

## Processing Pipeline

1. **PDF Upload** → `POST /api/upload`
   - File validation (PDF type, size)
   - Generate unique job ID
   - Save to uploads directory

2. **BOM Extraction** → `POST /api/process/{job_id}`
   - Load and render PDF pages
   - Detect BOM-containing pages
   - Send images to Gemini Vision API

3. **AI Interpretation**
   - Gemini extracts structured BOM JSON
   - Validate against Pydantic schema

4. **Component Processing**
   - Identify component types
   - Normalize descriptions
   - Parse dimensions

5. **Weight Calculation**
   - Calculate weight per unit using formulas
   - Calculate total weight based on quantity
   - Track calculation method and status

6. **Summary Generation**
   - Compile extracted and calculated data
   - Calculate grand total weight

7. **PDF Generation**
   - Create professional summary table
   - Format with ReportLab
   - Save to outputs directory

8. **Result Delivery**
   - `GET /api/download/{job_id}` → PDF file
   - `GET /api/result/{job_id}` → JSON data

## Weight Calculation

The weight calculator uses deterministic formulas based on component type:

### PIPE
Formula: W = ρ × π/4 × (OD² - ID²) × L

Requirements: Outer diameter, inner diameter, length

### PLATE
Formula: W = L × W × T × ρ

Requirements: Length, width, thickness

### ANGLE
Formula: W = t × (2a - t) × L × ρ

Requirements: Leg size, thickness, length

Uses standard section masses from reference tables when available.

### UB/I-BEAM
Uses standard section mass per meter from section designation.

Requirements: Section designation (e.g., "UB 406x178x67")

### Other Components
- **Flat Bar**: W = W × T × L × ρ
- **Round Bar**: W = π × (D/2)² × L × ρ
- **Square Bar**: W = S² × L × ρ

All dimensions converted to meters (SI units).

**Default Steel Density**: 7850 kg/m³ (configurable via .env)

## Component Types

The system automatically identifies these component types:

- **PIPE**: Circular piping (with nominal bore)
- **PLATE**: Flat rectangular sheets
- **ANGLE**: L-section angles
- **CHANNEL**: C-section channels
- **I_BEAM**: I-beam sections
- **UB**: Universal beam sections
- **FLAT_BAR**: Rectangular bars
- **ROUND_BAR**: Circular rods
- **SQUARE_BAR**: Square-sectioned bars
- **BRACKET**: Mounting brackets
- **GUSSET**: Stiffening plates
- **OTHER**: Unclassified components

## Gemini Vision Integration

### Setup

1. Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set in `.env`:
```
GEMINI_API_KEY=sk-...
GEMINI_MODEL=gemini-2.0-flash
```

### BOM Extraction Prompt

The system uses a carefully crafted prompt that instructs Gemini to:

- Read ONLY visible information
- NOT invent missing dimensions
- Preserve original descriptions and part numbers
- Return strict JSON format
- Flag uncertain information with low confidence

Example extraction:
```json
{
    "bom": [
        {
            "part_no": "1",
            "description": "PIPE 100 NB",
            "material": "STEEL",
            "dimensions": {"nominal_bore": 100, "length": 4.5},
            "quantity": 10,
            "unit": "M"
        }
    ]
}
```

### Fallback Handling

If Gemini fails:
1. Error is logged
2. Job is marked as failed
3. Clear error message is returned
4. No synthetic data is generated

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_weight_calculation.py

# Run with coverage
pytest tests/ --cov=app
```

### Test Coverage

- **Upload Tests**: File validation, PDF verification
- **BOM Extraction Tests**: Component identification, description parsing
- **Weight Calculation Tests**: Formula validation, edge cases
- **Summary Generation Tests**: Data aggregation, total calculations

## Configuration

### Environment Variables

```
# Gemini Configuration
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.0-flash

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# File Size Limit (MB)
MAX_FILE_SIZE_MB=25

# Directories
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs

# Material Properties
STEEL_DENSITY=7850

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### Directory Structure

The backend automatically creates:
- `uploads/` - Stores uploaded PDFs
- `outputs/` - Stores generated summary PDFs
- `app/temp/` - Temporary rendering files

## Frontend Integration

The backend is designed to integrate with an existing frontend:

### CORS Configuration

CORS is enabled for:
- Frontend URL (from .env)
- `http://localhost:3000`
- `http://localhost:5000`

### Frontend Workflow

1. User uploads PDF via frontend
2. Frontend calls `POST /api/upload`
3. Frontend receives `job_id`
4. Frontend polls `GET /api/status/{job_id}`
5. When status is "completed", frontend calls `GET /api/download/{job_id}`

Example frontend code:
```javascript
// Upload
const formData = new FormData();
formData.append('file', pdfFile);
const uploadResp = await fetch('http://localhost:8000/api/upload', {
    method: 'POST',
    body: formData
});
const { job_id } = await uploadResp.json();

// Process
const procResp = await fetch(`http://localhost:8000/api/process/${job_id}`, {
    method: 'POST'
});

// Poll status
const statusResp = await fetch(`http://localhost:8000/api/status/${job_id}`);
const status = await statusResp.json();

// Download when complete
if (status.status === 'completed') {
    window.location.href = `http://localhost:8000/api/download/${job_id}`;
}
```

## Logging

Logs are written to:
- **Console**: Real-time application output
- **app.log**: Detailed logging file

Log levels (configurable via .env):
- `DEBUG`: Detailed diagnostic information
- `INFO`: Confirmation of proper operation
- `WARNING`: Something unexpected occurred
- `ERROR`: A serious problem
- `CRITICAL`: A very serious problem

Example logs:
```
2024-01-15 10:30:45 - app - INFO - Successfully uploaded PDF for job abc123
2024-01-15 10:31:02 - app - INFO - Starting PDF processing for job abc123
2024-01-15 10:31:15 - app - INFO - Extracted BOM with 5 items
2024-01-15 10:31:32 - app - INFO - Generated summary for job abc123
2024-01-15 10:31:45 - app - INFO - Successfully generated PDF: outputs/drawing_summary_abc123.pdf
```

## Error Handling

The system handles errors gracefully:

### Invalid PDF
```json
{
    "success": false,
    "error": "Invalid PDF file"
}
```

### No BOM Detected
```json
{
    "success": false,
    "error": "BOM could not be detected in the uploaded PDF"
}
```

### Insufficient Data
Items with incomplete dimensions are marked for manual review:
```json
{
    "part_no": "9",
    "description": "BRACKET-1",
    "calculation_status": "insufficient_data",
    "requires_review": true
}
```

## Performance Considerations

- PDF rendering: 2-3 seconds per page
- Gemini API call: 5-10 seconds
- Weight calculations: <1 second
- PDF generation: <2 seconds

**Total typical processing time**: 20-30 seconds per drawing

## Known Limitations

1. **Pipe Diameter Mapping**: Standard pipe dimensions must be provided or calculated from schedule data
2. **Custom Components**: Non-standard fabricated parts may require manual weight entry
3. **Multiple BOMs**: Only first detected BOM is processed
4. **Text-Only PDFs**: Requires OCR fallback for scanned documents
5. **Large Files**: Processing time increases with PDF size

## Deployment

### Production Deployment

For production deployment:

1. Set `DEBUG=False` in .env
2. Use production-grade ASGI server:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```
3. Configure proper logging
4. Use proper PDF storage (not temporary)
5. Add database for job persistence
6. Add job queue (Redis + Celery) for async processing

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Gemini API Key Error
- Check that `GEMINI_API_KEY` is correctly set in .env
- Verify API key is valid and has Generative AI access

### PDF Upload Fails
- Check file is valid PDF (starts with `%PDF`)
- Verify file size is under 25MB
- Check write permissions in `uploads/` directory

### No BOM Detected
- Verify PDF contains a table or BOM information
- Check that text is not rasterized/scanned
- Review PDF with Gemini API docs limitations

### Weight Calculations Show Zero
- Verify dimensions are provided in BOM
- Check units are recognized (mm, cm, m, in)
- Review calculation method in response

## Support & Documentation

- **API Docs**: http://localhost:8000/docs
- **Code Comments**: Extensive inline documentation
- **Test Examples**: See `tests/` directory

## License

This project is part of EngiSummary system.

---

**Last Updated**: 2024  
**Version**: 1.0.0
