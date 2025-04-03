import pandas as pd
import faicons as fa
import plotly.express as px
import matplotlib.pyplot as plt
import textwrap

# Load data and compute static values
from shared import app_dir, coffee_survey, dropped_coffee_survey, multiselect_columns
from shiny import reactive, render
from shiny.express import input, ui
from shinywidgets import render_plotly

# Add page title and sidebar
ui.page_opts(title="Customer Analysis", fillable=True)

with ui.sidebar(open="desktop"):
    ui.input_checkbox_group(
        "age",
        "Age",
        ["<18","18-24","25-34","35-44","45-54","55-64",">65"],
        selected=["<18","18-24","25-34","35-44","45-54","55-64",">65"],
        inline=True,
    )

    ui.input_checkbox_group(
        "cups",
        "Cups",
        ['Less than 1', '1', '2', '3', '4', 'More than 4'],
        selected=['Less than 1', '1', '2', '3', '4', 'More than 4'],
        inline=True,
    )
    ui.input_action_button("reset", "Reset filter")

# Add main content
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    "mug": fa.icon_svg("mug-hot"),
    "age": fa.icon_svg("people-group"),
    "ellipsis": fa.icon_svg("ellipsis"),
}

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=ICONS["user"]):
        "Total survey participants"
        @render.express
        def total_survey_participants():
            coffee_survey_data().shape[0]

    with ui.value_box(showcase=ICONS["mug"]):
        "Most consuming cups of coffee per day"
        @render.express
        def consuming_cups():
            d = coffee_survey_data()
            if d.shape[0] > 0:
                most_selected = d.cups.value_counts().idxmax()
                f"{most_selected} cups"

    with ui.value_box(showcase=ICONS["age"]):
        "Biggest age group"
        @render.express
        def most_age_group():
            d = coffee_survey_data()
            if d.shape[0] > 0:
                most_selected = d.age.value_counts().idxmax()
                f"{most_selected} years old"

with ui.layout_columns(col_widths=[6, 6, 12]):
    with ui.card(full_screen=True):
        ui.card_header("Coffee survey data")
        @render.data_frame
        def table():
            return render.DataGrid(coffee_survey_data_raw())

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Frequency of multiselect column selections"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["ellipsis"]
                ui.input_radio_buttons(
                    "frequency",
                    None,
                    choices=multiselect_columns,
                    inline=True,
                )


        @render.plot
        def histogram():
            df = coffee_survey_data()
            col_for_frequency = input.frequency()
            dummies_cols = [c for c in df.columns if c.startswith(col_for_frequency + "_")]
            counts = df[dummies_cols].sum().sort_values(ascending=False)
            counts.index = counts.index.str.replace(f"{col_for_frequency}_", "")
            wrapped_labels = [textwrap.fill(label, width=10) for label in counts.index]
            plt.bar(wrapped_labels, counts.values)
            plt.title(f"Frequency of '{col_for_frequency}' Selections")
            fig, ax = plt.gcf(), plt.gca()
            return fig

    with ui.card(full_screen=True):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Cross-tabulation analysis"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["ellipsis"]
                ui.input_select(
                    "ct_right",
                    "Select base option below:",
                    {
                        "Single select": {col: col for col in [item for item in dropped_coffee_survey.columns.tolist() if item not in multiselect_columns]},
                        "Multi select": {col: col for col in multiselect_columns},
                    },
                    selected='age'
                )
                ui.input_select(
                    "ct_left",
                    "Select side option below:",
                    {
                        "Single select": {col: col for col in [item for item in dropped_coffee_survey.columns.tolist() if item not in multiselect_columns]},
                        "Multi select": {col: col for col in multiselect_columns},
                    },
                    selected='cups'
                )
                ui.input_radio_buttons(
                    "ct_right_detail",
                    "Base selection",
                    choices={"Total": "Total"},
                    inline=True
                )


        @render.plot
        def crosstab():
            df = coffee_survey_data()
            base_column = input.ct_right()
            side_column = input.ct_left()
            is_base_column_multiselect = base_column in multiselect_columns
            is_side_column_multiselect = side_column in multiselect_columns
            if is_side_column_multiselect:
                cols = [col for col in df.columns if col.startswith(f"{side_column}_")]
                grouped = df.groupby(base_column)[cols].sum()
            else:
                grouped = pd.crosstab(df[base_column], df[side_column])
            grouped_ratio = grouped.div(grouped.sum(axis=1), axis=0)
            grouped_ratio.plot(kind='bar', stacked=True, figsize=(10,6))

            plt.xticks(rotation=0)
            plt.ylabel("Proportion")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            fig, ax = plt.gcf(), plt.gca()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(True)
            ax.spines['left'].set_visible(True)
            return fig


ui.include_css(app_dir / "styles.css")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------


@reactive.calc
def data_filter():
    return (
        coffee_survey.age.isin(input.age())
        & coffee_survey.cups.isin(input.cups())
    )

def coffee_survey_data():
    return coffee_survey[data_filter()]

def coffee_survey_data_raw():
    return dropped_coffee_survey[data_filter()]


@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_checkbox_group("age", selected=["<18","18-24","25-34","35-44","45-54","55-64",">65"])
    ui.update_checkbox_group("cups", selected=['Less than 1', '1', '2', '3', '4', 'More than 4'])

@reactive.effect
def _():
    selected_ct = input.ct_right()
    df = coffee_survey
    dummies_cols = [c for c in df.columns if c.startswith(selected_ct + "_")]
    counts = df[dummies_cols].sum().sort_values(ascending=False)
    choices = ['Total'] + counts.index.str.replace(f"{selected_ct}_", "").tolist()
    ui.update_radio_buttons(
        "ct_right_detail",
        choices={choice: choice for choice in choices},
        inline=True
    )

