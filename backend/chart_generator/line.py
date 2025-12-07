import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import List, Optional

def generate_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    output_path: str = "output/line_chart.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a line chart from CSV data
    
    Args:
        df: pandas DataFrame with data
        x_column: Column name for x-axis (typically time/sequence)
        y_columns: List of column names for y-axis (numeric)
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Sort by x column if numeric or datetime
    try:
        df_sorted = df.sort_values(by=x_column)
    except:
        df_sorted = df
    
    # Plot each y column
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    
    for idx, y_col in enumerate(y_columns):
        color = colors[idx % len(colors)]
        plt.plot(df_sorted[x_column], df_sorted[y_col], 
                marker='o', linewidth=2.5, markersize=6,
                label=y_col, color=color, alpha=0.8)
    
    # Styling
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel('Value', fontsize=12, fontweight='bold')
    plt.title(title or f'{", ".join(y_columns)} over {x_column}', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='best', frameon=True, shadow=True)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_multi_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    output_path: str = "output/multi_line_chart.png",
    title: Optional[str] = None,
    fill_between: bool = False
) -> str:
    """Generate multi-line chart with optional area fill"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    try:
        df_sorted = df.sort_values(by=x_column)
    except:
        df_sorted = df
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    for idx, y_col in enumerate(y_columns):
        color = colors[idx % len(colors)]
        plt.plot(df_sorted[x_column], df_sorted[y_col], 
                marker='o', linewidth=2, label=y_col, color=color)
        
        if fill_between:
            plt.fill_between(df_sorted[x_column], df_sorted[y_col], 
                           alpha=0.2, color=color)
    
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel('Value', fontsize=12, fontweight='bold')
    plt.title(title or f'Trends over {x_column}', fontsize=14, fontweight='bold', pad=20)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
