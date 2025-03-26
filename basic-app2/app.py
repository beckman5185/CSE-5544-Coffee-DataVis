#Audrey Beckman
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd
from pathlib import Path
coffeeSurvey= pd.read_csv(Path(__file__).parent / "coffee_survey.csv")

ui.page_opts(title="Market Analysis Interactive Visualizations", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "trait", "Select coffee trait",
        ['personal_preference', 'bitterness', 'acidity']
    )

    ui.input_checkbox_group(
        "coffee", "Select coffee blend", 
        ['coffee_a', 'coffee_b', 'coffee_c', 'coffee_d']   
    )

with ui.card():
    ui.card_header("Count")
    @render_plotly
    def dotChart():
        import plotly.express as px
        import statistics

    
        coffeeList = input.coffee()
        traitList = []

        if(len(coffeeList) > 0):
            traitList = [coffee + "_" + input.trait() for coffee in coffeeList]


        preferenceData = coffeeSurvey[coffeeSurvey[traitList].notnull().all(axis=1)]
        
        traitFrame = pd.DataFrame()


        for i in range(len(traitList)):

            traitData = preferenceData[traitList[i]].value_counts(normalize=False)
            
            
            traitData = traitData.reset_index()
            traitData["coffee"] = traitList[i][0:8]

            traitData = traitData.rename(columns={traitList[i]: input.trait()})

            traitFrame = pd.concat([traitFrame, traitData])



        if not (traitFrame.empty):
            traitFrame = traitFrame.sort_values(by=[input.trait(), "coffee"])
            fig = px.line(traitFrame, y="count", x=input.trait(), color="coffee", markers=True, color_discrete_sequence=px.colors.qualitative.Set1) 

            return fig





        


