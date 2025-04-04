# Combined Market Analysis App
#Individual pages by Audrey Beckman
#Tab organization by Hansol Lee
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd
from pathlib import Path

# Read in data once for the entire app
app_dir = Path(__file__).parent.parent
coffeeSurvey = pd.read_csv(app_dir/"coffee_survey.csv")

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
                    ['Age', 'Gender', 'Education Level', 'Ethnicity Race',
                     'Employment Status', 'Number Children', 'Political Affiliation']
                )

            # Main panel content for demographics
            with ui.card():
                #proportion heatmap
                ui.card_header("Blend Preference - Proportions")
                @render_plotly
                def proportionHeatmap():
                    import plotly.express as px

                    #get non-null preference data
                    preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

                    #group by level of demographic variable
                    inputDemographic = input.demographic().replace(" ", "_").lower()
                    demographicGroups = preferenceData.groupby(inputDemographic)['prefer_overall'].value_counts(normalize=True)
                    demographicGroups = demographicGroups.reset_index()

                    #sort category values
                    demographicGroups = demographicGroups.sort_values(by=[inputDemographic, 'prefer_overall'])

                    #make grouped bar chart
                    return px.bar(demographicGroups, x=inputDemographic, y='proportion', color='prefer_overall', barmode='group', 
                                  color_discrete_sequence=px.colors.qualitative.Prism, title='Proportions of Preferred Blend by Demographic Group', 
                                  labels={ inputDemographic : input.demographic(),
                                      "proportion": "Proportion of " + input.demographic() + " Group",
                                      "prefer_overall" : "Preferred Blend"
                                      })

            with ui.card():
                #count heatmap
                ui.card_header("Blend Preference - Counts")
                @render_plotly
                def countHeatmap():
                    import plotly.express as px

                    #get non-null preference data                    
                    preferenceData = coffeeSurvey[coffeeSurvey['prefer_overall'].notnull()]

                    #group by level of demographic variable
                    inputDemographic = input.demographic().replace(" ", "_").lower()
                    demographicGroups = preferenceData.groupby(inputDemographic)['prefer_overall'].value_counts(normalize=False)
                    demographicGroups = demographicGroups.reset_index()

                    #pivot table to heatmap format
                    demographicGroups = pd.pivot_table(demographicGroups, values='count', index=inputDemographic, columns='prefer_overall')

                    #make heatmap
                    return px.imshow(demographicGroups, color_continuous_scale="algae", title="Counts of Preferred Blend by Demographic Group", 
                                     labels={'x':'Preferred Blend', 'y':input.demographic(), 'color':'# Responses'})

    # Second tab for Coffee Traits Analysis
    with ui.nav_panel("Coffee Traits"):
        with ui.layout_sidebar():
            with ui.sidebar():
                #select coffee trait
                ui.input_selectize(
                    "trait", "Select coffee trait",
                    ['Personal Preference', 'Bitterness', 'Acidity']
                )

                #select coffee blends
                ui.input_checkbox_group(
                    "coffee", "Select coffee blend",
                    ['Coffee A', 'Coffee B', 'Coffee C', 'Coffee D'],
                    selected=['Coffee A', 'Coffee B', 'Coffee C', 'Coffee D']
                )

            # Main panel content for traits
            with ui.card():
                ui.card_header("Blend Traits - Counts")
                #line chart for trait
                @render_plotly
                def lineChart():
                    import plotly.express as px

                    #get coffees and traits chosen
                    coffeeList = [name.replace(" ", "_").lower() for name in input.coffee()]
                    inputTrait = input.trait().replace(" ", "_").lower()
                    traitList = []
                    if(len(coffeeList) > 0):
                        traitList = [coffee + "_" + inputTrait for coffee in coffeeList]

                    #get non-null data from survey
                    ratingData = coffeeSurvey[coffeeSurvey[traitList].notnull().all(axis=1)]
                    traitFrame = pd.DataFrame()

                    #for each rating column
                    for i in range(len(traitList)):
                        #get counts for each response
                        traitData = ratingData[traitList[i]].value_counts(normalize=False)

                        #adjust into long format
                        traitData = traitData.reset_index()
                        traitData["coffee"] = input.coffee()[i]
                        traitData = traitData.rename(columns={traitList[i]: inputTrait})

                        #add to dataframe
                        traitFrame = pd.concat([traitFrame, traitData])


                    if not (traitFrame.empty):
                        #sort x values and colors
                        traitFrame = traitFrame.sort_values(by=[inputTrait, "coffee"])

                        #make line chart
                        return px.line(traitFrame, y="count", x=inputTrait, color="coffee",
                                       labels={'count':'# Responses', inputTrait:input.trait() + " Rating (1-5 scale)", 'coffee':'Coffee Blend'},
                                       title="Ratings of " + input.trait() + " Trait among Blends", markers=True, color_discrete_sequence=px.colors.qualitative.Set1)