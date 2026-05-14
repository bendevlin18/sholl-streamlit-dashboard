import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

st.set_page_config(layout='wide')
st.title("Manual 2D Sholl Analysis")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Why manual?', 'Step 1: Selecting cells', 'Step 2: Ilastik', 'Step 3: Custom Python', 'Step 3.5: Combining output files'])

with tab1:
    st.markdown(
        """
        As an introduction, I am going to first go over the tried-and-true manual method of performing 2D sholl analysis.
        Follow this if you want to do everything as close to manual as possible. I get it! For a first pass it is nice to work through each step of the analysis manually so you can really understand.

        The overall goal is to take individual microglia selections and get raw sholl data out (i.e. # of process intersections for each concentric ring)

        There is a built-in plugin in fiji for this, but I found it to be terribly slow, needing you to wade through a set of menus, and make several clicks for every single cell/image.

        To expedite the process, I wrote a python package that works much faster. We will go over the details of that in step 3 on this tab.

        """
    )


with tab2:
    st.header("Cell Selection Criteria")
    st.markdown("""
    Not every microglia in a field of view should be included in your analysis.
    Use the following criteria to decide which cells to select:
    """)

    st.info("""
    **TODO:** Fill in your selection criteria — for example:
    - Full soma must be visible (not cut off at the image edge)
    - Cell must not be overlapping with another microglia
    - Sufficient process branching to be informative
    - Any criteria specific to your staining or imaging conditions
    """)

    st.header("Fiji ROI Selection Workflow")
    st.markdown("""
    Once you have identified which cells to include, use Fiji's ROI Manager to crop and export them as individual images.
    """)

    st.info("""
    **TODO:** Add step-by-step Fiji ROI selection workflow — for example:
    1. Open your full field-of-view image in Fiji
    2. Select the Rectangle (or Freehand) tool from the toolbar
    3. Draw an ROI tightly around one microglia
    4. Press **T** to add the ROI to the ROI Manager
    5. Repeat for each qualifying cell
    6. In the ROI Manager: More → Multi Crop to export each cell as its own image
    7. Save outputs to a dedicated folder for the next step (iLastik segmentation)
    """)


with tab3:
    st.markdown(
        """
        Now that you have individual microglia images cropped out, the next step is to create a **binary segmentation**.
        That means producing an image where pixels have values of **ONLY 0 or 1** — background vs. cell processes.

        iLastik really *excels* at this step.
        """
    )

    st.header("Why iLastik?")
    st.info("""
    **TODO:** Expand on why iLastik is the right tool here — e.g., its pixel classification approach handles
    staining variability well across experiments, requires minimal labeled training data, and produces clean
    binary outputs without needing to write any code.
    """)

    st.header("Step-by-step Workflow")
    st.info("""
    **TODO:** Add iLastik workflow steps — for example:
    1. Open iLastik and start a new Pixel Classification project
    2. Load your cropped microglia images
    3. Select features (e.g., Gaussian Smoothing, Laplacian of Gaussian)
    4. Paint training labels — Label 1: cell processes, Label 2: background
    5. Train the classifier and review the probability map
    6. Iterate by adding more labels where the classifier is uncertain
    7. Export binary segmentations (threshold probability map at 0.5)
    """)


with tab4:
    st.markdown("""
    With binary segmentations in hand, we can now run them through the custom Python Sholl analysis script
    to extract the raw intersection data from each cell.
    """)

    st.header("Overview")
    st.info("""
    **TODO:** Describe the custom Python package/script — e.g.:
    - What it does: skeletonizes the binary image, places concentric rings at fixed step intervals,
      and counts how many times the skeleton crosses each ring
    - Why it is faster than the Fiji plugin
    - Installation or setup instructions
    """)

    st.header("Running the Script")
    st.info("""
    **TODO:** Add a code snippet showing how to call the script on a folder of binary segmentation images.
    Example structure:

    ```python
    # TODO: replace with actual package name and function call
    from sholl_analysis import run_sholl_batch

    run_sholl_batch(
        input_dir='path/to/binary_segmentations/',
        output_dir='path/to/sholl_outputs/',
        step_size=5,
        max_radius=200
    )
    ```
    """)

    st.header("Output Format")
    st.info("""
    **TODO:** Describe what the script outputs — one CSV per cell where columns are ring distances
    and values are intersection counts. Example:

    | image_name | 10 | 20 | 30 | 40 | ... |
    |---|---|---|---|---|---|
    | cell_001   |  3 |  7 |  5 |  2 | ... |
    """)


with tab5:
    st.header("Why This Step?")
    st.markdown("""
    After running the Sholl script you will have one output CSV per cell. Before downstream analysis
    (calculating AUC, statistical comparisons, feeding into the CNN classifier), these need to be
    combined into a single dataframe and lightly cleaned up.
    """)

    st.header("Merging Output Files")
    st.info("""
    **TODO:** Add the actual combining script used in your pipeline. Example structure:

    ```python
    import pandas as pd
    import glob

    files = glob.glob('sholl_outputs/*.csv')
    combined = pd.concat([pd.read_csv(f, index_col=0) for f in files])
    combined.to_csv('all_cells_sholl.csv')
    ```
    """)

    st.header("Post-processing & Cleanup")
    st.info("""
    **TODO:** Add any cleanup steps applied after merging — for example:
    - Trimming rings beyond the actual cell boundary (dropping trailing NaN columns)
    - Renaming or standardizing column names across experiments with different step sizes
    - Flagging or removing outlier cells (e.g., those with very low total intersection counts)
    - Normalizing ring distances if different experiments used different pixel-to-micron calibrations
    """)
