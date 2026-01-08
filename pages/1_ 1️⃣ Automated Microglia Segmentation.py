import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly

st.set_page_config(layout = 'wide')
st.title("Automated Microglia Segmentation with SAM")
tab1, tab2, tab3, tab4 = st.tabs(['SAM Overview', 'Image Details', 'Running Cellpose-SAM', 'Performance Example'])


with tab1:
    st.markdown("""

                There are now a lot of different options popping up for doing automated image segmenation using the Segment Anything Model.
            
                This is a CNN that was originally trained by Meta on over 11 million images


                """,
                
                text_alignment="left")
    
    st.image('images/SAM.png', width = 1200)



with tab2:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.markdown("""
            The cellpose algorithm works with multiple image types, but I have found the best performance to be with 2048x2048 pixel density
            Since the model downsamples, this gives each cell enough pixels to be picked up by the classifier.
                    
            Below is an example of what the Iba1 stain might look like between the 1024 resolution (right) and 2048 resolution (left)
            
            """,
            text_alignment="left"
            )

        st.image('images/1024v2048.png', width = 'stretch')

        st.markdown("""
                It is helpful to also have a DAPI channel imaged so that you can overlay it with the Iba1 channel
                This drastically helps cellpose predicts its "flows" which are the unique feature where it predicts processes radiating out from the soma/cell body
                To preprocess any images I've made a fiji macro that requires just a few user inputs:

                        USER_iba_chnl = "C2-"
                        USER_dapi_chnl = "C1-"
                        USER_file_ext = ".oir"
                        
                    
                    To download the macro click the button below
                    """)
        with open("scripts/cellpose_prep_w_masking_combining_nucle.ijm", 'rb') as f:
            st.download_button(label = "Cellpose Prep Fiji Macro", data = f, file_name='cellpose_prep_fiji_macro.ijm')
    


with tab3:
    st.markdown("""

                I have added four new functions to the standalone Cellpose-SAM package that assist in exporting individual cells, and an annotated image of masks with cell labels

                1. Modified show segmentation:
                    
                        def show_segmentation_modified(fig, img, maski, flowi, channels=[0, 0], file_name=None):

                            ax = fig.add_subplot(1, 4, 1)
                            img0 = img.copy()
                            if img0.shape[0] < 4:
                                img0 = np.transpose(img0, (1, 2, 0))
                            if img0.shape[-1] < 3 or img0.ndim < 3:
                                img0 = image_to_rgb(img0, channels=channels)
                            else:
                                if img0.max() <= 50.0:
                                    img0 = np.uint8(np.clip(img0, 0, 1) * 255)
                            ax.imshow(img0)
                            ax.set_title("original image")
                            ax.axis("off")

                            outlines = utils.masks_to_outlines(maski)
                            overlay = mask_overlay(img0, maski)

                            if file_name is not None:
                                save_path = os.path.splitext(file_name)[0]
                                io.imsave(save_path + "_overlay.jpg", overlay)
                
                2. Export Segmented Images:
                    
                        def export_segmented_images(img):
                            
                            selected_channels = []
                            for i, c in enumerate([first_channel, second_channel, third_channel]):
                                if c == 'None':
                                    continue
                                if int(c) > img.shape[0]:
                                    assert False, 'invalid channel index, must have index greater or equal to the number of channels'
                                if c != 'None':
                                    selected_channels.append(int(c))

                            img_selected_channels = np.zeros_like(img)
                            img_selected_channels[:, :, :len(selected_channels)] = img[:, :, selected_channels]
                            fig = plt.figure(figsize=(12,5))
                            show_segmentation_modified(fig, img, masks, flows[0], file_name=f)
                

                3. Mask Filter:
                    
                        def mask_filter_fixed(masks, pix_size):
                            for msk in np.unique(masks):
                                if np.where(masks == msk)[1].shape[0] > pix_size:
                                    pass
                                elif np.where(masks == msk)[1].shape[0] < pix_size:
                                    rows, cols = np.where(masks == msk)
                                    masks[rows, cols] = 0
                            return masks
                
                4. Save Segmentation Image with Labelled Masks (cellIDs)
                
                        def save_segmentation_img_w_mask_ns_fixed(img, maski, file_name, odir):

                            img0 = img.copy()
                            if img0.shape[0] < 4:
                                img0 = np.transpose(img0, (1, 2, 0))
                            #if img0.shape[-1] < 3 or img0.ndim < 3:
                                #img0 = image_to_rgb(img0, channels=[0, 0])
                            else:
                                if img0.max() <= 50.0:
                                    img0 = np.uint8(np.clip(img0, 0, 1) * 255)
                            z = mask_overlay(img0, maski)
                            
                            my_dpi = 300
                            plt.figure(figsize=(np.shape(img)[1]/my_dpi, np.shape(img)[2]/my_dpi), dpi = my_dpi)
                            plt.axis("off")
                            plt.imshow(z)    
                            for cell in np.unique(masks):
                                y, x = np.where(masks == cell)
                                plt.text(int(np.median(x)), int(np.median(y)), str(cell), color="white", fontsize=4)
                            plt.savefig(os.path.join(odir, str(file_name).split('_MIP')[0].split("\\")[1] + "_labelled_segmentations" + '.png'), dpi=my_dpi, bbox_inches = "tight")
                            plt.close()
                

                To actually run the code, the following block is executed. 
                I have found that these parameters (the first 5 lines) work really well for this model
                They have been optimized for 20X images at 2048x2048 resolution (i.e. images from the zeiss)
                It should work for 1024x1024 images taken on the confocal but will likely need to reduce the diameter by half or a little less than half (i.e. 250)

                        PARAMS
                        flow_threshold = 3
                        cellprob_threshold = -4
                        tile_norm_blocksize = 0
                        diam = 375
                        niterations = 3000

                        masks_ext = ".png" if image_ext == ".png" else ".tif"
                        for i in trange(len(files)):
                            f = files[i]
                            img = io.imread(f)
                            masks, flows, styles = model.eval(img, batch_size=32, diameter = diam, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold,
                                                        normalize={"tile_norm_blocksize": tile_norm_blocksize}, niter=niterations)
                        
                            masks = mask_filter_fixed(masks, pix_size = 5000)
                            io.imsave(dir / (f.stem + "_masks" + masks_ext), masks)
                            output_dir = str(f).split('\\')[1].split('.')[0] + '_outputs'

                            os.mkdir(output_dir)
                            print(output_dir + " making folder")

                            save_segmentation_img_w_mask_ns_fixed(img, masks, file_name = f, odir = output_dir)

                            for cell in np.unique(masks):
                                if cell > 0:
                                    x, y = np.where(masks == cell)
                                    cropped = img[1][x.min():x.max(), y.min():y.max()]
                                    try:
                                        cv2.imwrite(os.path.join(output_dir, str(f).split('_MIP')[0].split("\\")[1] + "_cell_" + str(cell) + '.png'), cropped)
                                    except:
                                        pass
                

                
                If you'd like to download my entire jupyter notebook to see the whole script, click the download button below

                """)
    with open("scripts/running_the_model.ipynb", 'rb') as f:
        st.download_button(label = "Cellpose Jupyter Notebook", data = f, file_name='running_cellpose.ipynb')



with tab4:
    col1, col2, col3 = st.columns([7, 1, 1])
    with col1:
        st.markdown("""
                    Here are some examples of what it outputs if you set the parameters correctly
                    """,
                    text_alignment="left")
        st.image('images/cellpose_sample_output.png', width = 'stretch')


