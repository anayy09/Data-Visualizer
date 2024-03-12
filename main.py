import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Function to reset the values


def reset_values():
    st.session_state.display_rows = 5
    st.session_state.plot_width = 10
    st.session_state.plot_height = 6
    st.session_state.title_size = 12
    st.session_state.label_size = 10
    st.session_state.full_dataframe = False
    st.session_state.download_data = False


# Check at the start if a reset is requested
if 'reset' in st.session_state and st.session_state.reset:
    reset_values()
    st.session_state.reset = False  # Reset the flag

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered', page_icon='📊')
st.title('📊 Data Visualizer')

# Sidebar for Configuration
with st.sidebar:
    st.header("Settings")

    # Define the widgets with session_state keys
    display_rows = st.number_input('Number of rows to display', min_value=5,
                                   value=st.session_state.get('display_rows', 5), key='display_rows')
    plot_width = st.slider('Plot Width', min_value=5, max_value=20,
                           value=st.session_state.get('plot_width', 10), key='plot_width')
    plot_height = st.slider('Plot Height', min_value=5, max_value=20,
                            value=st.session_state.get('plot_height', 6), key='plot_height')
    title_size = st.slider('Title Size', min_value=10, max_value=30,
                           value=st.session_state.get('title_size', 12), key='title_size')
    label_size = st.slider('Label Size', min_value=8, max_value=25,
                           value=st.session_state.get('label_size', 10), key='label_size')
    full_dataframe = st.checkbox('Display Full Dataframe', value=st.session_state.get(
        'full_dataframe', False), key='full_dataframe')

    # Button to set the reset flag
    if st.button('Reset Settings'):
        st.session_state.reset = True
        st.experimental_rerun()  # Trigger a rerun after setting the flag

# Data File Uploader
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

# Initialization
df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = f"{working_dir}/data"
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    selected_file = st.selectbox(
        'Or, select a file from available datasets', files, index=None)

    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        df = pd.read_csv(file_path)

if df is not None:
    if full_dataframe:
        st.write(df)
    else:
        st.write(df.head(display_rows))

    columns = df.columns.tolist()
    x_axis = st.selectbox('Select the X-axis',
                          options=columns+["None"], key='x_axis')
    y_axis = st.selectbox('Select the Y-axis',
                          options=columns+["None"], key='y_axis')

    plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot',
                 'Distribution Plot', 'Count Plot', 'Box Plot', 'Heatmap']
    plot_type = st.selectbox('Select the type of plot',
                             options=plot_list, key='plot_type')

    if st.button('Generate Plot'):
        with st.spinner('Generating Plot...'):
            fig, ax = plt.subplots(figsize=(plot_width, plot_height))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'
            elif plot_type == 'Box Plot':
                sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Heatmap':
                if y_axis != "None":
                    st.warning(
                        'Heatmap uses only the X-axis for categorical data. Y-axis selection will be ignored.')
                corr = df.select_dtypes(include=['float64', 'int64']).corr()
                sns.heatmap(corr, annot=True, fmt=".2f",
                            cmap='coolwarm', ax=ax)
                plt.xticks(rotation=45)
                plt.yticks(rotation=45)

            ax.tick_params(axis='x', labelsize=label_size)
            ax.tick_params(axis='y', labelsize=label_size)
            plt.title(f'{plot_type} of {y_axis} vs {
                      x_axis}', fontsize=title_size)
            plt.xlabel(x_axis, fontsize=label_size)
            plt.ylabel(y_axis, fontsize=label_size)

            # st.pyplot(fig)
            # Save the plot to a BytesIO object and use st.image to display it
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            st.image(buf, caption='Generated Plot')

            # Provide the plot image for download
            buf.seek(0)
            st.download_button(
                label="Download the Output",
                data=buf,
                file_name="plot.png",
                mime="image/png"
            )

            plt.close(fig)  # Close the figure to free memory

            st.success('Plot Generated Successfully!')
