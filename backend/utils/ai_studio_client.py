import os
import google.generativeai as genai
from typing import Optional, List, Dict
import json

class AIStudioClient:
    """Google AI Studio (Gemini) integration for chart recommendations and analysis"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY", "")
        self.model_name = "gemini-pro"
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Warning: Failed to initialize Google AI Studio: {e}")
    
    def is_available(self) -> bool:
        """Check if AI Studio is configured and available"""
        return self.model is not None
    
    async def analyze_dataset(self, dataset_info: dict) -> dict:
        """Analyze dataset and provide insights"""
        if not self.is_available():
            return {
                "available": False,
                "message": "AI Studio not configured. Set GOOGLE_AI_STUDIO_API_KEY environment variable."
            }
        
        prompt = self._create_analysis_prompt(dataset_info)
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "available": True,
                "analysis": response.text,
                "insights": self._parse_insights(response.text)
            }
        except Exception as e:
            return {
                "available": True,
                "error": str(e),
                "message": "Failed to analyze dataset"
            }
    
    async def recommend_chart(self, dataset_info: dict) -> dict:
        """Recommend appropriate chart types for the dataset"""
        if not self.is_available():
            return {
                "available": False,
                "recommendations": self._get_fallback_recommendations(dataset_info)
            }
        
        prompt = self._create_recommendation_prompt(dataset_info)
        
        try:
            response = self.model.generate_content(prompt)
            recommendations = self._parse_recommendations(response.text)
            
            return {
                "available": True,
                "recommendations": recommendations,
                "explanation": response.text
            }
        except Exception as e:
            return {
                "available": True,
                "error": str(e),
                "recommendations": self._get_fallback_recommendations(dataset_info)
            }
    
    async def generate_caption(self, chart_type: str, columns: List[str], dataset_info: dict) -> str:
        """Generate descriptive caption for a chart"""
        if not self.is_available():
            return f"{chart_type} chart showing {', '.join(columns)}"
        
        prompt = f"""Generate a concise, informative caption for a data visualization chart.

Chart Type: {chart_type}
Columns: {', '.join(columns)}
Dataset: {dataset_info.get('num_rows', 'N/A')} rows, {dataset_info.get('num_columns', 'N/A')} columns
Column Types: {json.dumps(dataset_info.get('dtypes', {}), indent=2)}

Generate a professional caption (1-2 sentences) that describes what this chart visualizes.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return f"{chart_type} chart showing {', '.join(columns)}"
    
    def _create_analysis_prompt(self, dataset_info: dict) -> str:
        """Create prompt for dataset analysis"""
        return f"""Analyze this dataset and provide insights:

Dataset Information:
- Rows: {dataset_info.get('num_rows')}
- Columns: {dataset_info.get('num_columns')}
- Column Names: {', '.join(dataset_info.get('columns', []))}
- Numeric Columns: {', '.join(dataset_info.get('numeric_columns', []))}
- Categorical Columns: {', '.join(dataset_info.get('categorical_columns', []))}
- Data Types: {json.dumps(dataset_info.get('dtypes', {}), indent=2)}

Sample Data:
{json.dumps(dataset_info.get('sample_data', [])[:3], indent=2)}

Provide:
1. Brief overview of the dataset
2. Key characteristics
3. Suggested analyses
4. Data quality observations
"""
    
    def _create_recommendation_prompt(self, dataset_info: dict) -> str:
        """Create prompt for chart recommendations"""
        return f"""Recommend the most appropriate chart types for this dataset:

Dataset Information:
- Columns: {', '.join(dataset_info.get('columns', []))}
- Numeric Columns: {', '.join(dataset_info.get('numeric_columns', []))}
- Categorical Columns: {', '.join(dataset_info.get('categorical_columns', []))}
- Rows: {dataset_info.get('num_rows')}

Available Chart Types:
1. Bar Chart
2. Line Chart
3. Histogram
4. Scatter Plot
5. Box Plot
6. Density Plot
7. Violin Plot
8. Heatmap
9. Area Chart
10. Pie Chart

For each recommended chart:
- Chart type name
- Suggested columns to visualize
- Brief explanation (1 sentence)

Provide top 3-5 recommendations in JSON format.
"""
    
    def _parse_insights(self, text: str) -> List[str]:
        """Parse insights from AI response"""
        # Simple parsing - split by numbered points
        lines = text.split('\n')
        insights = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                insights.append(line.lstrip('0123456789.-•').strip())
        return insights[:5]  # Top 5 insights
    
    def _parse_recommendations(self, text: str) -> List[dict]:
        """Parse chart recommendations from AI response"""
        # Try to extract structured recommendations
        # Fallback to simple parsing if JSON not found
        try:
            # Look for JSON in the response
            start = text.find('[')
            end = text.rfind(']') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback: create basic recommendations
        recommendations = []
        if "bar" in text.lower():
            recommendations.append({"type": "bar", "reason": "Good for categorical comparisons"})
        if "line" in text.lower():
            recommendations.append({"type": "line", "reason": "Good for trends over time"})
        if "scatter" in text.lower():
            recommendations.append({"type": "scatter", "reason": "Good for correlations"})
        
        return recommendations[:3]
    
    def _get_fallback_recommendations(self, dataset_info: dict) -> List[dict]:
        """Provide basic recommendations without AI"""
        recommendations = []
        
        numeric_cols = dataset_info.get('numeric_columns', [])
        categorical_cols = dataset_info.get('categorical_columns', [])
        
        # If we have numeric columns
        if len(numeric_cols) >= 1:
            recommendations.append({
                "type": "histogram",
                "columns": [numeric_cols[0]],
                "reason": "Visualize distribution of numeric data"
            })
        
        if len(numeric_cols) >= 2:
            recommendations.append({
                "type": "scatter",
                "columns": numeric_cols[:2],
                "reason": "Explore correlation between variables"
            })
        
        # If we have categorical columns
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            recommendations.append({
                "type": "bar",
                "columns": [categorical_cols[0], numeric_cols[0]],
                "reason": "Compare values across categories"
            })
        
        return recommendations[:3]
