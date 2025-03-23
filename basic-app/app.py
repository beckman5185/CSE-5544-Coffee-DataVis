#Audrey Beckman
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd
from pathlib import Path
coffeeSurvey= pd.read_csv(Path(__file__).parent / "coffee_survey.csv")

ui.page_opts(title="Market Analysis Interactive Visualizations", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "demographic", "Select demographic variable",
        ['age', 'gender', 'education_level', 'ethnicity_race', 'employment_status', 'number_children', 'political_affiliation']
    )

with ui.card():
    ui.card_header("Proportion")
    @render_plotly
    def proportionHeatmap():
        import plotly.express as px
        
        preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

        demographicGroups = preferenceData.groupby(input.demographic())['prefer_overall'].value_counts(normalize=True)
        demographicGroups = demographicGroups.reset_index()
        

        #overallPreference = pd.DataFrame(preferenceData['prefer_overall'].value_counts(normalize=True))
        #overallPreference[input.demographic()] = 'total'
        
        #demographicGroups = pd.concat([demographicGroups, overallPreference.reset_index()])
        demographicGroups = pd.pivot_table(demographicGroups, values='proportion', index=input.demographic(), columns='prefer_overall')

        return px.imshow(demographicGroups, color_continuous_scale="mint")

with ui.card():
    ui.card_header("Count")
    @render_plotly
    def countHeatmap():
        import plotly.express as px
        
        preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

        demographicGroups = preferenceData.groupby(input.demographic())['prefer_overall'].value_counts(normalize=False)
        demographicGroups = demographicGroups.reset_index()
        

        #overallPreference = pd.DataFrame(preferenceData['prefer_overall'].value_counts(normalize=True))
        #overallPreference[input.demographic()] = 'total'
        
        #demographicGroups = pd.concat([demographicGroups, overallPreference.reset_index()])
        demographicGroups = pd.pivot_table(demographicGroups, values='count', index=input.demographic(), columns='prefer_overall')

        return px.imshow(demographicGroups, color_continuous_scale="mint")
