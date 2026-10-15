# IssuePilot-AI

**AI-Powered Software Issue Classification and Analysis**

## Overview

IssuePilot-AI is a Python-based application designed to help users analyze and categorize software issues using Natural Language Processing (NLP). Users can submit a software issue description and receive an analysis based on the application's implemented classification and prioritization logic.

The goal is to make software issue reporting more organized and help developers understand reported problems more efficiently.

## Features

- Accept software issue descriptions as input.
- Classify issue descriptions using a pretrained NLP model, when successfully loaded.
- Support zero-shot classification without training a dedicated model on a new labeled dataset.
- Apply rule-based logic for issue prioritization, if configured in the application.
- Present issue analysis through the application's user interface.

*The available features depend on the current implementation.*

## Technology Stack

- **Programming Language:** Python
- **Machine Learning:** PyTorch and Hugging Face Transformers
- **Model Repository:** Hugging Face Model Hub
- **Interface:** Streamlit, if used by the current application
- **Environment:** Python virtual environment

## AI Model

The project is configured to use the following pretrained model:

`cross-encoder/nli-MiniLM2-L6-H768`

Model source: https://huggingface.co/cross-encoder/nli-MiniLM2-L6-H768

The model is based on Natural Language Inference (NLI) and can be used for zero-shot text classification. It compares an issue description against candidate categories to help identify the most relevant category.

### How It Works

1. The user enters a software issue description.
2. The application processes the input.
3. The configured NLP model evaluates the text against candidate categories.
4. The application returns the classification results.
5. Any additional priority assessment or recommendations depend on the application's implemented logic.

The model is pretrained; this project does not claim to train it from scratch.

## Role of Hugging Face

Hugging Face Model Hub provides access to the pretrained model and its configuration files. The Transformers library loads the model into the Python application.

The model is normally downloaded and cached locally when it is first loaded. An internet connection may be required for the initial download. Hugging Face Model Hub is the model source, not necessarily the hosting platform for this application.

## Installation and Setup

### Prerequisites

- Python installed on your computer
- Git
- Internet access for the initial model download, if the model is not cached

### 1. Clone the Repository

```bash
git clone https://github.com/aimanshahzadi2794-rgb/hacktoberfest 
cd IssuePilot-AI
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If the project contains a `requirements.txt` file:

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the Application

If the Streamlit entry point is `app.py`:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

If the project uses a different entry-point file, use the appropriate command.

## Project Structure

The structure depends on the current repository. A typical layout may look like:

```text
IssuePilot-AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

The virtual environment should remain local and should not be committed to Git.

## Limitations

- Classification results depend on the model, candidate categories, and input quality.
- A predicted category is not a guarantee of the actual root cause.
- Priority assessment and suggested fixes require their own implemented logic.
- Automatic code repair is not implied by issue classification.
- Model availability depends on successful installation and loading.

## Future Improvements

- Improve issue categorization and severity assessment.
- Add issue history and tracking.
- Evaluate classification quality using a labeled test dataset.
- Add explainable predictions and more detailed recommendations.
- Explore integration with issue-tracking platforms.

## Project Status

Under development.

## License

No license has been specified yet. Add a license before distributing the project under particular reuse terms.