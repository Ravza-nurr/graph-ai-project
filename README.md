# 📊 Graph AI System

An AI-powered data visualization platform that automatically analyzes datasets and generates beautiful, insightful charts. Built with FastAPI, React, and Google AI Studio integration.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![React](https://img.shields.io/badge/react-18.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

🎯 **AI-Powered Recommendations** - Google AI Studio analyzes your data and suggests the best chart types  
📈 **10 Chart Types** - Bar, Line, Scatter, Histogram, Box Plot, Density, Violin, Heatmap, Area, Pie  
🚀 **Easy Upload** - Drag-and-drop support for CSV, images, and audio files  
💅 **Premium UI** - Modern, glassmorphic design with smooth animations  
🤖 **Smart Captions** - AI-generated descriptions for your visualizations  
⚡ **Fast API** - Built with FastAPI for high performance  

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional, for AI features):
```bash
copy .env.example .env
# Edit .env and add your Google AI Studio API key
```

5. Start the backend server:
```bash
python app.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## 📖 Usage

1. **Upload Your Data**: Drag and drop a CSV file or click to browse
2. **AI Analysis**: The system analyzes your data and recommends chart types
3. **Select Chart**: Choose from recommended or all available chart types
4. **Configure Columns**: Select which columns to visualize
5. **Generate**: Click "Generate Chart" to create your visualization
6. **Download**: Save your chart as a PNG image

## 🎨 Available Chart Types

### Week 1 (Implemented ✅)
- **Bar Chart** - Compare categorical data
- **Line Chart** - Show trends over time
- **Scatter Plot** - Explore correlations with optional color coding

### Coming Soon
- **Histogram** - Distribution analysis
- **Box Plot** - Statistical distributions
- **Density Plot** - Smooth distributions
- **Violin Plot** - Combined box plot and density
- **Heatmap** - Correlation matrices
- **Area Chart** - Cumulative trends
- **Pie Chart** - Proportional data

## 🔧 API Endpoints

### GET /
Health check endpoint

### POST /upload
Upload a data file

**Request:**
- Multipart form data with `file` field

**Response:**
```json
{
  "success": true,
  "file_id": "uuid",
  "metadata": {
    "columns": [...],
    "num_rows": 100,
    "ai_recommendations": {...}
  }
}
```

### POST /generate-chart
Generate a chart from uploaded data

**Request:**
```json
{
  "file_id": "uuid",
  "chart_type": "bar",
  "x_column": "Category",
  "y_columns": ["Value"]
}
```

**Response:**
```json
{
  "success": true,
  "chart_url": "/charts/generated.png",
  "caption": "AI-generated caption...",
  "columns_used": ["Category", "Value"]
}
```

### GET /charts/{filename}
Retrieve a generated chart image

### GET /chart-types
List all available chart types

### POST /analyze-dataset
Get AI analysis of a dataset

## 🧠 Google AI Studio Integration

Graph AI System uses Google's Gemini API for intelligent features:

1. **Dataset Analysis**: Automatically analyzes your data structure
2. **Chart Recommendations**: Suggests the best visualizations
3. **Caption Generation**: Creates descriptive captions

### Setup

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to `backend/.env`:
```
GOOGLE_AI_STUDIO_API_KEY=your_api_key_here
```

**Note:** The system works without an API key, but AI features will be disabled.

## 📁 Project Structure

```
graph-ai-project/
├── backend/
│   ├── app.py                  # FastAPI main application
│   ├── requirements.txt        # Python dependencies
│   ├── chart_generator/        # Chart generation modules
│   │   ├── bar.py
│   │   ├── line.py
│   │   └── scatter.py
│   └── utils/                  # Utilities
│       ├── file_handler.py
│       └── ai_studio_client.py
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API services
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── data/
│   ├── samples/                # Sample datasets
│   └── uploads/                # User uploads
└── docs/                       # Documentation
```

## 🧪 Testing with Sample Data

A sample Titanic dataset is included for testing:

```bash
# Located at: data/samples/titanic.csv
```

Try these visualizations:
- Bar chart: `Pclass` vs `Survived`
- Line chart: `PassengerId` vs `Age`, `Fare`
- Scatter plot: `Age` vs `Fare`, color by `Sex`

## 🛠️ Development

### Adding New Chart Types

1. Create a new file in `backend/chart_generator/`
2. Implement the chart generation function
3. Update `backend/app.py` to handle the new chart type
4. Add the chart to the frontend dropdown

Example:
```python
# backend/chart_generator/histogram.py
def generate_histogram(df, column, output_path, **kwargs):
    # Implementation
    return output_path
```

## 📝 Week 1 Status

✅ Backend API with FastAPI  
✅ 3 working chart types (Bar, Line, Scatter)  
✅ File upload with validation  
✅ Google AI Studio integration ready  
✅ React frontend with modern UI  
✅ Complete documentation  

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👨‍💻 Author

Built with ❤️ using React, FastAPI, and Google AI Studio

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- React and Vite for the frontend tooling
- Google AI Studio for intelligent features
- Matplotlib, Seaborn, and Plotly for visualization
