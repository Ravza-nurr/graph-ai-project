import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional
import seaborn as sns

def generate_density_plot(
    df: pd.DataFrame,
    column: str,
    output_path: str = "output/density.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a density plot (KDE) from numeric data
    
    Args:
        df: pandas DataFrame with data
        column: Column name for density plot (must be numeric)
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate column
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric for density plot")
    
    # Remove NaN values
    data = df[column].dropna()
    
    if len(data) == 0:
        raise ValueError(f"Column '{column}' has no valid data")
    
    # Create density plot
    plt.figure(figsize=(10, 6))
    
    # Use seaborn for better density visualization
    sns.kdeplot(data=data, fill=True, color='#3498db', alpha=0.6, linewidth=2)
    
    # Add rug plot to show individual data points
    sns.rugplot(data=data, color='#2c3e50', alpha=0.3, height=0.05)
    
    # Mark mean and median
    mean_val = data.mean()
    median_val = data.median()
    
    plt.axvline(mean_val, color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    plt.axvline(median_val, color='#2ecc71', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
    
    # Styling
    plt.xlabel(column, fontsize=12, fontweight='bold')
    plt.ylabel('Density', fontsize=12, fontweight='bold')
    plt.title(title or f'Density Distribution of {column}', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_multi_density_plot(
    df: pd.DataFrame,
    columns: list,
    output_path: str = "output/multi_density.png",
    title: Optional[str] = None
) -> str:
    """
    Generate overlapping density plots for multiple columns
    
    Args:
        df: pandas DataFrame with data
        columns: List of column names (must be numeric)
        output_path: Where to save the chart
        title: Chart title
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate columns
    if not columns:
        raise ValueError("At least one column must be specified")
    
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric")
    
    plt.figure(figsize=(10, 6))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    for i, col in enumerate(columns):
        data = df[col].dropna()
        if len(data) > 0:
            sns.kdeplot(
                data=data,
                fill=True,
                color=colors[i % len(colors)],
                alpha=0.4,
                linewidth=2,
                label=col
            )
    
    plt.xlabel('Value', fontsize=12, fontweight='bold')
    plt.ylabel('Density', fontsize=12, fontweight='bold')
    plt.title(title or f'Density Comparison - {", ".join(columns)}', fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
