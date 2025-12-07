import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional

def generate_histogram(
    df: pd.DataFrame,
    column: str,
    bins: int = 30,
    output_path: str = "output/histogram.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a histogram from numeric data
    
    Args:
        df: pandas DataFrame with data
        column: Column name for histogram (must be numeric)
        bins: Number of bins for the histogram
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate column exists and is numeric
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric for histogram")
    
    # Remove NaN values
    data = df[column].dropna()
    
    if len(data) == 0:
        raise ValueError(f"Column '{column}' has no valid data")
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    
    n, bins_edges, patches = plt.hist(
        data, 
        bins=bins, 
        color='#3498db', 
        alpha=0.7, 
        edgecolor='#2c3e50',
        linewidth=1.2
    )
    
    # Add a kernel density estimate (KDE) curve
    from scipy import stats
    density = stats.gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), 200)
    density_values = density(xs)
    # Scale density to match histogram height
    density_values = density_values * len(data) * (data.max() - data.min()) / bins
    plt.plot(xs, density_values, color='#e74c3c', linewidth=2, label='Density')
    
    # Styling
    plt.xlabel(column, fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.title(title or f'Distribution of {column}', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.legend()
    
    # Add statistics text box
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()
    stats_text = f'Mean: {mean_val:.2f}\nMedian: {median_val:.2f}\nStd: {std_val:.2f}'
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
