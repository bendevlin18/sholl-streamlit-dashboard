import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

st.set_page_config(layout="wide")
st.title("My Microglia Morphology Journey")

tab1, tab2, tab3 = st.tabs(['Dashboard Overview', 'Sholl Explainer', 'Protocols'])

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




with tab2:
    st.markdown("""
                Sholl analysis is widely used in the field of neuroimmunology to quantify microglia process complexity. Below you can see an image representing the general pipeline for performing sholl
                1. Segment out a microglia from a larger microscope scan
                2. Create a single cell, binary representation of that cell
                3. Skeletonize the cell and plot concentric rings coming out from the soma. Calculate the number of intersections of the cell skeleton with the 
                """)
    st.image(image = "images/microglia_sholl.jpg", width=1000)
    st.markdown("""
            Sholl data is commonly plotted as "# of intersections" vs "distance from soma". Here is a really nice published example of what this data might look like, from Sipe et al., 2016. 
                Usually there are the most intersections nearest to the soma, as those are the primary branches, and then the number of intersections gradually decreases for rings that are further from the center of the cell. In the graph's case, each dot is a ring.
            """)
    st.image(image = "images/sholl_example_sipe_2016.jpg", width = 1000)

with tab3:
    st.markdown("""
                There are now several ways that one can perform sholl analysis on microscopy images. I would say the main split is between 3-dimensional (3D) vs 2D sholl.


                ***3D sholl*** can be calculated in Imaris. So I usually recommend folks do this if they've already created Imaris 3D-reconstructions of their microglia by hand for something like engulfment. There is a filament tracer plugin that can create rings and output intersections for you. 
                The protocol for doing this is beyond the scope of this dashboard, but there are plenty of tutorials available online.

                ***2D sholl*** is where the rubber hits the road. I find this to be the perfect middle-ground between speed, effectiveness, and reproducibility. (1) It is much faster to acquire images for 2D sholl than it is for 3D sholl, and you are able to get more microglia per image, (2) You can also quantify things like microglial density, or expression
                of homeostatic proteins in other channels of your images, (3) Running the sholl code is much much faster for 2D, especially if you haven't already created manual 3D reconstructions, and (4) we have internally tested and found that 2D sholl data is comparable to 3D sholl data in terms of sensitivity and reproducibility.


                If you are looking to do 2D sholl, the following are *roughly* the steps you will need to take:
                - Acquire 20X or 30X images of Iba1-labelled microglia
                - Manually (or automatically! see tab 1) segment individual microglia from each image. I usually do 3-4 microglia/image, 2-3 images/animal. This step, if done manually, is a great undergrad project!
                - Create binary segmentations of the individual microglia images
                - Run those segmentations through software that skeletonizes, plots rings, calculates and exports intersections
                - Combine any outputs for downstream analysis (usually you have one output per cell)


                In the tabs to the left, I walk through various tools I have used + developed to break down each step of this process to either be easier, faster, more reproducible, or some combination of all three. 
                At each of those steps listed above, there are a few different analysis options, and I will explain at each decision point the pros and cons of each.
                
                If you are looking to download a written protocol for this process, you can find that here
                """)
    ### download button for the full protocol
    with open("images/ilastik_for_2d_sholl.docx", 'rb') as f:
        st.download_button(label = "Download Protocol Here", data = f, file_name='ilastik_protocol.docx')