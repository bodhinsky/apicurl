import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from CSV file
""" data = pd.read_csv('experimentData.csv')

data = data.drop(columns=['issue'])
grouped_data = data.groupby('model').mean()
grouped_data = grouped_data.T
# Set the size of the plot
plt.figure(figsize=(10, 8))

# Create the heatmap
heatmap = sns.heatmap(grouped_data, annot=True, fmt=".2f", cmap='viridis', linewidths=.5)

# Add labels and title
plt.title('LLMs on SEGym')
plt.xlabel('Different LLMs')
plt.ylabel('Scoring Categories')

# Show the plot
plt.show()
 """

# Load data from CSV file
data = pd.read_csv('experimentData.csv')

# Melt the dataframe to long format
melted_data = data.melt(id_vars=['model', 'issue'], var_name='Metric', value_name='Value')

# Set the size of the plot
plt.figure(figsize=(14, 8))

# Create a grouped bar plot
g = sns.catplot(
    data=melted_data,
    kind="bar",
    x="Metric",
    y="Value",
    hue="issue",
    col="model",
    ci=None,
    palette="viridis",
    height=6,
    aspect=1
)

# Add title and adjust the layout
g.fig.suptitle('Comparison of Metrics by Issue Type for Each Model', y=1.02)
g.set_axis_labels("Metrics", "Values")
g._legend.set_title("Issue Type")

# Show the plot
plt.show()