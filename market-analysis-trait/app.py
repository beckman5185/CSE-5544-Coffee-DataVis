#Audrey Beckman
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd

#read in data
coffeeSurvey= pd.read_csv("CSE-5544-Coffee-DataVis\coffee_survey.csv")

#page title
ui.page_opts(title="Market Analysis - Coffee Traits", fillable=True)

with ui.sidebar():
    #select coffee trait
    ui.input_selectize(
        "trait", "Select coffee trait",
        ['personal_preference', 'bitterness', 'acidity']
    )

    #select coffees of interest
    ui.input_checkbox_group(
        "coffee", "Select coffee blend", 
        ['coffee_a', 'coffee_b', 'coffee_c', 'coffee_d']   
    )

with ui.card():
    ui.card_header("Coffee Traits")
    @render_plotly
    def lineChart():
        import plotly.express as px
        import statistics

        #get coffees and traits chosen
        coffeeList = input.coffee()
        traitList = []
        if(len(coffeeList) > 0):
            traitList = [coffee + "_" + input.trait() for coffee in coffeeList]

        #get non-null data from survey
        ratingData = coffeeSurvey[coffeeSurvey[traitList].notnull().all(axis=1)]
        traitFrame = pd.DataFrame()

        #for each rating column
        for i in range(len(traitList)):
            #get counts for each response
            traitData = ratingData[traitList[i]].value_counts(normalize=False)
            
            #adjust into long format
            traitData = traitData.reset_index()
            traitData["coffee"] = traitList[i][0:8]
            traitData = traitData.rename(columns={traitList[i]: input.trait()})

            #add to dataframe
            traitFrame = pd.concat([traitFrame, traitData])


        if not (traitFrame.empty):
            #sort x values and colors
            traitFrame = traitFrame.sort_values(by=[input.trait(), "coffee"])

            #make line chart
            return px.line(traitFrame, y="count", x=input.trait(), color="coffee", markers=True, color_discrete_sequence=px.colors.qualitative.Set1) 






        


