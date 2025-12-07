import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import List, Optional

def generate_area_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    output_path: str = "output/area.png",
    title: Optional[str] = None,
    stacked: bool = False,
    **kwargs
) -> str:
    """
    Generate an area chart from data
    
    Args:
        df: pandas DataFrame with data
        x_column: Column name for x-axis
        y_columns: List of column names for y-axis (numeric)
        output_path: Where to save the chart
        title: Chart title
        stacked: Whether to stack areas
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate columns
    if x_column not in df.columns:
        raise ValueError(f"Column '{x_column}' not found in DataFrame")
    
    if not y_columns:
        raise ValueError("At least one y_column must be specified")
    
    for col in y_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric for area chart")
    
    # Prepare data - remove NaN and sort by x
    plot_columns = [x_column] + y_columns
    plot_df = df[plot_columns].dropna()
    
    if len(plot_df) == 0:
        raise ValueError("No valid data after removing NaN values")
    
    # Sort by x column
    plot_df = plot_df.sort_values(by=x_column)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Color palette
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    
    if stacked:
        # Stacked area chart
        plt.stackplot(
            plot_df[x_column],
            *[plot_df[col] for col in y_columns],
            labels=y_columns,
            colors=colors[:len(y_columns)],
            alpha=0.7
        )
    else:
        # Overlapping area charts
        for i, col in enumerate(y_columns):
            plt.fill_between(
                plot_df[x_column],
                plot_df[col],
                alpha=0.5,
                color=colors[i % len(colors)],
                label=col
            )
            plt.plot(
                plot_df[x_column],
                plot_df[col],
                color=colors[i % len(colors)],
                linewidth=2
            )
    
    # Styling
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel('Value', fontsize=12, fontweight='bold')
    plt.title(
        title or f'Area Chart - {", ".join(y_columns)}',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    plt.legend(loc='best')
    plt.grid(alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
