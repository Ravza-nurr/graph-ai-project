/**
 * API Service for Graph AI System
 * Handles all backend communication
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  /**
   * Upload a file to the backend
   */
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Get information about an uploaded file
   */
  async getFileInfo(fileId) {
    const response = await api.get(`/file/${fileId}`);
    return response.data;
  },

  /**
   * Generate a chart
   */
  async generateChart(chartRequest) {
    const response = await api.post('/generate-chart', chartRequest);
    return response.data;
  },

  /**
   * Get AI analysis of a dataset
   */
  async analyzeDataset(fileId) {
    const response = await api.post('/analyze-dataset', { file_id: fileId });
    return response.data;
  },

  /**
   * Get list of available chart types
   */
  async getChartTypes() {
    const response = await api.get('/chart-types');
    return response.data;
  },

  /**
   * Get chart image URL
   */
  getChartUrl(chartPath) {
    return `${API_BASE_URL}${chartPath}`;
  },

  /**
   * Health check
   */
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;
