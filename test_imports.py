#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

try:
    import sys
    print(f"Python version: {sys.version}")
    
    import streamlit as st
    print("✅ Streamlit imported successfully")
    
    import pandas as pd
    print("✅ Pandas imported successfully")
    
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    print("✅ Plotly imported successfully")
    
    import numpy as np
    print("✅ NumPy imported successfully")
    
    # Test our local imports
    sys.path.insert(0, '.')
    from src.data_loader import load_all_data
    from src.config import DASHBOARD_INDICATORS
    from src.charts import create_plot_type, get_kpi_value
    print("✅ Local modules imported successfully")
    
    print("\n🎉 All imports successful! The app should work.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")