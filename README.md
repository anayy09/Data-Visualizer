# Data Visualizer Streamlit Web App

## Overview
This Streamlit app provides an interactive interface for data visualization. It allows users to upload their own CSV files or select from preloaded datasets to generate various types of plots, including line plots, bar charts, scatter plots, distribution plots, and more.

## Features
- **Data Upload**: Users can upload their CSV files for visualization.
- **Dataset Selection**: Users can select from the existing datasets like diabetes, heart, Parkinson's, tips, Titanic, and wine.
- **Dynamic Plotting**: Several plot types can be generated based on user input.
- **Customizable Settings**: Plot dimensions, text sizes, and the number of data rows to display can be adjusted.

## Installation
To run this app locally, you need to have Python installed on your system. Then, follow these steps:

1. Clone this repository:
```
git clone https://github.com/anayy09/Data-Visualizer.git
```

2. Navigate to the project directory:
```
cd Data-Visualizer
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Run the app:
```
streamlit run main.py
```

## Usage
Once the app is running, follow these steps to visualize your data:

1. Use the sidebar to adjust settings and choose the number of rows to display from the data.
2. Upload your CSV file or choose one from the available datasets.
3. Select the columns for the X and Y axes.
4. Choose the type of plot you wish to generate.
5. Click the 'Generate Plot' button to visualize the data.
6. Download the plot or the processed data if needed.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
