import matplotlib.pyplot as plt

def generate_chart(df, column, chart_type):

    if column is None:

        return None

    fig, ax = plt.subplots()

    if chart_type == "Histogram":

        df[column].plot(
            kind='hist',
            ax=ax
        )

    elif chart_type == "Line Chart":

        df[column].plot(
            kind='line',
            ax=ax
        )

    elif chart_type == "Bar Chart":

        df[column].head(10).plot(
            kind='bar',
            ax=ax
        )

    ax.set_title(f"{chart_type} of {column}")

    return fig