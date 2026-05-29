import gradio as gr
import pandas as pd

from utils.data_loader import load_data
from utils.llm_helper import ask_llm
from utils.charts import generate_chart
from utils.insights import dataset_summary


# Global dataframe
df = None


# Upload and preview dataset
def upload_file(file):

    global df

    if file is None:
        return None, "Please upload a file."

    df = load_data(file)

    preview = df.head()

    info = f"""
Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column Names:
{list(df.columns)}
"""

    return preview, info


# Get numeric columns
def get_numeric_columns():

    global df

    if df is not None:

        numeric_cols = df.select_dtypes(
            include='number'
        ).columns.tolist()

        return gr.update(
            choices=numeric_cols,
            value=numeric_cols[0] if numeric_cols else None
        )

    return gr.update(
        choices=[],
        value=None
    )


# Ask AI question
def ask_question(question):

    global df

    if df is None:
        return "Please upload dataset first."

    if not question:
        return "Please enter a question."

    columns = ", ".join(df.columns)

    sample_data = df.head(5).to_string()

    prompt = f"""
You are an expert data analyst.

Dataset columns:
{columns}

Sample dataset:
{sample_data}

User question:
{question}

Give clear and professional business insights.
"""

    answer = ask_llm(prompt)

    return answer


# Generate dataset summary
def generate_summary():

    global df

    if df is None:
        return "Please upload dataset first."

    return dataset_summary(df)


# Generate chart
def create_chart(column, chart_type):

    global df

    if df is None:
        return None

    if column is None:
        return None

    fig = generate_chart(
        df,
        column,
        chart_type
    )

    return fig


# -----------------------------
# GRADIO UI
# -----------------------------

with gr.Blocks() as demo:

    gr.Markdown("# 📊 AI Data Analyst")

    gr.Markdown(
        "Upload CSV/Excel files and ask AI questions about your data."
    )

    # =========================
    # Upload Section
    # =========================

    with gr.Row():

        file_input = gr.File(
            label="Upload CSV or Excel File"
        )

    upload_btn = gr.Button(
        "Load Dataset"
    )

    preview_output = gr.Dataframe(
        label="Dataset Preview"
    )

    info_output = gr.Textbox(
        label="Dataset Information",
        lines=8
    )

    # Hidden initially
    column_dropdown = gr.Dropdown(
        label="Select Numeric Column",
        choices=[],
        render=False
    )

    # Upload button action
    upload_btn.click(
        upload_file,
        inputs=file_input,
        outputs=[
            preview_output,
            info_output
        ]
    ).then(
        get_numeric_columns,
        outputs=column_dropdown
    )

    # =========================
    # Summary Section
    # =========================

    gr.Markdown("## 📌 Dataset Summary")

    summary_output = gr.Textbox(
        label="Summary",
        lines=12
    )

    summary_btn = gr.Button(
        "Generate Summary"
    )

    summary_btn.click(
        generate_summary,
        outputs=summary_output
    )

    # =========================
    # AI Question Section
    # =========================

    gr.Markdown("## 🤖 Ask Questions About Your Data")

    question_input = gr.Textbox(
        label="Enter Your Question",
        placeholder="Example: Show sales trend by month"
    )

    ask_btn = gr.Button(
        "Ask AI"
    )

    answer_output = gr.Textbox(
        label="AI Answer",
        lines=8
    )

    ask_btn.click(
        ask_question,
        inputs=question_input,
        outputs=answer_output
    )

    # =========================
    # Chart Section
    # =========================

    gr.Markdown("## 📈 Generate Charts")

    # Render dropdown HERE
    column_dropdown.render()

    chart_dropdown = gr.Dropdown(
        choices=[
            "Histogram",
            "Line Chart",
            "Bar Chart"
        ],
        label="Select Chart Type",
        value="Histogram"
    )

    chart_btn = gr.Button(
        "Generate Chart"
    )

    chart_output = gr.Plot()

    chart_btn.click(
        create_chart,
        inputs=[
            column_dropdown,
            chart_dropdown
        ],
        outputs=chart_output
    )


# Launch app
demo.launch()