# Combined Market Analysis App
#Individual pages by Audrey Beckman
#Tab organization by Hansol Lee
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd

# Read in data once for the entire app
coffeeSurvey = pd.read_csv("CSE-5544-Coffee-DataVis/coffee_survey.csv")

# Page title and settings
ui.page_opts(title="Coffee Market Analysis", fillable=True)

# Create navigation with tabs
with ui.navset_tab():
    # First tab for Demographics Analysis
    with ui.nav_panel("Customer Demographics"):
        with ui.layout_sidebar():
            with ui.sidebar():
                #select demographic variable
                ui.input_selectize(
                    "demographic", "Select demographic variable",
                    ['age', 'gender', 'education_level', 'ethnicity_race',
                     'employment_status', 'number_children', 'political_affiliation']
                )

            # Main panel content for demographics
            with ui.card():
                #proportion heatmap
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

            with ui.card():
                #count heamap
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

    # Second tab for Coffee Traits Analysis
    with ui.nav_panel("Coffee Traits"):
        with ui.layout_sidebar():
            with ui.sidebar():
                #select coffee trait
                ui.input_selectize(
                    "trait", "Select coffee trait",
                    ['personal_preference', 'bitterness', 'acidity']
                )

                #select coffee blends
                ui.input_checkbox_group(
                    "coffee", "Select coffee blend",
                    ['coffee_a', 'coffee_b', 'coffee_c', 'coffee_d'],
                    selected=['coffee_a', 'coffee_b', 'coffee_c', 'coffee_d']
                )

            # Main panel content for traits
            with ui.card():
                ui.card_header("Coffee Traits")
                #line chart for trait
                @render_plotly
                def lineChart():
                    import plotly.express as px

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
                        return px.line(traitFrame, y="count", x=input.trait(), color="coffee",
                                       markers=True, color_discrete_sequence=px.colors.qualitative.Set1)