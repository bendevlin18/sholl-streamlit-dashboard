import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Why manual?', 'Step 1: Selecting cells', 'Step 2: Ilastik', 'Step 3: Custom Python', 'Step 3.5: Combining output files'])

with tab1:
    st.markdown(
        """
        As an introduction, I am going to first go over the tried-and-true manual method of performing 2D sholl analysis. 
        Follow this if you want to do everything as close to manual as possible. I get it! For a first pass it is nice to work through each step of the analysis manually so you can really understand 
        
        take individual microglia selections and get raw sholl data out (i.e. # of process intersections for each concentric ring)

        There is a built-in plugin in fiji for this, but I found it to be terribly slow, needing you to wade through a set of menus, and make several clicks for every single cell/image.

        To expedite the process, I wrote a python package that works much faster. We will go over the details of that in step 2.

        """

    )


with tab2:
    st.markdown(
        """
        The first step after 

        """

    )

with tab3:
    st.markdown(
        """
        For this first manual step, we need to make a binary segmentation (that means pixels with values of ONLY 0 or 1)

        Ilastik really *excels* at this

        """

    )