
import streamlit as st
import pandas as pd
import openai
import os

# --- Configuration ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Load Journalist Data ---
@st.cache_data
def load_journalists():
    return pd.read_csv("journalists.csv")

journalists_df = load_journalists()

# --- UI ---
st.title("\ud83c\udfae FT Pitch Assistant")
st.markdown("Write tailored pitches to Financial Times journalists with AI assistance.")

story_idea = st.text_area("Enter your story idea", placeholder="e.g. How Gen Z is reshaping luxury travel")

suggest_journalist = st.checkbox("Suggest journalist based on story idea")

if suggest_journalist and story_idea:
    with st.spinner("Matching your story to journalists..."):
        match_prompt = f"""
        Based on the story idea below, suggest the 3 most relevant journalists from this list.
        Return a list of their names only.

        Story Idea:
        "{story_idea}"

        Journalists:
        {journalists_df[['name', 'beat', 'recent_article_title']].to_string(index=False)}
        """

        match_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": match_prompt}]
        )

        suggested_names = match_response['choices'][0]['message']['content'].split("\n")
        suggested_names = [name.strip("- •* ") for name in suggested_names if name.strip()]

        st.markdown("### \ud83d\udd0d Suggested Journalists")
        st.write(suggested_names)

        # Default to first suggested
        if suggested_names:
            journalist_name = suggested_names[0]
        else:
            journalist_name = st.selectbox("Select a journalist", journalists_df['name'])
else:
    journalist_name = st.selectbox("Select a journalist", journalists_df['name'])

if journalist_name:
    journalist_data = journalists_df[journalists_df['name'] == journalist_name].iloc[0]

    if st.button("Generate Pitch") and story_idea:
        with st.spinner("Crafting your pitch..."):
            # --- Generate Pitch ---
            prompt = f"""
            You are a PR assistant helping pitch a story to a Financial Times journalist.

            - Story idea: "{story_idea}"
            - Journalist: {journalist_data['name']}
            - Beat: {journalist_data['beat']}
            - Recent article: "{journalist_data['recent_article_title']}"
            - Excerpt: "{journalist_data['recent_article_excerpt']}"

            Write a concise, persuasive email pitch (under 150 words) with:
            - A subject line
            - A strong opening hook
            - Clear relevance to FT’s audience
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            pitch = response['choices'][0]['message']['content']

            st.markdown("### \u2709\ufe0f Your Custom Pitch")
            st.text_area("Pitch", value=pitch, height=200)

            # --- Score the Pitch ---
            with st.spinner("Evaluating pitch quality..."):
                score_prompt = f"""
                You are a PR writing coach. Please rate the following pitch based on 4 criteria from 1–10:

                1. Clarity – Is it clearly written?
                2. Relevance – Is it relevant to the journalist’s beat and the Financial Times readership?
                3. Persuasiveness – Does it make a compelling case to cover the story?
                4. Brevity – Is it concise and avoids fluff (target under 150 words)?

                Provide scores and a brief reason for each.

                PITCH:
                {pitch}
                """

                score_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": score_prompt}]
                )

                evaluation = score_response['choices'][0]['message']['content']
                st.markdown("### \ud83d\udcca Pitch Quality Feedback")
                st.markdown(evaluation)

            # --- Improvement Suggestions ---
            with st.spinner("Suggesting improvements..."):
                suggestion_prompt = f"""
                Act as an expert media pitching editor. Here’s a PR pitch:

                ---
                {pitch}
                ---

                Please suggest 2–3 specific improvements to make it more compelling, relevant, or concise.
                Make each suggestion actionable (e.g., “Rephrase the hook to emphasize urgency”).
                """

                suggestion_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": suggestion_prompt}]
                )

                suggestions = suggestion_response['choices'][0]['message']['content']
                st.markdown("### \ud83d\udee0\ufe0f Improvement Suggestions")
                st.markdown(suggestions)
    else:
        st.info("Please enter a story idea to get started.")
