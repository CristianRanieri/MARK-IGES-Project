import pandas as pd
import matplotlib.pyplot as plt

def generate_mann_whitney_table(results_csv, output_image="mann_whitney_results.png"):
    """
    Generate an image table for Mann-Whitney U test results.

    Args:
        results_csv (str): Path to the CSV file containing Mann-Whitney results.
        output_image (str): Path to save the generated image table.
    """
    # Load Mann-Whitney results from CSV
    results = pd.read_csv(results_csv)

    # Select and format relevant columns
    results_table = results[[
        "Metric", "Group 1", "Group 2", "U-Statistic", "Raw p-value",
        "Adjusted p-value", "Significant (Holm)"
    ]]

    # Convert significance status to a readable format
    results_table["Significant (Holm)"] = results_table["Significant (Holm)"].apply(
        lambda x: "Yes" if x else "No"
    )

    # Plot the table
    fig, ax = plt.subplots(figsize=(12, len(results_table) * 0.6))  # Adjust height based on the number of rows
    ax.axis("off")  # Hide the axes
    table = ax.table(
        cellText=results_table.values,
        colLabels=results_table.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(results_table.columns))))

    # Save the table as an image
    plt.savefig(output_image, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Table saved to {output_image}")


# Example Usage
# CSV file must contain columns: Metric, Group 1, Group 2, U-Statistic, Raw p-value, Adjusted p-value, Significant (Holm)
generate_mann_whitney_table("analysis_results_posthoc.csv", "mann_whitney_results.png")
