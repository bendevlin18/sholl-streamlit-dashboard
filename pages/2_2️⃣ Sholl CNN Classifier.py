import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Sholl -> Ramification Score (AUC)', 'Model Details', 'Model Performance', 'Example images', 'External Validation of AUC'])

with tab1:
    #st.image(image = 'images\\shollAUC.png')
    st.image(image = 'images/shollAUC.png')
with tab4:
    st.write('we want a scrollbar here that lets us scroll through some example images')