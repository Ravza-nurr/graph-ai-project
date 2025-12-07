import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import List, Optional

def generate_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: Optional[str] = None,
    output_path: str = "output/bar_chart.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a bar chart from CSV data
    
    Args:
        df: pandas DataFrame with data
        x_column: Column name for x-axis (categorical)
        y_column: Column name for y-axis (numeric). If None, counts occurrences
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional matplotlib arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    if y_column is None:
        # Count occurrences
        value_counts = df[x_column].value_counts()
        x_vals = value_counts.index.tolist()
        y_vals = value_counts.values.tolist()
        ylabel = "Count"
    else:
        # Use specified y column
        # Group by x_column and sum/mean y_column
        grouped = df.groupby(x_column)[y_column].sum()
        x_vals = grouped.index.tolist()
        y_vals = grouped.values.tolist()
        ylabel = y_column
    
    # Create bar chart
    bars = plt.bar(x_vals, y_vals, color='#3498db', alpha=0.8, edgecolor='#2c3e50')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)
    
    # Styling
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel(ylabel, fontsize=12, fontweight='bold')
    plt.title(title or f'{ylabel} by {x_column}', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path


def generate_grouped_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    group_column: str,
    output_path: str = "output/grouped_bar_chart.png",
    title: Optional[str] = None
) -> str:
    """Generate grouped bar chart"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Pivot data for grouped bar chart
    pivot_df = df.pivot_table(values=y_column, index=x_column, columns=group_column, aggfunc='sum')
    
    plt.figure(figsize=(12, 6))
    pivot_df.plot(kind='bar', ax=plt.gca(), width=0.8)
    
    plt.xlabel(x_column, fontsize=12, fontweight='bold')
    plt.ylabel(y_column, fontsize=12, fontweight='bold')
    plt.title(title or f'{y_column} by {x_column} (grouped by {group_column})', 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(title=group_column, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
