import os
import pandas as pd
from typing import Optional
from fastapi import UploadFile, HTTPException
import uuid

class FileHandler:
    """Handles file uploads, validation, and processing"""
    
    ALLOWED_EXTENSIONS = {
        'csv': ['csv'],
        'image': ['png', 'jpg', 'jpeg', 'gif'],
        'audio': ['mp3', 'wav', 'ogg']
    }
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> tuple[bool, str]:
        """Validate file type and size"""
        if not file.filename:
            return False, "No filename provided"
        
        # Check extension
        ext = file.filename.split('.')[-1].lower()
        all_extensions = []
        for exts in self.ALLOWED_EXTENSIONS.values():
            all_extensions.extend(exts)
        
        if ext not in all_extensions:
            return False, f"File type .{ext} not allowed"
        
        return True, "Valid"
    
    async def save_file(self, file: UploadFile) -> dict:
        """Save uploaded file and return metadata"""
        is_valid, message = self.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Generate unique filename
        ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        content = await file.read()
        
        # Check file size
        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Get file type
        file_type = self._get_file_type(ext)
        
        metadata = {
            "original_name": file.filename,
            "saved_name": unique_filename,
            "file_path": file_path,
            "file_type": file_type,
            "size_bytes": len(content),
            "extension": ext
        }
        
        return metadata
    
    def _get_file_type(self, ext: str) -> str:
        """Determine file type from extension"""
        for file_type, extensions in self.ALLOWED_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        return "unknown"
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load CSV file into pandas DataFrame"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading CSV: {str(e)}"
            )
    
    def get_csv_info(self, df: pd.DataFrame) -> dict:
        """Extract metadata from DataFrame"""
        # Replace NaN values with None for JSON compatibility
        sample_df = df.head(5).fillna(value="null")
        
        return {
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "sample_data": sample_df.to_dict('records')
        }
