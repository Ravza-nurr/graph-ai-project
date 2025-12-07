import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional

def generate_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    output_path: str = "output/scatter_plot.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a scatter plot from CSV data
    
    Args:
        df: pandas DataFrame with data
        x_column: Column name for x-axis (numeric)
        y_column: Column name for y-axis (numeric)
        color_column: Optional column to color points by category
        size_column: Optional column to size points by value
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    
    # Prepare scatter plot parameters
    x_data = df[x_column]
    y_data = df[y_column]
    
    # Handle color by category
    if color_column and color_column in df.columns:
        categories = df[color_column].unique()
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        for idx, category in enumerate(categories):
            mask = df[color_column] == category
            
            # Handle size
            if size_column and size_column in df.columns:
                sizes = df[mask][size_column] * 50  # Scale sizes
            else:
                sizes = 100
            
            plt.scatter(df[mask][x_column], df[mask][y_column],
                       c=[colors[idx]], s=sizes, alpha=0.6,
                       edgecolors='black', linewidth=0.5,
                       label=str(category))
        
        plt.legend(title=color_column, bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        # Simple scatter without categories
        if size_column and size_column in df.columns:
            sizes = df[size_column] * 50
        else:
            sizes = 100
        
        plt.scatter(x_data, y_data, c='#3498db', s=sizes, 
                   alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Add trend line
    try:
        z = np.polyfit(x_data.dropna(), y_data.dropna(), 1)
        p = np.poly1d(z)
        plt.plot(x_data, p(x_data), "r--", alpha=0.5, linewidth=2, label='Trend')
    except:
        pass
    
    # Styling
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel(y_column, fontsize=12, fontweight='bold')
    plt.title(title or f'{y_column} vs {x_column}', 
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_bubble_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: str,
    color_column: Optional[str] = None,
    output_path: str = "output/bubble_chart.png",
    title: Optional[str] = None
) -> str:
    """Generate bubble chart (scatter with sized points)"""
    return generate_scatter_plot(
        df=df,
        x_column=x_column,
        y_column=y_column,
        color_column=color_column,
        size_column=size_column,
        output_path=output_path,
        title=title or f'Bubble Chart: {y_column} vs {x_column}'
    )
