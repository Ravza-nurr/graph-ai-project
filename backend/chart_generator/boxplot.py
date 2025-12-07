import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional, List

def generate_boxplot(
    df: pd.DataFrame,
    columns: List[str],
    output_path: str = "output/boxplot.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a box plot from numeric data
    
    Args:
        df: pandas DataFrame with data
        columns: List of column names for box plot (must be numeric)
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate columns
    if not columns:
        raise ValueError("At least one column must be specified")
    
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric for box plot")
    
    # Prepare data - remove NaN values
    data_to_plot = [df[col].dropna() for col in columns]
    
    # Check if we have data
    if all(len(d) == 0 for d in data_to_plot):
        raise ValueError("No valid data in specified columns")
    
    # Create box plot
    plt.figure(figsize=(max(10, len(columns) * 1.5), 6))
    
    bp = plt.boxplot(
        data_to_plot,
        labels=columns,
        patch_artist=True,
        notch=True,
        showmeans=True,
        meanprops=dict(marker='D', markerfacecolor='red', markersize=8)
    )
    
    # Color the boxes
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    for patch, color in zip(bp['boxes'], colors * (len(columns) // len(colors) + 1)):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Styling
    plt.ylabel('Value', fontsize=12, fontweight='bold')
    plt.title(title or f'Box Plot - {", ".join(columns)}', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_boxplot_by_category(
    df: pd.DataFrame,
    numeric_column: str,
    category_column: str,
    output_path: str = "output/boxplot_category.png",
    title: Optional[str] = None
) -> str:
    """
    Generate a box plot of numeric data grouped by categories
    
    Args:
        df: pandas DataFrame with data
        numeric_column: Numeric column for box plot
        category_column: Categorical column for grouping
        output_path: Where to save the chart
        title: Chart title
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate columns
    if numeric_column not in df.columns:
        raise ValueError(f"Column '{numeric_column}' not found")
    if category_column not in df.columns:
        raise ValueError(f"Column '{category_column}' not found")
    
    if not pd.api.types.is_numeric_dtype(df[numeric_column]):
        raise ValueError(f"Column '{numeric_column}' must be numeric")
    
    # Group data by category
    categories = df[category_column].unique()
    data_by_category = [df[df[category_column] == cat][numeric_column].dropna() for cat in categories]
    
    plt.figure(figsize=(max(10, len(categories) * 1.5), 6))
    
    bp = plt.boxplot(
        data_by_category,
        labels=categories,
        patch_artist=True,
        notch=True
    )
    
    # Color boxes
    for patch in bp['boxes']:
        patch.set_facecolor('#3498db')
        patch.set_alpha(0.7)
    
    plt.xlabel(category_column, fontsize=12, fontweight='bold')
    plt.ylabel(numeric_column, fontsize=12, fontweight='bold')
    plt.title(title or f'{numeric_column} by {category_column}', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
