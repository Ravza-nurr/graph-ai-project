"""
LLM-Supported Graph Generation System - Main Backend API
FastAPI application for handling file uploads and chart generation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from dotenv import load_dotenv

# Import utilities
from utils.file_handler import FileHandler
from utils.ai_studio_client import AIStudioClient

# Import chart generators
from chart_generator import bar, line, scatter, histogram, boxplot, density, heatmap, violin, area, pie

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Graph AI System",
    description="AI-powered chart generation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handlers
file_handler = FileHandler()
ai_client = AIStudioClient()

# Create output directory
os.makedirs("output", exist_ok=True)

# Store uploaded file info in memory (use database in production)
uploaded_files = {}


class ChartRequest(BaseModel):
    file_id: str
    chart_type: str
    x_column: Optional[str] = None
    y_columns: Optional[List[str]] = None
    color_column: Optional[str] = None
    size_column: Optional[str] = None
    title: Optional[str] = None


@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Graph AI System API",
        "version": "1.0.0",
        "status": "running",
        "ai_studio_available": ai_client.is_available()
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "file_handler": "ok",
            "ai_studio": "configured" if ai_client.is_available() else "not_configured"
        }
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a data file (CSV, image, or audio)
    Returns file metadata and analysis
    """
    try:
        # Save file
        metadata = await file_handler.save_file(file)
        file_id = str(uuid.uuid4())
        
        # If CSV, analyze it
        if metadata["file_type"] == "csv":
            df = file_handler.load_csv(metadata["file_path"])
            csv_info = file_handler.get_csv_info(df)
            metadata.update(csv_info)
            
            # Get AI recommendations
            ai_recommendations = await ai_client.recommend_chart(csv_info)
            metadata["ai_recommendations"] = ai_recommendations
        
        # Store metadata
        uploaded_files[file_id] = metadata
        
        return {
            "success": True,
            "file_id": file_id,
            "metadata": metadata
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    return uploaded_files[file_id]


@app.post("/generate-chart")
async def generate_chart(request: ChartRequest):
    """
    Generate a chart based on uploaded data
    """
    # Check if file exists
    if request.file_id not in uploaded_files:
        raise HTTPException(
            status_code=404, 
            detail="File not found. Please upload your file again. (Note: File sessions are cleared when the server restarts)"
        )
    
    file_metadata = uploaded_files[request.file_id]
    
    # Only CSV files supported for now
    if file_metadata["file_type"] != "csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported for chart generation"
        )
    
    try:
        # Load data
        df = file_handler.load_csv(file_metadata["file_path"])
        
        # Generate output path
        chart_filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join("output", chart_filename)
        
        # Generate chart based on type
        chart_type = request.chart_type.lower()
        
        if chart_type == "bar":
            if not request.x_column:
                raise HTTPException(status_code=400, detail="x_column required for bar chart")
            
            chart_path = bar.generate_bar_chart(
                df=df,
                x_column=request.x_column,
                y_column=request.y_columns[0] if request.y_columns else None,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "line":
            if not request.x_column or not request.y_columns:
                raise HTTPException(
                    status_code=400,
                    detail="x_column and y_columns required for line chart"
                )
            
            chart_path = line.generate_line_chart(
                df=df,
                x_column=request.x_column,
                y_columns=request.y_columns,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "scatter":
            if not request.x_column or not request.y_columns:
                raise HTTPException(
                    status_code=400,
                    detail="x_column and y_columns required for scatter plot"
                )
            
            chart_path = scatter.generate_scatter_plot(
                df=df,
                x_column=request.x_column,
                y_column=request.y_columns[0],
                color_column=request.color_column,
                size_column=request.size_column,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "histogram":
            if not request.x_column:
                raise HTTPException(status_code=400, detail="x_column required for histogram")
            
            chart_path = histogram.generate_histogram(
                df=df,
                column=request.x_column,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "boxplot":
            # Can use either x_column or y_columns
            columns = request.y_columns if request.y_columns else ([request.x_column] if request.x_column else [])
            if not columns:
                raise HTTPException(status_code=400, detail="At least one column required for box plot")
            
            chart_path = boxplot.generate_boxplot(
                df=df,
                columns=columns,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "density":
            if not request.x_column:
                raise HTTPException(status_code=400, detail="x_column required for density plot")
            
            chart_path = density.generate_density_plot(
                df=df,
                column=request.x_column,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "heatmap":
            # Heatmap can work with all numeric columns or specified columns
            columns = request.y_columns if request.y_columns else None
            
            chart_path = heatmap.generate_heatmap(
                df=df,
                columns=columns,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "violin":
            if not request.x_column:
                raise HTTPException(status_code=400, detail="x_column required for violin plot")
            
            # x_column is numeric, color_column is optional category
            chart_path = violin.generate_violin_plot(
                df=df,
                numeric_column=request.x_column,
                category_column=request.color_column,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "area":
            if not request.x_column or not request.y_columns:
                raise HTTPException(
                    status_code=400,
                    detail="x_column and y_columns required for area chart"
                )
            
            chart_path = area.generate_area_chart(
                df=df,
                x_column=request.x_column,
                y_columns=request.y_columns,
                output_path=output_path,
                title=request.title
            )
        
        elif chart_type == "pie":
            if not request.x_column:
                raise HTTPException(status_code=400, detail="x_column (category) required for pie chart")
            
            chart_path = pie.generate_pie_chart(
                df=df,
                category_column=request.x_column,
                value_column=request.y_columns[0] if request.y_columns else None,
                output_path=output_path,
                title=request.title
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Chart type '{chart_type}' not yet implemented. Available: bar, line, scatter, histogram, boxplot, density, heatmap, violin, area, pie"
            )
        
        # Generate caption using AI
        columns_used = [request.x_column] + (request.y_columns or [])
        caption = await ai_client.generate_caption(
            chart_type=chart_type,
            columns=columns_used,
            dataset_info=file_metadata
        )
        
        return {
            "success": True,
            "chart_type": chart_type,
            "chart_url": f"/charts/{chart_filename}",
            "local_path": chart_path,
            "caption": caption,
            "columns_used": columns_used
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart generation failed: {str(e)}")


@app.get("/charts/{filename}")
async def get_chart(filename: str):
    """Serve generated chart images"""
    file_path = os.path.join("output", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Chart not found")
    
    return FileResponse(file_path, media_type="image/png")


@app.post("/analyze-dataset")
async def analyze_dataset(file_id: str):
    """Get AI analysis of a dataset"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_metadata = uploaded_files[file_id]
    
    if file_metadata["file_type"] != "csv":
        raise HTTPException(status_code=400, detail="Only CSV files can be analyzed")
    
    analysis = await ai_client.analyze_dataset(file_metadata)
    
    return analysis


@app.get("/chart-types")
async def get_chart_types():
    """List all available chart types"""
    return {
        "available": [
            {"id": "bar", "name": "Bar Chart", "status": "implemented"},
            {"id": "line", "name": "Line Chart", "status": "implemented"},
            {"id": "scatter", "name": "Scatter Plot", "status": "implemented"},
            {"id": "histogram", "name": "Histogram", "status": "implemented"},
            {"id": "boxplot", "name": "Box Plot", "status": "implemented"},
            {"id": "density", "name": "Density Plot", "status": "implemented"},
            {"id": "violin", "name": "Violin Plot", "status": "implemented"},
            {"id": "heatmap", "name": "Heatmap", "status": "implemented"},
            {"id": "area", "name": "Area Chart", "status": "implemented"},
            {"id": "pie", "name": "Pie Chart", "status": "implemented"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
