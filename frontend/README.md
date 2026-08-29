# EngiSummary

**Engineering Drawing Summary Generator**

EngiSummary is a simple and user-friendly web application that converts engineering drawing PDFs into summarized engineering documents.

The application follows a single workflow:

**Upload PDF → Process → Preview Result → Download PDF**

The frontend is designed as a lightweight interface for uploading an engineering drawing, displaying the processing status, previewing the generated PDF, and downloading the final document.

---

## Features

* 📄 Upload engineering drawing PDF
* 🖱️ Drag-and-drop file upload
* ⚙️ Processing progress indicator
* 🤖 AI-based drawing analysis through backend integration
* 📋 Display extracted engineering information
* 📑 Preview processed PDF
* ⬇️ Download generated PDF
* 🔄 Upload another drawing
* 🎨 Clean and professional engineering-style UI
* 🧪 Mock mode for frontend development without a backend

---

## Technology Stack

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| React 18      | Frontend framework                |
| Vite          | Development server and build tool |
| Tailwind CSS  | UI styling                        |
| React Router  | Page navigation                   |
| Axios         | Backend API communication         |
| Lucide React  | Icons                             |
| React Context | State management                  |

---

## Application Workflow

```text
        Upload Engineering PDF
                 ↓
            Upload File
                 ↓
             Analyzing
                 ↓
        Generating Summary
                 ↓
          Process Completed
                 ↓
          Preview Result PDF
                 ↓
           Download PDF
```

---

## Getting Started

### Prerequisites

Make sure you have installed:

* Node.js 18 or higher
* npm
* Git

### Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the frontend directory:

```bash
cd EngiSummary/frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The application will be available at:

```text
http://localhost:5173
```

---

## Mock Mode

The application runs in **mock mode by default**.

Mock mode allows you to test the complete frontend flow without connecting a backend.

It simulates:

* PDF upload
* Processing
* Engineering data extraction
* Summary generation
* PDF result

This is useful for frontend development and demonstrations.

---

## Backend Integration

To connect the frontend with the real backend:

### 1. Create `.env`

Copy:

```text
.env.example
```

to:

```text
.env
```

### 2. Configure environment variables

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_MOCK_MODE=false
```

Replace the API URL with your backend URL.

---

## Backend API

The frontend expects the following REST APIs:

| Method | Endpoint          | Purpose                              |
| ------ | ----------------- | ------------------------------------ |
| POST   | `/api/upload`     | Upload engineering PDF               |
| POST   | `/api/process`    | Process the uploaded drawing         |
| GET    | `/api/result/:id` | Get processed PDF and extracted data |

### Upload

```http
POST /api/upload
```

Accepts:

```text
multipart/form-data
```

Expected response:

```json
{
  "id": "123",
  "filename": "drawing.pdf",
  "size": 245678
}
```

### Process

```http
POST /api/process
```

Request:

```json
{
  "id": "123"
}
```

The backend should analyze the engineering drawing and generate the summary/BOM table.

### Result

```http
GET /api/result/:id
```

Expected response:

```json
{
  "id": "123",
  "pdfUrl": "/files/processed-drawing.pdf",
  "summary": {
    "partNumber": "ENG-4471-B",
    "drawingTitle": "Mounting Plate",
    "material": "Aluminium 6061-T6",
    "quantity": 4,
    "scale": "1:2",
    "revision": "B",
    "toleranceClass": "ISO 2768-m",
    "surfaceFinish": "Ra 3.2",
    "weight": "1.25 kg",
    "drawnBy": "Engineering Team",
    "checkedDate": "2026-08-29"
  }
}
```

---

## Project Structure

```text
EngiSummary/
│
├── src/
│   ├── api/
│   │   └── client.js
│   │
│   ├── context/
│   │   └── DrawingContext.jsx
│   │
│   ├── components/
│   │   ├── Logo.jsx
│   │   ├── TopNav.jsx
│   │   ├── Button.jsx
│   │   ├── UploadDropzone.jsx
│   │   ├── ProcessingSteps.jsx
│   │   ├── TitleBlock.jsx
│   │   └── PDFPreview.jsx
│   │
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── ProcessingPage.jsx
│   │   └── ResultPage.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## Pages

### Home Page

Allows the user to:

* Upload an engineering PDF
* Drag and drop a file
* View file information
* Start processing

### Processing Page

Displays the processing progress:

```text
Uploading
   ↓
Analyzing
   ↓
Generating Summary
   ↓
Completed
```

### Result Page

Displays:

* Processing success message
* Extracted engineering information
* Processed PDF preview
* View PDF option
* Download PDF option
* Upload another drawing option

---

## Summary Information

The frontend currently supports the following extracted fields:

* Part Number
* Drawing Title
* Material
* Quantity
* Scale
* Revision
* Tolerance Class
* Surface Finish
* Weight
* Drawn By
* Checked Date

These fields can be modified in:

```text
src/components/TitleBlock.jsx
```

---

## Frontend Responsibility

The frontend is responsible for:

* PDF selection
* File upload
* Displaying processing status
* Displaying extracted information
* PDF preview
* PDF download
* Backend API communication

The frontend **does not perform PDF analysis**.

The backend is responsible for:

* Reading the engineering drawing
* Extracting engineering information
* Generating the BOM/summary table
* Adding the summary table to the original PDF
* Returning the processed PDF

---

## Build for Production

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

---

## Future Scope

* Support for additional CAD formats such as DXF and DWG
* Improved AI-based engineering drawing analysis
* Automatic BOM generation
* Advanced drawing feature detection
* Engineering drawing validation
* Export to Excel and other formats

---

## License

This project is developed for **academic and industry project purposes**.
