import React from 'react';
import './ChartDisplay.css';

const ChartDisplay = ({ chartData, isGenerating, error }) => {
  if (isGenerating) {
    return (
      <div className="chart-display-container">
        <div className="generating-state">
          <div className="spinner-large"></div>
          <h3>Generating your chart...</h3>
          <p>AI is creating a beautiful visualization</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chart-display-container">
        <div className="error-state">
          <div className="error-icon">⚠️</div>
          <h3>Chart Generation Failed</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!chartData) {
    return (
      <div className="chart-display-container">
        <div className="empty-state">
          <div className="empty-icon">📊</div>
          <h3>No Chart Yet</h3>
          <p>Upload a file and select a chart type to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-display-container">
      <div className="chart-header">
        <h2>📈 Your Chart</h2>
        <div className="chart-meta">
          <span className="chart-type-badge">{chartData.chart_type}</span>
          <span className="columns-used">
            Columns: {chartData.columns_used?.join(', ')}
          </span>
        </div>
      </div>

      <div className="chart-image-wrapper">
        <img 
          src={chartData.chart_url} 
          alt={`${chartData.chart_type} chart`}
          className="chart-image"
        />
      </div>

      {chartData.caption && (
        <div className="chart-caption">
          <div className="caption-badge">✨ AI Caption</div>
          <p>{chartData.caption}</p>
        </div>
      )}

      <div className="chart-actions">
        <a 
          href={chartData.chart_url} 
          download={`chart-${chartData.chart_type}.png`}
          className="download-btn"
        >
          ⬇️ Download Chart
        </a>
      </div>
    </div>
  );
};

export default ChartDisplay;
