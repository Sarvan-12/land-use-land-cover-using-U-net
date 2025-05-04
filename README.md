<<<<<<< HEAD
# Land Use Land Cover Project

## Overview
This project analyzes geographical aspects of land use using annual NLCD satellite images. It includes preprocessing of images, pixel-level segmentation for detecting geographical features (e.g., water bodies, forests), trend analysis of land-use changes over time, and predictive modeling. The goal is to provide insights into how geographical aspects have evolved over the years and predict future changes.

## Project Structure
```
land_use_project/
│
├── data/
│   ├── raw/
│   │   ├── images/         # Contains the raw annual NLCD images in TIFF format
│   ├── processed/          # Processed images sorted chronologically
│   ├── analysis_results/   # Results of area calculations and aspect changes
│
├── models/
│   └── trend_predictor.pkl # Trained model for predicting trends
│
├── scripts/
│   ├── preprocess.py       # Preprocess and sort images using metadata
│   ├── analyze.py          # Analyze geographical aspects in images
│   ├── train_predictor.py  # Train model to predict future trends
│   ├── dashboard.py        # Create an interactive dashboard
│   ├── utils/
│       ├── metadata_utils.py  # Utilities for reading and processing metadata
│       └── image_utils.py     # Utilities for handling images
│
├── main.py                 # Main script to execute the project pipeline
└── requirements.txt        # Python dependencies
```

## Prerequisites
Before running the project, ensure that the following dependencies are installed:

- Python 3.x
- Pip (for installing Python packages)

You can install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

## Running the Project
Follow the steps below to run the project:

### Step 1: Prepare the Data
Ensure your raw NLCD images and corresponding metadata files are placed in the following directory structure:

```
data/
├── raw/
│   ├── region_1/
│   ├── region_2/
│   └── region_3/
```

Each region folder should contain the TIFF images.

### Step 2: Preprocess the Data
To preprocess the images and sort them chronologically based on the metadata, run the `preprocess.py` script. This will also resize the images if needed for model training.

```
python scripts/preprocess.py
```

This will organize the images into the `data/processed/` folder, sorted by year for each region.

### Step 3: Analyze the Geographical Aspects
Next, you can run the `analyze.py` script to detect geographical features (like water bodies, forests) and calculate their areas. This analysis will be saved in the `data/analysis_results/` directory.

```
python scripts/analyze.py
```

### Step 4: Train the Predictive Model
To train the model for predicting land-use trends, run the `train_predictor.py` script. This will use the processed images and analysis results to train a model saved in the `models/` directory.

```
python scripts/train_predictor.py
```

### Step 5: View the Interactive Dashboard
After running the analysis, you can create an interactive dashboard using `dashboard.py`. The dashboard will allow you to select a region and year, then display a pie chart showing the geographical aspect areas and a graph indicating trends over time.

```
python scripts/dashboard.py
```

### Step 6: Main Script
If you want to run the full pipeline (preprocessing, analysis, and model training), simply execute the `main.py` script. This will automatically call the necessary scripts in sequence.

```
python main.py
```

## Folder Structure
- `data/raw/`: Contains raw satellite images and metadata files.
- `data/processed/`: Contains processed and sorted images for training or analysis.
- `data/analysis_results/`: Stores the results of area calculations and geographical aspect detections.
- `models/`: Contains the trained model (`trend_predictor.pkl`) for predicting future trends.
- `scripts/`: Contains all the Python scripts for preprocessing, analysis, training, and dashboard creation.
- `requirements.txt`: Lists all the required Python packages.

## Dependencies
The project requires the following Python packages, which are listed in `requirements.txt`:

- numpy
- pandas
- matplotlib
- scikit-learn
- geopandas
- opencv-python
- dash (for the interactive dashboard)

Install them using:

```
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
=======
# land-use-land-cover-using-U-net
This project implements a U-Net-based deep learning model for pixel-level segmentation of satellite imagery to classify land use and land cover (LULC). It includes preprocessing, model training, and visualization to analyze changes in LULC over time.
>>>>>>> e69fea142030bafd331071b0ae7d2734363dfa2d
