import React, { useState, useEffect } from 'react';
import './ChartSelector.css';

const CHART_TYPES = [
  { id: 'bar', name: 'Bar Chart', icon: '📊', status: 'implemented' },
  { id: 'line', name: 'Line Chart', icon: '📈', status: 'implemented' },
  { id: 'scatter', name: 'Scatter Plot', icon: '⚫', status: 'implemented' },
  { id: 'histogram', name: 'Histogram', icon: '📊', status: 'implemented' },
  { id: 'boxplot', name: 'Box Plot', icon: '📦', status: 'implemented' },
  { id: 'density', name: 'Density Plot', icon: '〰️', status: 'implemented' },
  { id: 'violin', name: 'Violin Plot', icon: '🎻', status: 'implemented' },
  { id: 'heatmap', name: 'Heatmap', icon: '🔥', status: 'implemented' },
  { id: 'area', name: 'Area Chart', icon: '⛰️', status: 'implemented' },
  { id: 'pie', name: 'Pie Chart', icon: '🥧', status: 'implemented' },
];

const ChartSelector = ({ fileMetadata, onGenerate, aiRecommendations }) => {
  const [selectedChart, setSelectedChart] = useState('');
  const [xColumn, setXColumn] = useState('');
  const [yColumns, setYColumns] = useState([]);
  const [colorColumn, setColorColumn] = useState('');

  const columns = fileMetadata?.columns || [];
  const numericColumns = fileMetadata?.numeric_columns || [];
  const categoricalColumns = fileMetadata?.categorical_columns || [];

  useEffect(() => {
    // Auto-select first recommended chart if available
    if (aiRecommendations?.recommendations?.length > 0) {
      const firstRec = aiRecommendations.recommendations[0];
      if (firstRec.type) {
        setSelectedChart(firstRec.type);
      }
    }
  }, [aiRecommendations]);

  const handleChartChange = (e) => {
    setSelectedChart(e.target.value);
    // Reset column selections
    setXColumn('');
    setYColumns([]);
    setColorColumn('');
  };

  const handleYColumnToggle = (col) => {
    if (yColumns.includes(col)) {
      setYColumns(yColumns.filter(c => c !== col));
    } else {
      setYColumns([...yColumns, col]);
    }
  };

  const handleGenerate = () => {
    if (!selectedChart) {
      alert('Please select a chart type');
      return;
    }

    const chartConfig = {
      chart_type: selectedChart,
      x_column: xColumn || undefined,
      y_columns: yColumns.length > 0 ? yColumns : undefined,
      color_column: colorColumn || undefined,
    };

    onGenerate(chartConfig);
  };

  const isChartAvailable = (chartId) => {
    const chart = CHART_TYPES.find(c => c.id === chartId);
    return chart?.status === 'implemented';
  };

  return (
    <div className="chart-selector-container">
      <h2>📊 Select Chart Type</h2>

      {/* AI Recommendations */}
      {aiRecommendations?.recommendations?.length > 0 && (
        <div className="ai-recommendations">
          <div className="ai-badge">✨ AI Recommendations</div>
          <div className="recommendations-list">
            {aiRecommendations.recommendations.slice(0, 3).map((rec, idx) => (
              <div 
                key={idx} 
                className="recommendation-item"
                onClick={() => setSelectedChart(rec.type)}
              >
                <span className="rec-rank">#{idx + 1}</span>
                <span className="rec-name">{rec.type}</span>
                <span className="rec-reason">{rec.reason}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Chart Type Selection */}
      <div className="chart-type-selection">
        <label>Chart Type</label>
        <select 
          value={selectedChart} 
          onChange={handleChartChange}
          className="chart-dropdown"
        >
          <option value="">-- Select Chart Type --</option>
          {CHART_TYPES.map(chart => (
            <option 
              key={chart.id} 
              value={chart.id}
              disabled={!isChartAvailable(chart.id)}
            >
              {chart.icon} {chart.name} {!isChartAvailable(chart.id) ? '(Coming Soon)' : ''}
            </option>
          ))}
        </select>
      </div>

      {/* Column Selection */}
      {selectedChart && (
        <div className="column-selection">
          {/* X-axis column for various chart types */}
          {(selectedChart === 'bar' || selectedChart === 'line' || selectedChart === 'scatter' || 
            selectedChart === 'histogram' || selectedChart === 'density' || selectedChart === 'violin' ||
            selectedChart === 'area' || selectedChart === 'pie') && (
            <div className="column-group">
              <label>
                {selectedChart === 'violin' ? 'Numeric Column' :
                 selectedChart === 'pie' ? 'Category Column' :
                 'X-Axis Column'}
              </label>
              <select 
                value={xColumn} 
                onChange={(e) => setXColumn(e.target.value)}
                className="column-dropdown"
              >
                <option value="">-- Select Column --</option>
                {(selectedChart === 'histogram' || selectedChart === 'density' || selectedChart === 'violin' 
                  ? numericColumns 
                  : selectedChart === 'pie'
                  ? categoricalColumns.length > 0 ? categoricalColumns : columns
                  : columns
                ).map(col => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>
          )}

          {/* Y-axis columns for various chart types */}
          {(selectedChart === 'line' || selectedChart === 'scatter' || selectedChart === 'bar' || 
            selectedChart === 'boxplot' || selectedChart === 'heatmap' || selectedChart === 'area' ||
            selectedChart === 'pie') && (
            <div className="column-group">
              <label>
                {selectedChart === 'boxplot' ? 'Columns for Box Plot' : 
                 selectedChart === 'heatmap' ? 'Columns (Optional - uses all numeric if empty)' :
                 selectedChart === 'area' ? 'Y-Axis Columns (multiple allowed)' :
                 selectedChart === 'pie' ? 'Value Column (Optional - counts if empty)' :
                 `Y-Axis Column${selectedChart === 'line' ? 's' : ''}`}
              </label>
              {(selectedChart === 'line' || selectedChart === 'boxplot' || selectedChart === 'heatmap' || selectedChart === 'area') ? (
                <div className="multi-select">
                  {numericColumns.map(col => (
                    <label key={col} className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={yColumns.includes(col)}
                        onChange={() => handleYColumnToggle(col)}
                      />
                      <span>{col}</span>
                    </label>
                  ))}
                </div>
              ) : (
                <select 
                  value={yColumns[0] || ''} 
                  onChange={(e) => setYColumns([e.target.value])}
                  className="column-dropdown"
                >
                  <option value="">-- Select Column --</option>
                  {numericColumns.map(col => (
                    <option key={col} value={col}>{col}</option>
                  ))}
                </select>
              )}
            </div>
          )}

          {/* Color by category (for scatter and violin) */}
          {(selectedChart === 'scatter' || selectedChart === 'violin') && categoricalColumns.length > 0 && (
            <div className="column-group">
              <label>{selectedChart === 'violin' ? 'Group By (Optional)' : 'Color By (Optional)'}</label>
              <select 
                value={colorColumn} 
                onChange={(e) => setColorColumn(e.target.value)}
                className="column-dropdown"
              >
                <option value="">-- None --</option>
                {categoricalColumns.map(col => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}

      {/* Generate Button */}
      <button 
        onClick={handleGenerate}
        className="generate-btn"
        disabled={!selectedChart}
      >
        🎨 Generate Chart
      </button>
    </div>
  );
};

export default ChartSelector;
