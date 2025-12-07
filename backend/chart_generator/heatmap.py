import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional, List
import seaborn as sns

def generate_heatmap(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    output_path: str = "output/heatmap.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a correlation heatmap from numeric data
    
    Args:
        df: pandas DataFrame with data
        columns: List of column names for heatmap (must be numeric). If None, uses all numeric columns
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # If no columns specified, use all numeric columns
    if columns is None:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            raise ValueError("No numeric columns found in DataFrame")
        columns = numeric_df.columns.tolist()
    else:
        # Validate columns
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Column '{col}' must be numeric for heatmap")
    
    # Select only specified columns and drop NaN
    data = df[columns].dropna()
    
    if len(data) == 0:
        raise ValueError("No valid data after removing NaN values")
    
    # Calculate correlation matrix
    corr_matrix = data.corr()
    
    # Create heatmap
    plt.figure(figsize=(max(10, len(columns) * 0.8), max(8, len(columns) * 0.7)))
    
    # Use seaborn for better heatmap visualization
    sns.heatmap(
        corr_matrix,
        annot=True,  # Show correlation values
        fmt='.2f',   # Format to 2 decimal places
        cmap='coolwarm',  # Color scheme
        center=0,    # Center colormap at 0
        square=True,  # Make cells square
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        vmin=-1,
        vmax=1
    )
    
    # Styling
    plt.title(title or 'Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_value_heatmap(
    df: pd.DataFrame,
    row_column: str,
    col_column: str,
    value_column: str,
    output_path: str = "output/value_heatmap.png",
    title: Optional[str] = None
) -> str:
    """
    Generate a heatmap showing values in a matrix format
    
    Args:
        df: pandas DataFrame with data
        row_column: Column for heatmap rows
        col_column: Column for heatmap columns
        value_column: Column for heatmap values (numeric)
        output_path: Where to save the chart
        title: Chart title
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate columns
    for col in [row_column, col_column, value_column]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
    
    if not pd.api.types.is_numeric_dtype(df[value_column]):
        raise ValueError(f"Value column '{value_column}' must be numeric")
    
    # Create pivot table
    pivot_table = df.pivot_table(
        values=value_column,
        index=row_column,
        columns=col_column,
        aggfunc='mean'
    )
    
    plt.figure(figsize=(max(10, len(pivot_table.columns) * 0.8), 
                       max(8, len(pivot_table.index) * 0.5)))
    
    sns.heatmap(
        pivot_table,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    
    plt.title(title or f'{value_column} by {row_column} and {col_column}',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel(col_column, fontsize=12, fontweight='bold')
    plt.ylabel(row_column, fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
