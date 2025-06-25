
# FT Pitch Assistant

An AI-powered Streamlit app to help craft tailored pitches to Financial Times journalists.

## Features

- Suggests the most relevant FT journalists based on your story idea
- Generates a concise, persuasive email pitch customized for the selected journalist
- Scores the pitch on clarity, relevance, persuasiveness, and brevity
- Provides actionable improvement suggestions for your pitch

## Setup

### Requirements

- Python 3.8+
- OpenAI API key ([Get your key here](https://platform.openai.com/account/api-keys))

### Installation

1. Clone or download this repo.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

4. Run the app:

```bash
streamlit run pitch_agent.py
```

### Usage

- Enter a story idea.
- Optionally check "Suggest journalist based on story idea" to get AI recommendations.
- Select or accept the suggested journalist.
- Click **Generate Pitch** to get your custom pitch, feedback scores, and improvement tips.

## Deployment

You can deploy this app easily on [Streamlit Cloud](https://streamlit.io/cloud) by connecting your GitHub repo and adding your OpenAI API key in the Secrets section.

## Files

- `pitch_agent.py` — Main Streamlit app
- `journalists.csv` — List of FT journalists (update as needed)
- `requirements.txt` — Python dependencies

---

Made with ❤️ to help PR pros pitch smarter.
