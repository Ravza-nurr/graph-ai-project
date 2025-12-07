# System Architecture

## Overview

The Graph AI System is a three-tier web application that combines data visualization, machine learning, and modern web technologies to provide an intelligent chart generation platform.

```
┌─────────────────┐
│   React Frontend│  (Port 3000)
│   (Vite + React)│
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  FastAPI Backend│  (Port 8000)
│                 │
├─────────────────┤
│ Chart Generators│
│                 │
├─────────────────┤
│ File Handler    │
│                 │
├─────────────────┤
│  AI Client      │──────► Google AI Studio
└─────────────────┘         (Gemini API)
```

## Components

### 1. Frontend Layer (React + Vite)

**Technology**: React 18.2, Vite 5.0

**Responsibilities**:
- User interface and interaction
- File upload handling
- Chart display and download
- API communication

**Key Components**:

#### App.jsx
Main orchestrator component that manages application state:
- File upload data
- Chart generation data
- Loading states
- Error handling

#### FileUpload Component
```
┌─────────────────────────────┐
│       File Upload UI        │
├─────────────────────────────┤
│   Drag & Drop Zone          │
│   File Validation           │
│   Upload Progress           │
└──────────┬──────────────────┘
           │
           ▼
   POST /upload (API)
```

#### ChartSelector Component
```
┌─────────────────────────────┐
│     Chart Selector UI       │
├─────────────────────────────┤
│  AI Recommendations         │
│  Chart Type Dropdown        │
│  Column Selection           │
│  Generate Button            │
└──────────┬──────────────────┘
           │
           ▼
  POST /generate-chart (API)
```

#### ChartDisplay Component
```
┌─────────────────────────────┐
│     Chart Display UI        │
├─────────────────────────────┤
│  Loading State              │
│  Error State                │
│  Chart Image                │
│  AI Caption                 │
│  Download Button            │
└─────────────────────────────┘
```

### 2. Backend Layer (FastAPI)

**Technology**: FastAPI 0.109, Python 3.9+

**Responsibilities**:
- RESTful API endpoints
- Request validation
- File processing
- Chart generation coordination
- AI integration

**Architecture Pattern**: Layered Architecture

```
┌──────────────────────────────┐
│      API Layer (app.py)      │
│  - Route handlers            │
│  - Request/Response models   │
│  - CORS middleware           │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│    Business Logic Layer      │
│  - Chart generation logic    │
│  - File validation           │
│  - AI recommendation logic   │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│     Utility Layer            │
│  - FileHandler               │
│  - AIStudioClient           │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│   Chart Generator Layer      │
│  - bar.py                    │
│  - line.py                   │
│  - scatter.py                │
│  - (7 more planned)          │
└──────────────────────────────┘
```

### 3. Chart Generation Engine

**Technology**: Matplotlib, Seaborn, Plotly, Pandas

**Design Pattern**: Strategy Pattern

Each chart type is implemented as a separate module with a consistent interface:

```python
def generate_CHARTTYPE(
    df: pd.DataFrame,
    parameters: dict,
    output_path: str,
    **kwargs
) -> str:
    # 1. Data validation
    # 2. Chart generation
    # 3. Styling
    # 4. Save to file
    return output_path
```

**Chart Styling Standards**:
- DPI: 300 (high quality)
- Figure size: 10x6 or 12x6 inches
- Color palette: Professional blues and purples
- Grid: Light, dashed
- Labels: Bold, 12pt
- Title: Bold, 14pt

### 4. Google AI Studio Integration

**Technology**: google-generativeai SDK, Gemini Pro model

**Flow**:
```
User uploads CSV
       │
       ▼
Extract metadata
       │
       ▼
Send to Gemini API
       │
       ▼
Parse AI response
       │
       ▼
Return recommendations
```

**Prompts**:

1. **Dataset Analysis**:
   - Input: Column names, types, sample data
   - Output: Insights about the dataset

2. **Chart Recommendations**:
   - Input: Dataset metadata
   - Output: Top 3-5 chart suggestions with reasoning

3. **Caption Generation**:
   - Input: Chart type, columns used
   - Output: Professional description

## Data Flow

### Upload Flow
```
User selects file
     │
     ▼
Frontend validates
     │
     ▼
POST /upload (FormData)
     │
     ▼
Backend receives file
     │
     ▼
FileHandler saves file
     │
     ▼
Parse CSV → pandas DataFrame
     │
     ▼
Extract metadata
     │
     ▼
AI analysis (optional)
     │
     ▼
Return file_id + metadata
     │
     ▼
Frontend displays file info
```

### Chart Generation Flow
```
User configures chart
     │
     ▼
POST /generate-chart
{
  file_id,
  chart_type,
  x_column,
  y_columns
}
     │
     ▼
Retrieve file metadata
     │
     ▼
Load CSV data
     │
     ▼
Select chart generator
     │
     ▼
Generate chart PNG
     │
     ▼
Generate AI caption
     │
     ▼
Return chart URL + metadata
     │
     ▼
Frontend displays chart
```

## Security Considerations

### File Upload
- File type whitelist (CSV, PNG, JPG, MP3, WAV)
- File size limit (10MB)
- Unique filenames (UUID)
- Isolated upload directory

### API
- CORS configured for frontend domain
- Request validation with Pydantic
- Error handling without exposing internals
- No SQL injection (using pandas, not raw SQL)

### Future Security Enhancements
- [ ] Rate limiting
- [ ] User authentication
- [ ] File virus scanning
- [ ] Input sanitization for chart rendering
- [ ] HTTPS in production

## Scalability Considerations

### Current Architecture
- Synchronous processing
- In-memory file metadata storage
- Single-process server

### Future Scalability
- [ ] Background job queue (Celery)
- [ ] Database for metadata (PostgreSQL)
- [ ] Cloud storage for files (S3)
- [ ] Caching layer (Redis)
- [ ] Horizontal scaling with load balancer

## Technology Rationale

### Why FastAPI?
- Automatic API documentation (Swagger/OpenAPI)
- Built-in data validation (Pydantic)
- High performance (async support)
- Modern Python features (type hints)
- Easy to test

### Why React?
- Component-based architecture
- Virtual DOM for performance
- Large ecosystem
- Developer tools
- TypeScript support (future)

### Why Matplotlib/Seaborn?
- Industry standard for Python
- High-quality output
- Extensive customization
- Good documentation
- Large community

### Why Google AI Studio?
- State-of-the-art language model
- Free tier available
- Easy to integrate
- Multimodal capabilities (future)
- Reliable API

## Deployment Architecture (Future)

```
┌─────────────┐
│   Nginx     │  (Reverse Proxy)
│  (Port 80)  │
└──────┬──────┘
       │
       ├─────► Frontend (Static Files)
       │
       └─────► Backend API
                  │
                  ├─► Chart Generators
                  │
                  ├─► PostgreSQL (metadata)
                  │
                  ├─► Redis (cache)
                  │
                  └─► S3 (file storage)
```

## Monitoring & Logging (Planned)

- Request logging
- Error tracking (Sentry)
- Performance metrics
- User analytics
- API usage statistics

## Version History

- **v1.0.0** (Week 1): Initial release with 3 chart types
