import gradio as gr
import pickle
import pandas as pd
from theme import Seafoam

# Load models
with open('models/model_xgb.pkl', 'rb') as f:
    heart_model = pickle.load(f)
    
seafoam = Seafoam()

def predict_heart_disease(Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, 
                         RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope):
    data = {
        'Age': [float(Age)],
        'Sex': [1 if Sex == 'Male' else 0],
        'RestingBP': [float(RestingBP)],
        'Cholesterol': [float(Cholesterol)],
        'FastingBS': [1 if FastingBS == 'Yes' else 0],
        'MaxHR': [float(MaxHR)],
        'ExerciseAngina': [1 if ExerciseAngina == 'Yes' else 0],
        'Oldpeak': [float(Oldpeak)],
        'ChestPainType_ASY': [1 if ChestPainType == 'ASY' else 0],
        'ChestPainType_ATA': [1 if ChestPainType == 'ATA' else 0],
        'ChestPainType_NAP': [1 if ChestPainType == 'NAP' else 0],
        'ChestPainType_TA': [1 if ChestPainType == 'TA' else 0],
        'ST_Slope_Down': [1 if ST_Slope == 'Down' else 0],
        'ST_Slope_Flat': [1 if ST_Slope == 'Flat' else 0],
        'ST_Slope_Up': [1 if ST_Slope == 'Up' else 0],
        'RestingECG_LVH': [1 if RestingECG == 'LVH' else 0],
        'RestingECG_Normal': [1 if RestingECG == 'Normal' else 0],
        'RestingECG_ST': [1 if RestingECG == 'ST' else 0]
    }
    df_input = pd.DataFrame(data)
    prediction = heart_model.predict(df_input)
    result = "Hasta" if prediction[0] == 1 else "Sağlıklı"
    html_result = f"<div class='result-box {result.lower()}'>{result}</div>"
    return html_result

def predict_diabetes(Age, BMI, Glucose, BloodPressure, Insulin, DiabetesPedigree):
    result = "Hasta"  # Placeholder result
    html_result = f"<div class='result-box {result.lower()}'>{result}</div>"
    return html_result

def predict_cancer(Age, TumorSize, LymphNodes, Malignancy, CellShape, CellSize):
    result = "Sağlıklı"  # Placeholder result
    html_result = f"<div class='result-box {result.lower()}'>{result}</div>"
    return html_result

with gr.Blocks(theme=seafoam) as demo:
    # Add custom CSS for styling
    gr.HTML(
        """
        <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #1a1c1f;
        }
        .gradio-container {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            max-width: none !important;
            background-color: #1a1c1f;
        }
        #main-container {
            border: none;
            border-radius: 0;
            box-shadow: none;
            background-color: #1a1c1f;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }
        .tabs {
            background-color: #1a1c1f;
            border: none;
            box-shadow: none;
        }
        .tab-nav {
            background-color: #1a1c1f;
            border: none;
            padding: 1rem 0;
        }
        #centered-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #1a1c1f;
            border: none;
        }
        .form-container {
            background-color: #2d3339;
            padding: 2rem;
            border-radius: 10px;
            margin-top: 1rem;
        }
        .result-box {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            margin: 20px auto;
            border-radius: 10px;
            max-width: 300px;
            color: white;
        }
        .hasta {
            background-color: #dc3545;
        }
        .sağlıklı {
            background-color: #28a745;
        }
        .gr-button {
            min-width: 200px;
            margin: 10px auto;
            display: block;
            background-color: #3d4752;
            border: none;
        }
        .gr-button:hover {
            background-color: #4a5562;
        }
        .gr-form {
            border: none;
            background-color: transparent;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        /* Input styling */
        .gr-input, .gr-dropdown, .gr-slider {
            background-color: #3d4752 !important;
            border: none !important;
            color: white !important;
        }
        .gr-input:focus, .gr-dropdown:focus {
            border: 1px solid #4a5562 !important;
        }
        /* Label styling */
        label {
            color: #e0e0e0 !important;
        }
        /* Markdown styling */
        .markdown-text {
            color: #e0e0e0 !important;
            text-align: center;
        }
        </style>
        """
    )

    with gr.Tabs() as tabs:
        # Heart Disease Tab
        with gr.Tab("Heart Disease Prediction"):
            with gr.Column(elem_id="centered-container"):
                gr.Markdown("# Heart Disease Prediction", elem_classes="markdown-text")
                
                with gr.Group(elem_classes="form-container"):
                    heart_age = gr.Number(label="Age")
                    heart_sex = gr.Dropdown(choices=["Male", "Female"], label="Sex")
                    heart_chest_pain = gr.Dropdown(choices=["ATA", "ASY", "NAP", "TA"], label="Chest Pain Type")
                    heart_resting_bp = gr.Number(label="Resting Blood Pressure")
                    heart_cholesterol = gr.Number(label="Cholesterol")
                    heart_fasting_bs = gr.Dropdown(choices=["Yes", "No"], label="Fasting Blood Sugar")
                    heart_resting_ecg = gr.Dropdown(choices=["LVH", "Normal", "ST"], label="Resting ECG")
                    heart_max_hr = gr.Number(label="Max Heart Rate")
                    heart_exercise_angina = gr.Dropdown(choices=["Yes", "No"], label="Exercise Angina")
                    heart_oldpeak = gr.Number(label="ST Depression")
                    heart_st_slope = gr.Dropdown(choices=["Up", "Flat", "Down"], label="ST Slope")
                    
                    heart_submit = gr.Button("Predict", size="lg")
                    heart_output = gr.HTML(label="Result")

        # Diabetes Tab
        with gr.Tab("Diabetes Prediction"):
            with gr.Column(elem_id="centered-container"):
                gr.Markdown("# Diabetes Prediction", elem_classes="markdown-text")
                
                with gr.Group(elem_classes="form-container"):
                    diabetes_age = gr.Number(label="Age")
                    diabetes_bmi = gr.Number(label="BMI")
                    diabetes_glucose = gr.Number(label="Glucose Level")
                    diabetes_bp = gr.Number(label="Blood Pressure")
                    diabetes_insulin = gr.Number(label="Insulin Level")
                    diabetes_pedigree = gr.Number(label="Diabetes Pedigree Function")
                    
                    diabetes_submit = gr.Button("Predict", size="lg")
                    diabetes_output = gr.HTML(label="Result")

        # Cancer Tab
        with gr.Tab("Cancer Prediction"):
            with gr.Column(elem_id="centered-container"):
                gr.Markdown("# Cancer Prediction", elem_classes="markdown-text")
                
                with gr.Group(elem_classes="form-container"):
                    cancer_age = gr.Number(label="Age")
                    cancer_tumor_size = gr.Number(label="Tumor Size")
                    cancer_lymph_nodes = gr.Number(label="Number of Lymph Nodes")
                    cancer_malignancy = gr.Dropdown(choices=["Benign", "Malignant"], label="Malignancy")
                    cancer_cell_shape = gr.Slider(minimum=1, maximum=10, label="Cell Shape Uniformity")
                    cancer_cell_size = gr.Slider(minimum=1, maximum=10, label="Cell Size Uniformity")
                    
                    cancer_submit = gr.Button("Predict", size="lg")
                    cancer_output = gr.HTML(label="Result")

    # Event handlers
    heart_submit.click(
        fn=predict_heart_disease,
        inputs=[
            heart_age, heart_sex, heart_chest_pain, heart_resting_bp,
            heart_cholesterol, heart_fasting_bs, heart_resting_ecg,
            heart_max_hr, heart_exercise_angina, heart_oldpeak, heart_st_slope
        ],
        outputs=heart_output
    )
    
    diabetes_submit.click(
        fn=predict_diabetes,
        inputs=[
            diabetes_age, diabetes_bmi, diabetes_glucose,
            diabetes_bp, diabetes_insulin, diabetes_pedigree
        ],
        outputs=diabetes_output
    )
    
    cancer_submit.click(
        fn=predict_cancer,
        inputs=[
            cancer_age, cancer_tumor_size, cancer_lymph_nodes,
            cancer_malignancy, cancer_cell_shape, cancer_cell_size
        ],
        outputs=cancer_output
    )

demo.launch(share=True)