import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly


tab1, tab2, tab3 = st.tabs(['SAM Overview', 'Image Details', 'Performance Example'])


with tab1:

    st.markdown("""

            There are now a lot of different options popping up for doing automated image segmenation using the Segment Anything Model.
            
            This is a CNN that was originally trained by Meta on over 11 million images


                """,
                
                text_alignment="left")
    
    st.image('images\\SAM.png', width = 1200)



with tab2:
    st.markdown("""
        The cellpose algorithm works with multiple image types, but I have found the best performance to be with 2048x2048 pixel density
        Since the model downsamples, this gives each cell enough pixels to be picked up by the classifier.
                
        Below is an example of what the Iba1 stain might look like between the 1024 resolution (right) and 2048 resolution (left)
        
        """,
        text_alignment="center"
        )

    st.image('images\\1024v2048.png', width = 'stretch')


with tab3:

    st.markdown("""
                Here are some examples of what it outputs if you set the parameters correctly
                """,
                text_alignment="left")
    
    st.image('images\\cellpose_sample_output.png', width = 'stretch')


    st.markdown("""
                
                
                
                I added some additional code that saves all the microglia as separate image files.

                This becomes useful for putting into either the 2️⃣ Sholl CNN Classifier or 3️⃣ Manual Sholl for finishing the analysis
                """,
                text_alignment="left")

