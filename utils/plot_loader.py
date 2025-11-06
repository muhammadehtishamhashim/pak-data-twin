import plotly.graph_objects as go
import plotly.io as pio
import pickle
import json
import streamlit as st

def save_plotly_figure(fig, filename):
    """Save a Plotly figure for later use in Streamlit"""
    # Save as JSON
    fig.write_json(f"saved_plots/{filename}.json")
    
    # Save as HTML (for embedding)
    fig.write_html(f"saved_plots/{filename}.html")
    
    # Save as pickle (preserves all properties)
    with open(f"saved_plots/{filename}.pkl", 'wb') as f:
        pickle.dump(fig, f)

def load_plotly_figure(filename, format='json'):
    """Load a saved Plotly figure"""
    try:
        if format == 'json':
            with open(f"saved_plots/{filename}.json", 'r') as f:
                fig_dict = json.load(f)
            return go.Figure(fig_dict)
        
        elif format == 'pickle':
            with open(f"saved_plots/{filename}.pkl", 'rb') as f:
                return pickle.load(f)
        
        elif format == 'html':
            with open(f"saved_plots/{filename}.html", 'r') as f:
                return f.read()
    
    except Exception as e:
        st.error(f"Error loading plot: {e}")
        return None

def display_saved_plot(filename, format='json'):
    """Display a saved plot in Streamlit"""
    fig = load_plotly_figure(filename, format)
    
    if fig is not None:
        if format == 'html':
            st.components.v1.html(fig, height=600)
        else:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Could not load plot: {filename}")

# Example: Save notebook outputs
def save_notebook_analysis_results():
    """Example function to save analysis results from notebooks"""
    
    # This would be your notebook analysis results
    results = {
        'gdp_forecast': [400, 420, 440, 460, 480],  # Example forecast
        'export_trend': 'increasing',
        'correlation_matrix': [[1.0, 0.8], [0.8, 1.0]],
        'key_insights': [
            "GDP shows steady growth",
            "Exports are highly correlated with GDP",
            "Seasonal patterns detected in monthly data"
        ]
    }
    
    # Save results
    with open('saved_analysis/economic_analysis_results.pkl', 'wb') as f:
        pickle.dump(results, f)
    
    return results

def load_notebook_analysis_results():
    """Load saved analysis results"""
    try:
        with open('saved_analysis/economic_analysis_results.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None