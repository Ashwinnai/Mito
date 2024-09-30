import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
import io

# Set page config for a wider layout and custom title/icon
st.set_page_config(page_title="Mito Spreadsheet Demo", page_icon="📊", layout="wide")

# Add custom CSS for improved UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-emotion-cache-1v0mbdj {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# App title and description
st.title("📊 Interactive Mito Spreadsheet Demo")
st.markdown("""
    This app demonstrates the power of the Mito spreadsheet component in Streamlit.
    Upload a CSV or Excel file, edit the data, perform operations, and see the results instantly!
""")

# Function to read different file types
@st.cache_data
def read_file(file):
    file_type = file.name.split('.')[-1]
    if file_type == 'csv':
        df = pd.read_csv(file)
    elif file_type in ['xls', 'xlsx']:
        df = pd.read_excel(file)
    else:
        st.error(f"Unsupported file type: {file_type}")
        return None
    return df

# File uploader
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xls', 'xlsx'])

if uploaded_file is not None:
    try:
        df = read_file(uploaded_file)
        if df is not None:
            st.success("File successfully uploaded and read!")

            # Display the Mito spreadsheet
            st.subheader("Edit Your Data")
            final_dfs, code = spreadsheet(df)

            # Display the modified data
            st.subheader("Modified Data")
            for name, dataframe in final_dfs.items():
                st.write(f"DataFrame: {name}")
                st.dataframe(dataframe)

            # Display the generated code
            st.subheader("Generated Python Code")
            st.code(code)

            # Add a download button for the modified data
            if final_dfs:
                modified_df = next(iter(final_dfs.values()))  # Get the first (and likely only) dataframe
                csv = modified_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Modified Data as CSV",
                    data=csv,
                    file_name="modified_data.csv",
                    mime="text/csv",
                )
    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
else:
    st.info("Please upload a CSV or Excel file to get started.")

# Add some helpful tips
st.sidebar.title("Tips")
st.sidebar.info("""
    - Upload a CSV or Excel file to begin
    - Double-click cells to edit values
    - Use the toolbar for various operations
    - The generated code shows the Python equivalent of your actions
    - Download the modified data using the button below the spreadsheet
""")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Mito 🚀")
