import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from matplotlib.gridspec import GridSpec
# # Path to the Libertine font file
libertine_font_path = './plot_generating/LinBiolinum_R.otf'
#
# # Add the font to Matplotlib's font manager
font_manager.fontManager.addfont(libertine_font_path)

font = {'family' : 'Linux Libertine Capitals'}
plt.rc('font', **font)


def remove_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))]
# Z-Score Method
def remove_outliers_zscore(data, threshold=2):
    z_scores = (data - np.mean(data)) / np.std(data)
    return data[np.abs(z_scores) <= threshold]

def generate_unique_plot_v2(data_p, data_c, data_t, data_p_c, attributes):
    print("-----------------Generating Unique Plot-----------------")
    num_plots = len(attributes)
    rows = (num_plots + 2) // 3  # Dynamically calculate rows for a maximum of 3 columns
    cols = 3
    fig, axs = plt.subplots(rows, cols, figsize=(26, 13))
    axs = axs.flatten()  # Flatten the array to iterate easily
    #delete axs that are not used
    colors = ['#3172AD', '#C76526', '#479C76', '#AD56AD']  # Blue, Orange, Green, Purple
    y_labels = {'Stars': 'Stars',
                'Size': 'Lines of Code (LOC)',
                'Forks': 'Forks',
                'Commit Count': 'Commits',
                'Project Age': 'Project Age (Days)',
                'Activity Rate': 'Activity Rate (Commits/Day)',
                'ContributorNumber': 'Contributors'}

    for i, attribute in enumerate(attributes):

        data_p_clean = data_p[attribute]
        data_c_clean = data_c[attribute]
        data_t_clean = data_t[attribute]
        data_p_c_clean = data_p_c[attribute]
        data_t_clean.dropna(inplace=True)

        # Check if there are enough data points to plot
        if len(data_p_clean) == 0 or len(data_c_clean) == 0 or len(data_t_clean) == 0 or len(data_p_c_clean) == 0:
            print(f"Not enough data to plot for attribute: {attribute}")
            continue

        # Generate a box plot
        ax = axs[i].boxplot([data_p_clean, data_c_clean, data_t_clean, data_p_c_clean], patch_artist=True,
                            whiskerprops=dict(color='black'),
                            capprops=dict(color='black'),
                            medianprops=dict(color='white', linewidth=2))

        #merge the data
        data = pd.concat([data_p_clean, data_c_clean, data_t_clean, data_p_c_clean], axis=0)

        # ylim to the 75th percentile
        axs[i].set_ylim(data.quantile(0.05), data.quantile(0.95))

        valid_data = [data_p_clean, data_c_clean, data_t_clean, data_p_c_clean]
        valid_colors = [colors[i] for i, data in enumerate(valid_data) if len(data) > 0]
        for patch, color in zip(ax['boxes'], valid_colors):
            patch.set_facecolor(color)

        # Axis Labels and Grid
        axs[i].set_xticklabels(['MP', 'MC', 'LT', 'MPC'], fontsize=16, weight='bold')
        rounded_ticks = [round(tick, 1) for tick in axs[i].get_yticks()]
        #round the label if it is integer
        if attribute != "Activity Rate":
            rounded_ticks = [int(tick) for tick in rounded_ticks]
        axs[i].set_yticklabels(rounded_ticks, fontsize=18,weight='bold')
        axs[i].set_ylabel(y_labels[attribute], fontsize=18, weight='bold')
        axs[i].grid(True, linestyle='--', alpha=0.6)

        if len(data_t_clean) == 0:
            print(f"No data available for LT in {attribute}")
            axs[i].text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center')
            continue

        #for each median value if the median is integer then round it to integer
        median_p = data_p_clean.median()
        if median_p.is_integer():
            median_p = int(median_p)
        else:
            median_p = round(median_p, 2)
        median_c = data_c_clean.median()
        if median_c.is_integer():
            median_c = int(median_c)
        else:
            median_c = round(median_c, 2)

        median_t = data_t_clean.median()
        if median_t.is_integer():
            median_t = int(median_t)
        else:
            median_t = round(median_t, 2)

        median_p_c = data_p_c_clean.median()
        if median_p_c.is_integer():
            median_p_c = int(median_p_c)
        else:
            median_p_c = round(median_p_c, 2)

        # Create custom legend entries for the median values
        legend_handles = [
            plt.Line2D([0], [0], color=colors[0], lw=4, label=f'{median_p}'),
            plt.Line2D([0], [0], color=colors[1], lw=4, label=f'{median_c}'),
            plt.Line2D([0], [0], color=colors[2], lw=4, label=f'{median_t}'),
            plt.Line2D([0], [0], color=colors[3], lw=4, label=f'{median_p_c}')
        ]

        # Define font properties explicitly
        legend_font_properties = font_manager.FontProperties(
            family='Linux Libertine Capitals',  # Your custom font family
            weight='bold',  # Make it bold
            style='normal',  # Normal style (not italic)
            size=18  # Font size
        )

        # Define font properties explicitly for the title
        title_font_properties = font_manager.FontProperties(
            family='Linux Libertine Capitals',  # Your custom font family
            weight='bold',  # Make title bold
            style='normal',  # Normal style
            size=20  # Title font size (slightly larger for emphasis)
        )

        # Use the `prop` argument with the defined font properties
        axs[i].legend(
            handles=legend_handles,
            loc='upper center',
            fontsize=18,  # You can still use fontsize here for general scaling
            ncol=4,
            title='Median Values',
            bbox_to_anchor=(0, 1.25, 1, 0.14),
            prop=legend_font_properties,
            title_fontproperties=title_font_properties  # Bold title
        )

    for j in range(num_plots, len(axs)):
        axs[j].axis('off')




    plt.tight_layout()  # Adjust layout to fit the title
    plt.savefig('unique_plot_improved_part.pdf', dpi=300)
    plt.show()




def main():
    # Function to load data from a CSV file into a dictionary
    repository_attributes = ['Stars', 'Size', 'Forks', 'Commit Count']

    activity_metrics = ['Project Age', 'Activity Rate']

    collaboration_metrics = ['ContributorNumber']

    attributes = repository_attributes + activity_metrics + collaboration_metrics


    # Load data from CSV files
    df_p = pd.read_csv('inputs/metrics_ml_producer_synth.csv')
    df_c = pd.read_csv('inputs/metrics_ml_consumer_synth.csv')
    df_t = pd.read_csv('inputs/metrics_ml_Tool_synth.csv')
    df_p_c = pd.read_csv('inputs/metrics_ml_common_synth.csv')
    # Generate a unique plot
    generate_unique_plot_v2(df_p,df_c,df_t,df_p_c,attributes)

if __name__ == "__main__":
    main()