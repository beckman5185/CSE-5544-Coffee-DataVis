#Audrey Beckman
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd

#read in data
coffeeSurvey= pd.read_csv("CSE-5544-Coffee-DataVis\coffee_survey.csv")

#page title
ui.page_opts(title="Market Analysis - Customer Demographics", fillable=False)

#select demographic variable
with ui.sidebar():
    ui.input_selectize(
        "demographic", "Select demographic variable",
        ['age', 'gender', 'education_level', 'ethnicity_race', 'employment_status', 'number_children', 'political_affiliation']
    )

#proportion heatmap
with ui.card():
    ui.card_header("Proportion")
    @render_plotly
    def proportionHeatmap():
        import plotly.express as px
        
        #get non-null preference data
        preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

        #group by level of demographic variable
        demographicGroups = preferenceData.groupby(input.demographic())['prefer_overall'].value_counts(normalize=True)
        demographicGroups = demographicGroups.reset_index()

        #pivot table to heatmap format
        demographicGroups = pd.pivot_table(demographicGroups, values='proportion', index=input.demographic(), columns='prefer_overall')

        #make heatmap
        return px.imshow(demographicGroups, color_continuous_scale="mint")

#count heatmap
with ui.card():
    ui.card_header("Count")
    @render_plotly
    def countHeatmap():
        import plotly.express as px
        
        #get non-null preference data
        preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

        #group by level of demographic variable
        demographicGroups = preferenceData.groupby(input.demographic())['prefer_overall'].value_counts(normalize=False)
        demographicGroups = demographicGroups.reset_index()

        #pivot table to heatmap format
        demographicGroups = pd.pivot_table(demographicGroups, values='count', index=input.demographic(), columns='prefer_overall')

        #make heatmap
        return px.imshow(demographicGroups, color_continuous_scale="mint")
