import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly


tab1, tab2, tab3, tab4 = st.tabs(['Why manual?', 'Step 1: Ilastik', 'Step 2: Custom Python', 'Step 2.5: Combining output files'])


with tab1:
    st.markdown(
        """
        If you find yourself here, you probably want to take individual microglia selections and get raw sholl data out (i.e. # of process intersections for each concentric ring)

        There is a built-in plugin in fiji for this, but I found it to be terribly slow, needing you to wade through a set of menus, and make several clicks for every single cell/image.

        To expedite the process, I wrote a python package that works much faster. We will go over the details of that in step 2.

        """

    )