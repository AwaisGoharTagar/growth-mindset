import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed.")
            st.dataframe(df.head())

        # Fill Missing Values with Mean
        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing Values Filled with Mean.")
            st.dataframe(df.head())

        # Select Columns
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart with Dynamic Column Selection
        if st.checkbox(f"Show Chart - {file.name}"):
            numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

            if numeric_columns:
                selected_chart_columns = st.multiselect(f"Select columns to plot - {file.name}", numeric_columns, default=numeric_columns[:2])

                if selected_chart_columns:
                    st.bar_chart(df[selected_chart_columns])
                else:
                    st.warning("Please select at least one numeric column to display the chart.")
            else:
                st.warning("No numeric columns available to plot a chart.")

        # File Conversion
        format_Choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{file.name}")

        if st.button(f"Download {file.name} as {format_Choice}"):
            output = BytesIO()
            if format_Choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")

            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button(label="Download file", file_name=new_name, data=output, mime=mime)

            st.success("Processing Completed!")
