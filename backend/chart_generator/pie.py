import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional

def generate_pie_chart(
    df: pd.DataFrame,
    category_column: str,
    value_column: Optional[str] = None,
    output_path: str = "output/pie.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a pie chart from categorical data
    
    Args:
        df: pandas DataFrame with data
        category_column: Column for pie categories
        value_column: Optional numeric column for values. If None, counts occurrences
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate category column
    if category_column not in df.columns:
        raise ValueError(f"Column '{category_column}' not found in DataFrame")
    
    # Prepare data
    if value_column:
        # Use specified value column
        if value_column not in df.columns:
            raise ValueError(f"Column '{value_column}' not found in DataFrame")
        
        if not pd.api.types.is_numeric_dtype(df[value_column]):
            raise ValueError(f"Column '{value_column}' must be numeric")
        
        # Group by category and sum values
        plot_data = df.groupby(category_column)[value_column].sum()
    else:
        # Count occurrences
        plot_data = df[category_column].value_counts()
    
    # Remove any zero or negative values
    plot_data = plot_data[plot_data > 0]
    
    if len(plot_data) == 0:
        raise ValueError("No valid data for pie chart")
    
    # Limit to top 10 categories for readability
    if len(plot_data) > 10:
        plot_data = plot_data.nlargest(10)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Color palette
    colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data)))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        plot_data.values,
        labels=plot_data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        pctdistance=0.85,
        explode=[0.05] * len(plot_data)  # Slight separation
    )
    
    # Styling for text
    for text in texts:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    # Equal aspect ratio ensures pie is circular
    ax.axis('equal')
    
    # Title
    plt.title(
        title or f'{category_column} Distribution',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
    # Add legend with values
    legend_labels = [f'{label}: {value:.0f}' for label, value in zip(plot_data.index, plot_data.values)]
    plt.legend(
        legend_labels,
        loc='center left',
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=9
    )
    
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_donut_chart(
    df: pd.DataFrame,
    category_column: str,
    value_column: Optional[str] = None,
    output_path: str = "output/donut.png",
    title: Optional[str] = None
) -> str:
    """
    Generate a donut chart (pie chart with hole in center)
    
    Args:
        df: pandas DataFrame with data
        category_column: Column for categories
        value_column: Optional numeric column for values
        output_path: Where to save the chart
        title: Chart title
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate and prepare data (same as pie chart)
    if category_column not in df.columns:
        raise ValueError(f"Column '{category_column}' not found")
    
    if value_column:
        if value_column not in df.columns:
            raise ValueError(f"Column '{value_column}' not found")
        plot_data = df.groupby(category_column)[value_column].sum()
    else:
        plot_data = df[category_column].value_counts()
    
    plot_data = plot_data[plot_data > 0]
    
    if len(plot_data) > 10:
        plot_data = plot_data.nlargest(10)
    
    # Create donut chart
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(plot_data)))
    
    wedges, texts, autotexts = ax.pie(
        plot_data.values,
        labels=plot_data.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        pctdistance=0.85,
        wedgeprops=dict(width=0.5)  # This creates the donut hole
    )
    
    for text in texts:
        text.set_fontsize(10)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax.axis('equal')
    plt.title(title or f'{category_column} Distribution (Donut)', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
