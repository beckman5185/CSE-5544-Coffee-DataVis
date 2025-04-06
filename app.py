import pandas as pd
from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('coffee_survey.csv')

fav_cols = ['submission_id', 'favorite']
except_fav_cols = [col for col in df.columns if col not in fav_cols]
fav = df.drop(columns=except_fav_cols)
fav = fav.groupby('favorite').count()
fav = fav.reset_index()
fav = fav.rename(columns={'submission_id':'count'})
fav = fav.sort_values(by='count')


add_cols = ['submission_id', 'additions']
except_add_cols = [col for col in df.columns if col not in add_cols]
add = df.drop(columns=except_add_cols)
add = add.rename(columns={'submission_id':'count'})

add_org = add[add['additions'] == 'No - just black']
duplicated = add[add.apply(tuple, 1).isin(add_org.apply(tuple, 1))].index

syrup = add['additions'].str.contains('Flavor syrup').sum()
milk = add['additions'].str.contains('Milk, dairy alternative, or coffee creamer').sum()
sugar = add['additions'].str.contains('Sugar or sweetener').sum()
other = add['additions'].str.contains('Other').sum()
new_rows = pd.DataFrame({'additions': ['Flavor syrup', 'Milk, dairy alternative, or coffee creamer', 'Sugar or sweetener', 'Other'], 'count': [syrup, milk, sugar, other]})

add_org = add_org.groupby('additions').count()
add_org = add_org.reset_index()
add_org = pd.concat([add_org, new_rows], ignore_index=True)
add_org = add_org.sort_values(by='count')


style_cols = ['submission_id', 'style']
except_style_cols = [col for col in df.columns if col not in style_cols]
style = df.drop(columns=except_style_cols)
style = style.groupby('style').count()
style = style.reset_index()
style = style.rename(columns={'submission_id':'count'})
style = style.sort_values(by='count', ascending=False)


roastL_cols = ['submission_id', 'roast_level']
except_roastL_cols = [col for col in df.columns if col not in roastL_cols]
roastL = df.drop(columns=except_roastL_cols)
roastL = roastL.groupby('roast_level').count()
roastL = roastL.reset_index()
roastL = roastL.rename(columns={'submission_id':'count'})
roastL = roastL.sort_values(by='count', ascending=False)

caffeine_cols = ['submission_id', 'caffeine']
except_caffeine_cols = [col for col in df.columns if col not in caffeine_cols]
caffeine = df.drop(columns=except_caffeine_cols)
caffeine = caffeine.groupby('caffeine').count()
caffeine = caffeine.reset_index()
caffeine = caffeine.rename(columns={'submission_id':'count'})
caffeine = caffeine.sort_values(by='count', ascending=False)


app_ui = ui.page_fluid(
    ui.panel_title("Coffee Taste Analysis"),
    ui.input_select("histo_plot_data", "Select Plot", {"favorite": "favorite coffee type", "additions": "additions to coffee"}),
    ui.output_plot("histo"),
    ui.input_select("pie_plot_data", "Select Plot", {"style": "coffee style", "roast": "coffee roast level", "caffeine": "caffeine level"}),
    ui.output_plot("pie")
)

def server(input, output, session):
    @render.plot
    def histo():

        fig, ax = plt.subplots()
        if (input.histo_plot_data() == "favorite"):
            colors = ['#D2B48C'] * len(fav)
            for i in range(3):
                colors[len(colors) - i - 1] = '#8B4513'

            ax.barh(fav['favorite'], fav['count'], color=colors)
            ax.set_xlabel('favorite')
            ax.set_ylabel('count')
        else:
            colors = ['#D2B48C'] * len(add_org)
            for i in range(2):
                colors[len(colors) - i - 1] = '#8B4513'
            ax.barh(add_org['additions'], add_org['count'], color=colors)
            ax.set_xlabel('additions')
            ax.set_ylabel('count')
        
        return plt.gcf()
    
    @render.plot
    def pie():
        fig, ax = plt.subplots()
        if (input.pie_plot_data() == "style"):
            percent = 100 * style["count"] / style["count"].sum()
            percent = np.around(percent, decimals=2)
            percent = percent.astype(str)
            ax.pie(style["count"], startangle=90, colors=brownGradiant(len(style)))
            ax.axis('equal')
            ax.legend(labels=style["style"] + " - " + percent + "%")
        elif (input.pie_plot_data() == "roast"):
            percent = 100 * roastL["count"] / roastL["count"].sum()
            percent = np.around(percent, decimals=2)
            percent = percent.astype(str)
            ax.pie(roastL["count"], startangle=90, colors=brownGradiant(len(roastL)))
            ax.axis('equal')
            ax.legend(labels=roastL["roast_level"] + " - " + percent + "%")
        else:
            percent = 100 * caffeine["count"] / caffeine["count"].sum()
            percent = np.around(percent, decimals=2)
            percent = percent.astype(str)
            ax.pie(caffeine["count"], startangle=90, colors=brownGradiant(len(caffeine)))
            ax.axis('equal')
            ax.legend(labels=caffeine["caffeine"] + " - " + percent + "%")
        return plt.gcf()
    
    def brownGradiant(count):
        start_color = np.array([0.976, 0.894, 0.835])
        end_color = np.array([0.545, 0.271, 0.075])
        gradient = np.linspace(end_color, start_color, count)
    
        return gradient




app = App(app_ui, server)