import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Load the CSV file
df = pd.read_csv('consumer_libraries_count.csv')

# Check if the CSV contains the expected columns
if 'library' not in df.columns or 'count' not in df.columns:
    raise ValueError("CSV file must contain 'library' and 'count' columns")

# Sort the dataframe by 'count' in descending order and get the top 10
df_top10 = df.sort_values(by='count', ascending=False).head(10)

# Normalize sizes to prevent very small boxes
min_size_threshold = 0.05 * df_top10['count'].sum()
df_top10['adjusted_count'] = df_top10['count'].apply(lambda x: max(x, min_size_threshold))

# Prepare data for the treemap
labels = [f"{library}\n({count})" for library, count in zip(df_top10['library'], df_top10['count'])]
sizes = df_top10['adjusted_count']

# Define specific colors for each library for consumers
library_colors = {
    'keras': "#E69F00",        # Dark orange
    'tensorflow': "#56B4E9",   # Dark blue
    'torch': "#009E73",        # Dark green
    'sklearn': "#c0c422",      # Yellow
    'mxnet': "#0072B2",        # Blue
    'xgboost': "#D55E00",      # Red
    'tensorpack': "#CC79A7",   # Pink
    'transformers': "#999999", # Gray
    'stable_baselines': "#882255",     # Dark purple
    'lightgbm': "#44AA99"      # Teal
}


# Assign colors based on the library
colors = [library_colors.get(library, "#333333") for library in df_top10['library']]

# Create a treemap
plt.figure(figsize=(12, 8))
squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=.8,
    text_kwargs={'fontsize': 22, 'color': 'white', 'weight': 'bold'}
)
plt.axis('off')
plt.tight_layout()
# Show the plot

plt.savefig('consumer_libraries_treemap.pdf')
