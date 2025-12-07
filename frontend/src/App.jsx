import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ChartSelector from './components/ChartSelector';
import ChartDisplay from './components/ChartDisplay';
import apiService from './services/api';
import './App.css';

function App() {
  const [fileData, setFileData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    try {
      setError(null);
      const response = await apiService.uploadFile(file);
      
      if (response.success) {
        setFileData({
          file_id: response.file_id,
          ...response.metadata
        });
        setChartData(null); // Reset previous chart
      }
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Upload failed');
    }
  };

  const handleChartGenerate = async (chartConfig) => {
    if (!fileData?.file_id) {
      setError('No file uploaded');
      return;
    }

    setIsGenerating(true);
    setError(null);
    
    try {
      const request = {
        file_id: fileData.file_id,
        ...chartConfig
      };

      const response = await apiService.generateChart(request);
      
      if (response.success) {
        const chartUrl = apiService.getChartUrl(response.chart_url);
        setChartData({
          ...response,
          chart_url: chartUrl
        });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Chart generation failed');
      console.error('Chart generation error:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">📊</span>
            Graph AI System
          </h1>
          <p className="app-subtitle">
            AI-Powered Data Visualization Platform
          </p>
        </div>
        <div className="header-decoration"></div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Step 1: Upload */}
          <section className="step-section">
            <div className="step-header">
              <span className="step-number">1</span>
              <h2>Upload Your Data</h2>
            </div>
            <FileUpload onUploadSuccess={handleFileUpload} />
            
            {fileData && (
              <div className="file-info-box">
                <h4>✅ File Loaded: {fileData.original_name}</h4>
                <div className="file-stats">
                  <span>📝 {fileData.num_rows} rows</span>
                  <span>📊 {fileData.num_columns} columns</span>
                </div>
              </div>
            )}
          </section>

          {/* Step 2: Select Chart */}
          {fileData && (
            <section className="step-section">
              <div className="step-header">
                <span className="step-number">2</span>
                <h2>Select Chart Type</h2>
              </div>
              <ChartSelector 
                fileMetadata={fileData}
                onGenerate={handleChartGenerate}
                aiRecommendations={fileData.ai_recommendations}
              />
            </section>
          )}

          {/* Step 3: View Chart */}
          {(fileData || chartData || isGenerating || error) && (
            <section className="step-section">
              <div className="step-header">
                <span className="step-number">3</span>
                <h2>View Generated Chart</h2>
              </div>
              <ChartDisplay 
                chartData={chartData}
                isGenerating={isGenerating}
                error={error}
              />
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Built with ❤️ using React, FastAPI, and Google AI Studio</p>
        <p className="footer-note">Week 1 - 3 Chart Types Implemented</p>
      </footer>
    </div>
  );
}

export default App;
