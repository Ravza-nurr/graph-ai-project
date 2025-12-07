# API Design Documentation

## Base URL

```
Development: http://localhost:8000
Production: TBD
```

## Authentication

Currently, no authentication is required. Future versions will implement JWT-based authentication.

## Headers

### Request Headers
```
Content-Type: application/json (for JSON payloads)
Content-Type: multipart/form-data (for file uploads)
```

### Response Headers
```
Content-Type: application/json
```

## Endpoints

### 1. Health Check

#### GET /

Check if the API is running.

**Response 200 OK:**
```json
{
  "message": "Graph AI System API",
  "version": "1.0.0",
  "status": "running",
  "ai_studio_available": false
}
```

---

### 2. Detailed Health Check

#### GET /health

Get detailed service status.

**Response 200 OK:**
```json
{
  "status": "healthy",
  "services": {
    "file_handler": "ok",
    "ai_studio": "configured" | "not_configured"
  }
}
```

---

### 3. Upload File

#### POST /upload

Upload a data file for analysis and chart generation.

**Request:**
- Content-Type: multipart/form-data
- Body: Form data with `file` field

**Example:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data.csv"
```

**Response 200 OK:**
```json
{
  "success": true,
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "original_name": "data.csv",
    "saved_name": "550e8400-e29b-41d4-a716-446655440000.csv",
    "file_path": "data/uploads/550e8400-e29b-41d4-a716-446655440000.csv",
    "file_type": "csv",
    "size_bytes": 12345,
    "extension": "csv",
    "columns": ["Column1", "Column2", "Column3"],
    "num_rows": 100,
    "num_columns": 3,
    "dtypes": {
      "Column1": "int64",
      "Column2": "float64",
      "Column3": "object"
    },
    "numeric_columns": ["Column1", "Column2"],
    "categorical_columns": ["Column3"],
    "sample_data": [
      {"Column1": 1, "Column2": 2.5, "Column3": "A"},
      {"Column1": 2, "Column2": 3.5, "Column3": "B"}
    ],
    "ai_recommendations": {
      "available": true,
      "recommendations": [
        {
          "type": "scatter",
          "columns": ["Column1", "Column2"],
          "reason": "Good for correlations"
        }
      ]
    }
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "File type .txt not allowed"
}
```

400 Bad Request:
```json
{
  "detail": "File too large. Max size: 10.0MB"
}
```

500 Internal Server Error:
```json
{
  "detail": "Upload failed: [error message]"
}
```

---

### 4. Get File Information

#### GET /file/{file_id}

Retrieve metadata about an uploaded file.

**Parameters:**
- `file_id` (path): UUID of the uploaded file

**Response 200 OK:**
```json
{
  "original_name": "data.csv",
  "columns": ["Column1", "Column2"],
  "num_rows": 100,
  ...
}
```

**Error 404:**
```json
{
  "detail": "File not found"
}
```

---

### 5. Generate Chart

#### POST /generate-chart

Generate a chart from uploaded data.

**Request Body:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "chart_type": "bar",
  "x_column": "Category",
  "y_columns": ["Value"],
  "color_column": "Group",
  "size_column": null,
  "title": "My Custom Title"
}
```

**Parameters:**
- `file_id` (required): UUID from upload response
- `chart_type` (required): One of: bar, line, scatter, histogram, boxplot, density, violin, heatmap, area, pie
- `x_column` (optional): Column for x-axis
- `y_columns` (optional): Array of columns for y-axis
- `color_column` (optional): Column to color by (scatter plots)
- `size_column` (optional): Column to size by (scatter plots)
- `title` (optional): Custom chart title

**Response 200 OK:**
```json
{
  "success": true,
  "chart_type": "bar",
  "chart_url": "/charts/abc123.png",
  "local_path": "output/abc123.png",
  "caption": "Bar chart showing Value by Category demonstrates the distribution across different categories.",
  "columns_used": ["Category", "Value"]
}
```

**Error Responses:**

404 Not Found:
```json
{
  "detail": "File not found"
}
```

400 Bad Request:
```json
{
  "detail": "Only CSV files are supported for chart generation"
}
```

400 Bad Request:
```json
{
  "detail": "x_column required for bar chart"
}
```

400 Bad Request:
```json
{
  "detail": "Chart type 'histogram' not yet implemented. Available: bar, line, scatter"
}
```

500 Internal Server Error:
```json
{
  "detail": "Chart generation failed: [error message]"
}
```

---

### 6. Get Chart Image

#### GET /charts/{filename}

Retrieve a generated chart image.

**Parameters:**
- `filename` (path): Filename from chart_url in generate-chart response

**Response 200 OK:**
- Content-Type: image/png
- Body: PNG image binary data

**Error 404:**
```json
{
  "detail": "Chart not found"
}
```

---

### 7. Get Available Chart Types

#### GET /chart-types

List all chart types and their implementation status.

**Response 200 OK:**
```json
{
  "available": [
    {
      "id": "bar",
      "name": "Bar Chart",
      "status": "implemented"
    },
    {
      "id": "line",
      "name": "Line Chart",
      "status": "implemented"
    },
    {
      "id": "scatter",
      "name": "Scatter Plot",
      "status": "implemented"
    },
    {
      "id": "histogram",
      "name": "Histogram",
      "status": "planned"
    }
  ]
}
```

---

### 8. Analyze Dataset

#### POST /analyze-dataset

Get AI analysis of a dataset.

**Request Body:**
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response 200 OK (with AI configured):**
```json
{
  "available": true,
  "analysis": "This dataset contains passenger information...",
  "insights": [
    "The dataset has 891 rows and 12 columns",
    "Age column has missing values",
    "Strong correlation between Fare and Pclass"
  ]
}
```

**Response 200 OK (without AI):**
```json
{
  "available": false,
  "message": "AI Studio not configured. Set GOOGLE_AI_STUDIO_API_KEY environment variable."
}
```

**Error Responses:**

404 Not Found:
```json
{
  "detail": "File not found"
}
```

400 Bad Request:
```json
{
  "detail": "Only CSV files can be analyzed"
}
```

---

## Data Models

### ChartRequest

```typescript
interface ChartRequest {
  file_id: string;           // UUID
  chart_type: string;        // bar|line|scatter|histogram|...
  x_column?: string;         // Required for some charts
  y_columns?: string[];      // Required for some charts
  color_column?: string;     // Optional
  size_column?: string;      // Optional
  title?: string;            // Optional
}
```

### FileMetadata

```typescript
interface FileMetadata {
  original_name: string;
  saved_name: string;
  file_path: string;
  file_type: string;         // csv|image|audio
  size_bytes: number;
  extension: string;
  columns?: string[];        // For CSV files
  num_rows?: number;         // For CSV files
  num_columns?: number;      // For CSV files
  dtypes?: Record<string, string>;
  numeric_columns?: string[];
  categorical_columns?: string[];
  sample_data?: any[];
  ai_recommendations?: AIRecommendations;
}
```

### AIRecommendations

```typescript
interface AIRecommendations {
  available: boolean;
  recommendations?: ChartRecommendation[];
  explanation?: string;
}

interface ChartRecommendation {
  type: string;              // Chart type ID
  columns?: string[];        // Suggested columns
  reason: string;            // Why this chart is recommended
}
```

## Error Handling

All errors follow this structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request (validation failed)
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Not currently implemented. Future versions will include:
- 100 requests per minute per IP
- 10 file uploads per hour per IP

## CORS Configuration

Currently configured to allow all origins for development:
```python
allow_origins=["*"]
```

Production should restrict to specific domains:
```python
allow_origins=["https://yourdomain.com"]
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### Complete Workflow

```bash
# 1. Upload a file
RESPONSE=$(curl -X POST http://localhost:8000/upload \
  -F "file=@titanic.csv")
echo $RESPONSE

FILE_ID=$(echo $RESPONSE | jq -r '.file_id')

# 2. Generate a bar chart
curl -X POST http://localhost:8000/generate-chart \
  -H "Content-Type: application/json" \
  -d "{
    \"file_id\": \"$FILE_ID\",
    \"chart_type\": \"bar\",
    \"x_column\": \"Pclass\",
    \"y_columns\": [\"Survived\"]
  }"

# 3. Get the chart image
CHART_URL=$(curl -X POST http://localhost:8000/generate-chart \
  -H "Content-Type: application/json" \
  -d "{
    \"file_id\": \"$FILE_ID\",
    \"chart_type\": \"bar\",
    \"x_column\": \"Pclass\"
  }" | jq -r '.chart_url')

curl http://localhost:8000$CHART_URL -o chart.png
```

### JavaScript/Axios Example

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// Upload file
const formData = new FormData();
formData.append('file', fileBlob, 'data.csv');

const uploadResponse = await axios.post(
  `${API_BASE}/upload`,
  formData
);

const fileId = uploadResponse.data.file_id;

// Generate chart
const chartResponse = await axios.post(
  `${API_BASE}/generate-chart`,
  {
    file_id: fileId,
    chart_type: 'scatter',
    x_column: 'Age',
    y_columns: ['Fare'],
    color_column: 'Sex'
  }
);

const chartUrl = `${API_BASE}${chartResponse.data.chart_url}`;
```

## Versioning

Current version: v1.0.0

Future API versions will use URL versioning:
```
/api/v1/upload
/api/v2/upload
```

## Changelog

### v1.0.0 (Week 1)
- Initial release
- File upload endpoint
- 3 chart types (bar, line, scatter)
- Google AI Studio integration
- Chart download
