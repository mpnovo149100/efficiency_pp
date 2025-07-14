import pandas as pd 
import streamlit as st
#Import the data
def load_data(file_path):
    """
    Load data from a CSV file and return a DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: DataFrame containing the data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def show_graph_with_insight(title: str,
                            insight_md: str,
                            plot_func,
                            data):
    """
    Render a graph (right) with its main insight (left).

    Parameters
    ----------
    title : str
        Section title shown above the insight bullet(s)
    insight_md : str
        Markdown bullet list with the key takeaway(s)
    plot_func : callable
        Function that receives `data` and draws a Plotly figure
        (or any st.plotly_chart / st.pyplot inside)
    data : pd.DataFrame
        Filtered dataframe to feed the plot
    """
    col1, col2 = st.columns([1.2, 1.8], gap="medium")

    with col1:
        st.markdown(f"### {title}")
        st.markdown(insight_md)          # can be multiline Markdown

    with col2:
        plot_func(data)
