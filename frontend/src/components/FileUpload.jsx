import React, { useState } from 'react';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  };

  const handleFileSelect = async (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      await uploadFile(files[0]);
    }
  };

  const uploadFile = async (file) => {
    setIsUploading(true);
    setUploadError(null);

    try {
      // Call parent callback with file
      await onUploadSuccess(file);
    } catch (error) {
      setUploadError(error.message || 'Upload failed');
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isUploading ? (
          <div className="upload-progress">
            <div className="spinner"></div>
            <p>Uploading and analyzing...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📊</div>
            <h3>Drop your data file here</h3>
            <p className="upload-description">
              Supports CSV, images (PNG, JPG), and audio files (MP3, WAV)
            </p>
            <p className="upload-hint">or</p>
            <label className="file-select-btn">
              Browse Files
              <input
                type="file"
                onChange={handleFileSelect}
                accept=".csv,.png,.jpg,.jpeg,.gif,.mp3,.wav,.ogg"
                style={{ display: 'none' }}
              />
            </label>
          </>
        )}
      </div>

      {uploadError && (
        <div className="error-message">
          ⚠️ {uploadError}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
