import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(['Dashboard Overview', 'Sholl Explainer', 'Protocol .docx download'])

with tab1:
    title_container = st.container()
    col1, col2 = st.columns([100, 20])
    with title_container:
        with col1:
            st.markdown("""
                Hello! This is the streamlit dashboard I put together to highlight my journey of finding new and efficient ways to analyze microglial morphology from confocal images.
                    
                If you are wondering what morphology is, it is basically the shape of the cell. We can quantify the shape in many ways, one of the most common ways is by using sholl analysis.
                Sholl was originally developed for measuring neuronal branch complexity and uses concentric ring intersections to assign a number (i.e. quantify)  
                    
                Microglial biologists tend to like studying cell morphology because it is a fairly straightforward way of assessing whether a cell is functioning differently.
                
                        *** NOTE: morphology =/= function. While a change in shape can be reflective of a change in cell function, 
                        one does not definitively confirm the other
                        """,
                text_alignment="left"
                )
            
        with col2:
            st.image(image = "images/black_mgla.png", width=600)
        #st.image(image = "images\\black_mgla.png", width=600)


with tab2:
    st.write('want some details here showing what sholl analysis is')

with tab3:
    ### download button for the full protocol
    #with open("images\\ilastik_for_2d_sholl.docx", 'rb') as f:
    with open("images/ilastik_for_2d_sholl.docx", 'rb') as f:
        st.download_button(label = "Download Protocol Here", data = f, file_name='ilastik_protocol.docx')