import pandas as pd
from shiny import reactive, render
from shiny.express import input, ui
from shinywidgets import render_plotly
from pathlib import Path
import plotly.express as px

# Add page title and sidebar
ui.page_opts(title="Spend Analysis", fillable=True)

app_dir = Path(__file__).parent.parent
print(app_dir)
coffeeSurvey = pd.read_csv(app_dir/"coffee_survey.csv")

# Data Cleaning: Drop rows with missing values in key columns
key_columns = ['total_spend', 'most_willing', 'age', 'gender', 'education_level', 'number_children', 'ethnicity_race']
cleaned_data = coffeeSurvey.dropna(subset=key_columns)

# Define ordered categories for total_spend and most_willing
spend_order = ['$20-$40', '$40-$60', '$60-$80', '$80-$100', '>$100', '<$20']
willing_order = ['Less than $2', '$2-$4', '$4-$6', '$6-$8', '$8-$10', '$10-$15', '$15-$20', 'More than $20']

# Convert to ordered categorical types
cleaned_data['total_spend'] = pd.Categorical(cleaned_data['total_spend'], categories=spend_order, ordered=True)
cleaned_data['most_willing'] = pd.Categorical(cleaned_data['most_willing'], categories=willing_order, ordered=True)

# Calculate key insights
total_participants = cleaned_data.shape[0]
most_common_spend = cleaned_data['total_spend'].mode()[0]
most_common_willing = cleaned_data['most_willing'].mode()[0]
largest_age_group = cleaned_data['age'].mode()[0]
most_common_gender = cleaned_data['gender'].mode()[0]
most_common_education = cleaned_data['education_level'].mode()[0]
most_common_ethnicity = cleaned_data['ethnicity_race'].mode()[0]

# Prepare insights dictionary
insights = {
    "Total survey participants": total_participants,
    "Most common spend range per month": most_common_spend,
    "Most common willingness to spend on a cup of coffee": most_common_willing,
    "Largest age group in the survey": largest_age_group
}

# Define function to get spend data
def get_spend_data(spendData, spend, value_type):
    inputDemographic = spend.replace(" ", "_").lower()
    if value_type == 'percentage':
        spendGroups = spendData.groupby(inputDemographic)['total_spend'].value_counts(normalize=True) * 100
        spendGroups = spendGroups.reset_index(name='percentage')
        y_label = 'percentage'
    spendGroups = spendGroups.sort_values(by=[inputDemographic, 'total_spend'])
    return spendGroups, y_label

# Create navigation with tabs
with ui.navset_tab():
    # Insights Panel
    with ui.nav_panel("Data Insights"):
        ui.markdown("## Key Insights")
        for key, value in insights.items():
            with ui.card():
                ui.markdown(f"**{key}:** {value}")

    # Bar Charts
    with ui.nav_panel("Total Spend by different variables"):
        with ui.layout_sidebar():
            with ui.sidebar():
                ui.input_selectize(
                    "spend", "Select spend variable",
                    ['Age', 'Gender', 'Education Level', 'Employment Status']
                )
                ui.input_select(
                    "value_type", "Display as:",
                    {'percentage': 'Percentage'},
                    selected='percentage'
                )

            with ui.card():
                @render_plotly
                def barGraph():
                    spendData = coffeeSurvey[coffeeSurvey['total_spend'].notnull()]
                    spend = input.spend()
                    value_type = input.value_type()

                    spendGroups, y_label = get_spend_data(spendData, spend, value_type)

                    return px.bar(
                        spendGroups, x=spend.lower().replace(" ", "_"), y=y_label, color='total_spend',
                        barmode='group', color_discrete_sequence=px.colors.qualitative.Vivid, title='Spend Analysis',
                        labels={spend.lower().replace(" ", "_"): spend, y_label: y_label.title(), 'total_spend': 'Money range'}
                    )

    # Heatmap
    with ui.nav_panel("Correlation in Spending behaviours"):
        with ui.card():
            @render_plotly
            def heatmap():
                heatmap_data = pd.crosstab(cleaned_data['total_spend'], cleaned_data['most_willing'])
                heatmap_data = heatmap_data.reindex(index=spend_order, columns=willing_order)
                fig = px.imshow(heatmap_data, title='Correlation between Spend per Month and most willing for a coffee',
                               labels={'x': 'Most Willing to Spend on a Cup of coffee', 'y': 'Total Spend Range per Month'},
                               color_continuous_scale='Viridis')
                return fig
