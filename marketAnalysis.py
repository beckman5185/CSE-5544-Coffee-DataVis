#Audrey Beckman
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import pandas as pd

coffeeSurvey = pd.read_csv("coffee_survey.csv")

ui.page_opts(title="Penguins dashboard", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "var", "Select variable",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"]
    )
    ui.input_numeric("bins", "Number of bins", 30)

with ui.card(full_screen=True):
    @render_plotly
    def hist():
        import plotly.express as px
        return px.histogram(coffeeSurvey, x=input.var(), nbins=input.bins())