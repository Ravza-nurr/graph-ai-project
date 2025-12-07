import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional
import seaborn as sns

def generate_violin_plot(
    df: pd.DataFrame,
    numeric_column: str,
    category_column: Optional[str] = None,
    output_path: str = "output/violin.png",
    title: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a violin plot from numeric data
    
    Args:
        df: pandas DataFrame with data
        numeric_column: Numeric column for violin plot
        category_column: Optional categorical column for grouping
        output_path: Where to save the chart
        title: Chart title
        **kwargs: Additional arguments
    
    Returns:
        Path to saved chart
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Validate numeric column
    if numeric_column not in df.columns:
        raise ValueError(f"Column '{numeric_column}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[numeric_column]):
        raise ValueError(f"Column '{numeric_column}' must be numeric for violin plot")
    
    # Remove NaN values from numeric column
    if category_column:
        # Validate category column
        if category_column not in df.columns:
            raise ValueError(f"Column '{category_column}' not found in DataFrame")
        
        plot_df = df[[numeric_column, category_column]].dropna()
    else:
        plot_df = df[[numeric_column]].dropna()
    
    if len(plot_df) == 0:
        raise ValueError("No valid data after removing NaN values")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    if category_column:
        # Violin plot grouped by category
        sns.violinplot(
            data=plot_df,
            x=category_column,
            y=numeric_column,
            palette='Set2',
            inner='quartile'  # Show quartiles inside
        )
        
        # Add individual points
        sns.stripplot(
            data=plot_df,
            x=category_column,
            y=numeric_column,
            color='black',
            alpha=0.3,
            size=3
        )
        
        plt.xlabel(category_column, fontsize=12, fontweight='bold')
    else:
        # Single violin plot
        sns.violinplot(
            data=plot_df,
            y=numeric_column,
            color='#3498db',
            inner='quartile'
        )
        
        sns.stripplot(
            data=plot_df,
            y=numeric_column,
            color='black',
            alpha=0.3,
            size=3
        )
        
        plt.xlabel('')
    
    # Styling
    plt.ylabel(numeric_column, fontsize=12, fontweight='bold')
    plt.title(
        title or f'Violin Plot - {numeric_column}' + 
        (f' by {category_column}' if category_column else ''),
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path
