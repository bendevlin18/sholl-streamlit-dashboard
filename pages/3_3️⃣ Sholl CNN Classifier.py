import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import statsmodels.api as sm
st.set_page_config(layout = 'wide')
st.title("Conv. Neural Network For Predicting Microglia Morphology Scores")


testdata = pd.read_csv('data/test_dataset_preds_jan7.csv').sort_values(by = 'val_trues')
data2 = pd.read_csv('data/julia_images_preds_jan7.csv')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Sholl -> Ramification Score (AUC)', 'Model Details', 'Model Performance', 'Example images', 'External Validation of AUC'])

with tab1:
    st.markdown("""
                The first thing to do when it came to predicting ramification was to somehow turn sholl output (which is a curve of points representing each concentric ring and its intersections)
                into a single value that can be fed into the classifier. For this, I chose a simple area under the curve (AUC) calculation, which just takes the sum of all the area under the line that is
                created between the points (see graphic below). To calculate AUC this is the code used:
                    
                    from sklearn.metrics import auc
                    image_name = []
                    ramification_val = []
                    for i in range(len(df)):   
                        ramification = auc(df.columns[0:-2].astype('int'), np.nan_to_num(df.iloc[i].values[0:-2], nan = 0))  
                        image_name = np.append(image_name, df.iloc[i].name.split(' ')[0].split('_Simple')[0])
                        ramification_val = np.append(ramification_val, ramification)

                This AUC was normalized to total possible area because our dataset consisted of 7+ independent experiments, all of which had different ring sizes and outer diameters. To do so, I just simply
                divided the auc by total auc range (calculated by last ring diameter - initial ring diameter, code below)

                    auc_range = int(df.columns[-3]) - int(df.columns[0])
                    normalized_auc = output_df / auc_range
                

                In total, we had over 1600 individual microglia images represented in this dataset. With 1100 included in training and another 400 included in the test/validation set.

                """)
    st.image(image = 'images/shollAUC.png')

with tab2:
    st.header('Step 1')
    st.markdown("""

                Before training a CNN on our dataset, we needed to downsample the images to a reasonable size (244pix x 244pix). To do this, I used a fiji macro, 
                although it is probably easy to do it in native python as well.

                    // LOOP to process the list of files
                    for (i = 0; i < lengthOf(fileList); i++) {
                        // define the "path" 
                        // by concatenation of dir and the i element of the array fileList
                        current_imagePath = dir+fileList[i];
                        print(fileList[i]);
                        currentImage_name = fileList[i];
                        
                        // basic if statement to make sure we are not including any directory folders in this loop
                        // otherwise it will error out :(
                        if (!File.isDirectory(current_imagePath)){

                            // open the image
                            // open(current_imagePath);
                            print("importing image");
                            open(current_imagePath);
                            run("downsample ", "width=244 height=244 source=0.50 target=0.50");
                            saveAs("png", output_dir+currentImage_name+"_downsample");
                            close("*");
                    }
                    }
                """)
    
    st.markdown("""
                If you would like to download this fiji macro for your own use, you can click the button below
                """)

    with open("scripts/batch_downsampling.ijm", 'rb') as f:
        st.download_button(label = "Download Fiji Macro Here", data = f, file_name='batch_downsampling_fiji_macro.ijm')

    st.header('Step 2')
    st.markdown("""
                I tested just a conventional CNN that comes with PyTorch as well as the [ConvNext_tiny](https://huggingface.co/timm/convnext_tiny.fb_in22k) CNN model from PyTorch timm. After some A/B testing it seemed like the ConvNext was going to be a slightly better option, especially if
                it was run with many epochs. For final training, I used 50 epochs and used mean absolute error (MAE -> nn.L1Loss()) as the loss function. The code snippet is below

                    import torch
                    from torch.utils.data import DataLoader

                    model = build_model().cuda()
                    epochs = 50

                    criterion = nn.L1Loss()  # MAE is often better for morphology
                    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5, weight_decay=1e-4)
                    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

                    for epoch in range(epochs):
                        model.train()
                        train_loss = 0
                        for imgs, scores in train_loader:
                            imgs, scores = imgs.cuda(), scores.unsqueeze(1).cuda()

                            pred = model(imgs)
                            loss = criterion(pred, scores)

                            optimizer.zero_grad()
                            loss.backward()
                            optimizer.step()
                            scheduler.step()

                            train_loss += loss.item()
                        
                        print(f"Epoch {epoch} | Train MAE: {train_loss/len(train_loader):.3f}")

                        # validation
                        model.eval()
                        val_loss = 0
                        with torch.no_grad():
                            for imgs, scores in val_loader:
                                imgs, scores = imgs.cuda(), scores.unsqueeze(1).cuda()
                                pred = model(imgs)
                                loss = criterion(pred, scores)
                                val_loss += loss.item()

                        print(f"   Val MAE: {val_loss/len(val_loader):.3f}")
                

                If you would like to download the full script used to train and subsequently validate the model, click the button below

                """)
    
    with open("scripts/running_eval_mgla_morph_CNN.ipynb", 'rb') as f:
        st.download_button(label = "Download CNN Training Script", data = f, file_name='mgla_morph_CNN_training_script.ijm')

    


with tab3:
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown("""
                    Here I've printed the first five columns of the model output data table that contains information about 


                    """)
        st.write(testdata.head())
        fig = px.scatter(testdata, x='val_trues', y='val_preds', hover_data = ['imageID'], trendline="ols", title = 'Model Predictions v. Ground Truth AUC for Test Images <br><sup>MAE: 0.3949 | MSE: 0.2217 | R2: 0.8993</sup>')
        st.plotly_chart(fig, theme="streamlit")

        testdatares = testdata.copy()
        testdatares['residual'] = testdatares['val_trues'] - testdatares['val_preds']

        fig2 = px.scatter(testdatares, x='val_preds', y='residual', marginal_y='violin', trendline='ols', title = 'Residuals Plot')
        st.plotly_chart(fig2, theme="streamlit")

        st.markdown("""
                    We also ran Gradient-weighted Class Activation Mapping ([GradCam](https://arxiv.org/abs/1610.02391)) on all the images to get a sense of where the important regions were in the images for the classifier to make its prediction.
                    To see the GradCam results on a per-cell basis, scroll down to the bottom of the page in the next tab while exploring through the cells in the dataset.
                    """)
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("images/gradcam/2.2_exp36.png_overlay.png")
            st.caption("Example GradCam Heatmap")



with tab4:
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.header('Scroll through the images Small -> Large', text_alignment = 'center')
        st.subheader('To compare model predictions with images', text_alignment = 'center')
        st.markdown('Scroll down to see grabcam outputs which show where the model attended to when making the prediction', text_alignment = 'center')
        col1, col2 = st.columns(2)
        with col1:
            image = st.select_slider(label = '', options = testdata['imageID'])
            st.write(testdata[testdata['imageID'] == image])
            st.image('images/mgla/' + image, width = 'stretch')
            st.caption(image)
            fig = px.scatter(testdata, x='val_trues', y='val_preds', hover_data = ['imageID'], trendline="ols", opacity = 0.2)
            fig.add_traces(px.scatter(testdata[testdata['imageID'] == image], x='val_trues', y='val_preds').update_traces(marker_size=15, marker_color="orange").data)
            st.plotly_chart(fig, theme="streamlit", key = 3)

            try: 
                st.image('images/gradcam/' + image + '_overlay.png', width = 'stretch')
                st.caption("Gradcam results for "+ image)
            except:
                st.write('GradCAM results unavailable')
        
        with col2:
            image2 = st.select_slider(label = '', options = testdata['imageID'], key = 2)
            st.write(testdata[testdata['imageID'] == image2])
            st.image('images/mgla/' + image2, width = 'stretch')
            st.caption(image2)
            fig = px.scatter(testdata, x='val_trues', y='val_preds', hover_data = ['imageID'], trendline="ols", opacity = 0.2)
            fig.add_traces(px.scatter(testdata[testdata['imageID'] == image2], x='val_trues', y='val_preds').update_traces(marker_size=15, marker_color="orange").data)
            st.plotly_chart(fig, theme="streamlit", key = 4)

            try: 
                st.image('images/gradcam/' + image2 + '_overlay.png', width = 'stretch')
                st.caption("Gradcam results for "+ image2)
            except:
                st.write('GradCAM results unavailable')
    
with tab5:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.markdown("""
                    I wanted to validate that AUC is a good single datapoint representing morphology differences that would normally be captured by full sholl analysis.
                    To do so, I took two known datasets from the lab that had shown a significant difference via sholl in the past. I calculated raw AUC (straight from sholl output)
                    and put the cells through the classifier to 'predict' AUC.



                    """)
        st.image('images/blocking_ab_AUC_validation.jpg')
        st.image('images/KO_AUC_validation.jpg')
    