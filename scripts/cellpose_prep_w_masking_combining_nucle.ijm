// ask user to select a folder
dir = getDirectory("Select A folder");
// get the list of files (& folders) in it
fileList = getFileList(dir);
// prepare a folder to output the images
output_dir = dir + File.separator + "cellpose_Iba1_Nuclei_output" + File.separator ;
File.makeDirectory(output_dir);
thresholdMethod = "Otsu";


///HERE IS WHERE TO INPUT YOUR INFORMATION THAT MIGHT VARY BY IMAGE
USER_iba_chnl = "C2-"
USER_dapi_chnl = "C1-"
USER_file_ext = ".oir"
////







//activate batch mode
setBatchMode(true);


// LOOP to process the list of files
for (i = 0; i < lengthOf(fileList); i++) {
	// define the "path" 
	// by concatenation of dir and the i element of the array fileList
	current_imagePath = dir+fileList[i];
	// check that the currentFile is not a directory
	if (!File.isDirectory(current_imagePath)){
		print(current_imagePath);
		// open the image and split
		print("importing image");
		run("Bio-Formats Importer", "open=" + current_imagePath + " autoscale color_mode=Colorized rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
		// get some info about the image
		getDimensions(width, height, channels, slices, frames);
		// if it's a multi channel image
		print("image imported");
		run("8-bit");
		
		//Title: C4-101_1_1_MIP.czi
		max = "";
		iba_chnl = USER_iba_chnl;
		dapi_chnl = USER_dapi_chnl;
		file_ext = USER_file_ext;
		if (slices > 1){
			print("File was in 3D - converting to 2D before processing");
			run("Z Project...", "projection=[Max Intensity]");
			max = "MAX_";
			iba_chnl = iba_chnl+max;
			dapi_chnl = dapi_chnl+max;
		}
		
		
		if (channels > 1) run("Split Channels");

		// SELECTING IBA1 CHANNEL
		selectWindow(iba_chnl + fileList[i]);
		run("Enhance Contrast...", "saturated=0.35 normalize");
		run("Duplicate...", " ");
		
		// SELECTING DUPLICATE OF IBA1 CHANNEL AND APPLYING AUTOTHRESHOLD
		selectWindow(iba_chnl + fileList[i].substring(0, lengthOf(fileList[i])-4) + "-1" + file_ext);
		run("Auto Threshold", "method=" + thresholdMethod + " white");
		run("Convert to Mask");
		
		// NOW SELECTING THE DAPI CHANNEL
		selectWindow(dapi_chnl + fileList[i]);
		run("Enhance Contrast...", "saturated=0.35 normalize");
		
		// ADDING THE IBA1 MASK AND DAPI CHANNEL TOGETHER
		//imageCalculator("AND create", "C4-" + fileList[i].substring(0, lengthOf(fileList[i])-4) + "-1.czi", "C1-" + fileList[i]);
		
		imageCalculator("AND create", dapi_chnl + fileList[i],iba_chnl + fileList[i].substring(0, lengthOf(fileList[i])-4) + "-1" + file_ext);
	
		// SELECTING COMBINED COMPOSITE CHANNEL TO SAVE
		//print("c1=[Result of " + "C1-" + fileList[i] + "]" + " c2=C4-" + fileList[i] + " create");
		run("Merge Channels...", "c1=[Result of " + dapi_chnl + fileList[i] + "]" + " c2=" + iba_chnl + fileList[i] + " create keep");
		print(getInfo("window.title"));
		//selectWindow("Composite");
		saveAs("Tiff", output_dir + fileList[i]);

		// make sure to close every images befores opening the next one
		//run("Close All");
		
		print(((i/lengthOf(fileList)))*100 +"% finished");
	}
}