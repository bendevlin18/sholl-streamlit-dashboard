import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

st.set_page_config(layout='wide')
st.title("Manual 2D Sholl Analysis")

tab1, tab2, tab3, tab4 = st.tabs(['Why manual?', 'Step 1: Selecting cells', 'Step 2: Ilastik', 'Step 3: Custom Python'])

with tab1:
    st.markdown(
        """
        As an introduction, I am going to first go over the tried-and-true manual method of performing 2D sholl analysis.
        Follow this if you want to do everything as close to manual as possible. For a first pass it is nice to work through each step of the analysis manually so you can really understand.

        The overall goal is to take individual microglia selections and get raw sholl data out (i.e. # of process intersections for each concentric ring)

        There is a built-in plugin in fiji for this, but I found it to be terribly slow, needing you to wade through a set of menus, and make several clicks for every single cell/image.
        To expedite the process, I wrote a python package that works much faster. We will go over the details of that in step 3 on this tab.

        """
    )


with tab2:
    st.markdown("""
    The first step in this workflow is to take images of microglia (most commonly the Iba1 stain) and manually select appropriate cells to include in analysis.
    We usually do this step in Fiji/ImageJ as it is interactive and what most folks are comfortable working with.
    """)


    st.header("Fiji ROI Selection Workflow")
    st.markdown("""
    Here you are starting with probably a 20X or 30X Z-stack image of the Iba1 stain. 
    Make sure to maximum intensity project (MIP) it before selecting cells. This can be easily done using a simple FIJI macro.
                
    <u>**STEP 1.**</u> Use the (bean/freehand) selection tool in Fiji to trace a cell in the image. If you need to zoom in, use ctrl/cmd scroll wheel. If you want to pan around the image switch to the hand tool.
    """, unsafe_allow_html=True)
    st.image(image = 'images/selection_img_1.png', width = 500)
    st.markdown("""        
    <u>**STEP 2.**</u> With the selection made, use the commands <u>Ctrl + C -> Ctrl + N -> Set Size to ~500x500 + Enter -> Ctrl + V -> Ctrl + S -> Enter cell name and save.</u>
    This copies the selection (cell), creates a new empty image, pastes the selection in the new image, and saves it.
    Make sure to name the microglia selection something unique - I usually just use "cell1", "cell2" and so on. And save it as a png.
                
    ***Note:*** You will only need to set the size of the blank image for the first selection.
                Fiji should keep that as default for all future new images and you want them all to be the same size.
                500pix x 500pix should be enough for most images, but feel free to adjust as needed for your purposes.
                
                
                """, unsafe_allow_html=True)
    st.image(image = 'images/selection_img_2.png', width=500)
    st.markdown("""        
    <u>**STEP 3.**</u> Before starting with the next cell selection in the image, make sure to switch to the paintbrush tool and
                outline the cell and give it a name! Make sure that the individual
                selection image is named the same so you can match them up later on. 
                
                """, unsafe_allow_html=True)
    st.image(image = 'images/selection_img_3.png', width=500)
    st.markdown("""        
    <u>**STEP 3.**</u> From here, rinse and repeat until you have all the selections you want from that image. Don't forget to save the new, labelled full image separately as well!!
                Then open up the next image and continue making and saving selections for the rest of the dataset and all the animals.
                
                """, unsafe_allow_html=True)
    st.image(image = 'images/selection_img_4.png', width=500)
    st.header("Cell Selection Criteria")
    st.markdown("""
    Some notes about which cells to select and how many:
    1. I usually try to select around 12 cells per animal (biological replicate). This most commonly means selecting ~3 cells / image with 3 images / animal.
    2. Try to select cells that are fully in view (soma and all processes) in the maximum intensity image.
    3. Make sure that the cell is representative of other cells in the field of view in terms of brightness, general morphology, and size.
            - Sometimes this is easier said then done. Just make sure that you are completely blinded to the conditions when you are selecting these cells to prevent any bias.
            - Alternatively, you can use the unbiased, CellPose automated approach that I outline in the next tab to perform this step (1) way faster, and (2) more objective than any human.
    """)


with tab3:
    st.markdown(
        """
        Now that you have individual microglia images cropped out, the next step is to create a **binary segmentation**.
        That means producing an image where pixels have values of **ONLY 0 or 1** — background vs. cell processes. 
        To do this, I have found that ilastik is really the best tool for the job.

        [Ilastik](https://www.ilastik.org) is an image segmentation toolkit that leverages supervised machine learning (i.e. random forest classifiers) to quickly
        and interactively allow for pixel and object segmentation or "prediction" of microscopy images.
        """
    )

    st.header("Why ilastik?")
    st.markdown("""
    Its pixel classification approach handles
    staining variability well across experiments, requires minimal labeled training data, and produces clean
    binary outputs without needing to write any code.
                          
    It is out of the scope of this dashboard to write out all the steps to using Ilastik, but I have already created a detailed
    video tutorial that you can find here: [Ilastik Video Link](https://drive.google.com/drive/folders/1UP7xNpMqq3HFXKRNLDT0vq6aweMWL3bV?usp=sharing)
    
    A few small things to note:
    1. Make sure to do the pixel segmentation workflow ONLY - no need to do object segmentation.
    2. Make sure the output binary segmentation images are saved as TIFFs (note the two Ts) There should be compatibility with PNGs and JPEGs as well but TIFFs are best.         
    3. You may need to reconnect some processes in the binary segmentation images that come out from ilastik. I have done this using the paintbrush tool in Fiji in the past,
                but it is not usually necessary.
                
    It is also worth noting here that you can technically just use Fiji's threshold function for this step. Although it will be much
    much slower, less accurate, and more biased (since you will be manually adjusting each image by eye.)
    """)




with tab4:
    st.markdown("""
    With binary segmentations in hand (either from Ilastik or Fiji), we can now run them through the custom Python Sholl analysis script
    to extract the raw intersection data from each cell.
    """)

    st.header("Overview and Installation")
    st.markdown("""
    This package is a set of scripts I wrote in python for easy analysis of individual microglia images. It is interactive, asks users for input at all the right
            points, while not bogging them down with menus for every single cell. It does require <u>Python</u> to be installed and configured to use. While it is
            out of scope to give a full run down on how to download python as that is different for everyone, I can say that I recommend using the [anaconda](https://www.anaconda.com/download) or miniconda
            distributions which should download everything you need. I promise it is not too scary :D

    Once you have python installed, you will need to install the sholl analysis package that I wrote that is publicly accessible on github [here](https://github.com/bendevlin18/sholl-analysis-python).,
            There are instructions in the github readme for installation but briefly here are the steps:
                
    1. Install git on your computer if you do not already have it
                
    2. To isolate this install from any other system-level python projects, create a conda or mamba environment with python version python=3.10 using 
                
        `conda create -n sholl python=3.10`
                
        `conda activate sholl`
                
    3. Open terminal (macos) or command line (cmd on windows) and type
                
        `git clone https://github.com/bendevlin18/sholl-analysis-python.git`
    
    4. After the repository is installed on your computer, type:
                
         `cd sholl-analysis-python/sholl_analysis`
        
        `pip install --upgrade pip`
        
        `pip install -e .`
                

    If these steps all execute correctly, you should be all installed and ready to run the pipeline!
    """, unsafe_allow_html=True)

    st.header("Running the Script")
    st.markdown("""
    Run the following commands in the same terminal session:           

    `from sholl_analysis import ShollAnalyzer`
                
    `analyzer = ShollAnalyzer(start_radius=20, step_size=30, end_radius=600)`
                
    `summary = analyzer.run("/path/to/folder/with/tiffs")`
    
    In the last line, make sure to change the path strings (inside the '') to point toward your binary segmentations and where you want the output to exist.
                
    Worth noting that there are a ton of other features inherent to this python package so it is worth visiting the Github page listed above to 
    read the readme and better understand all the functions and features that you may want to use. ***I highly recommend using the pixel_size function to make sure everything
    is calculated in microns, rather than pixels. If you don't do it at this step you may need to manually convert everything by the scaling factor afterwards.***
    """)

    st.image(image = 'images/sholl_parameters.png', width=800)

    st.header("Analyzing the Output")
    st.markdown("""
    Once you have the output from the script


    """
                )

