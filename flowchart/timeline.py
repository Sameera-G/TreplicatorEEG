import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the timeline data
years = ['Year 1', 'Year 2', 'Year 3']
months = ['Months 1-4', 'Months 5-12', 'Months 13-18', 'Months 18-24', 'Months 24-30', 'Months 30-33', 'Month 36']
papers = ['Paper 1', 'Paper 2', 'Paper 3', 'Paper 4 (Optional)']

# Define the activities for each year
activities = {
    'Year 1': ['Literature Review & Data Acquisition Strategy', 'Data Collection, Preprocessing & Feature Extraction',
               'Machine Learning Model Development & Software Prototyping', 'Interim Data Analysis & Refinement'],
    'Year 2': ['Model Optimization & Software Enhancement', 'Hardware Exploration (Optional) & Edge Computing (Optional)',
               'Validation Studies (Small Group)'],
    'Year 3': ['Large-Scale Validation Studies', 'Hardware Development (Optional)', 'PhD Thesis & 4th Research Paper (Optional)']
}

# Define colors for each activity
colors = {'Literature Review & Data Acquisition Strategy': 'blue',
          'Data Collection, Preprocessing & Feature Extraction': 'orange',
          'Machine Learning Model Development & Software Prototyping': 'green',
          'Interim Data Analysis & Refinement': 'red',
          'Model Optimization & Software Enhancement': 'cyan',
          'Hardware Exploration (Optional) & Edge Computing (Optional)': 'magenta',
          'Validation Studies (Small Group)': 'yellow',
          'Large-Scale Validation Studies': 'purple',
          'Hardware Development (Optional)': 'brown',
          'PhD Thesis & 4th Research Paper (Optional)': 'grey'}

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the timeline
for i, year in enumerate(years):
    for j, activity in enumerate(activities[year]):
        ax.barh(year, left=j, width=0.8, height=0.4, color=colors[activity], align='center', edgecolor='black')

# Add paper publication labels
for i, paper in enumerate(papers):
    ax.text(7, i, paper, va='center')

# Add legend
legend_patches = [mpatches.Patch(color=color, label=activity) for activity, color in colors.items()]
ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))

# Set x-axis and y-axis ticks and labels
ax.set_xticks(range(len(months)))
ax.set_xticklabels(months)
ax.set_yticks(range(len(years)))
ax.set_yticklabels(years)

# Set title and labels
ax.set_title('Research Timeline Concept Diagram')
ax.set_xlabel('Months')
ax.set_ylabel('Years')

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Show the plot
plt.tight_layout()
plt.show()
