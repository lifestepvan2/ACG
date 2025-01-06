import random
import yaml
import os
import streamlit as st
# random number for background image
if "bg_idx" not in st.session_state:
    st.session_state.bg_idx = random.randint(1, 23)  # Generate a random background index only once


# Streamlit App
st.title("Automation Challenge Generator")

description_placeholder = st.empty()
description_placeholder.text("")

# Load YAML data from the car_data.yaml file
def load_yaml_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    yaml_file = os.path.join(script_dir, 'car_data.yaml')  # Path to the YAML file
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)
def add_bg(idx):

    # Define the CSS with opacity and a randomized URL
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: none; /* Remove any default background styling */
        }}
        .background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: url("https://raw.githubusercontent.com/lifestepvan2/ACG/refs/heads/main/static/{idx}.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.4); /* Adjust opacity and color here */
            z-index: -1;
        }}
        </style>
        <div class="background"></div>
        <div class="overlay"></div>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background
add_bg(st.session_state.bg_idx)
    
yaml_data = load_yaml_data()

def weighted_random_choice(variants):
    choices = []
    for variant in variants:
        choices.extend([variant['name']] * variant['weight'])
    return random.choice(choices)

def generate_car_description():
    year = random.randint(yaml_data['year_range'][0], yaml_data['year_range'][1])
    variant = weighted_random_choice(yaml_data['variants'])
    segment = random.choice(list(yaml_data['subsegments']))
    parent_segment = yaml_data['parent_segments'][segment['parent']]
    subjective_attribute = random.choice(parent_segment['subjective_attributes'])
    objective_attribute = random.choice(parent_segment['objective_attributes'])

    return {
        "year": year,
        "variant": variant,
        "subjective_attribute": subjective_attribute,
        "objective_attribute": objective_attribute,
        "segment": segment['name'],
        "parent_segment": segment['parent']
    }

def correct_indefinite_article(text):
    words = text.split()
    for i in range(len(words) - 1):
        if words[i].lower() == "a" and words[i + 1][0].lower() in "aeiou":
            words[i] = "an"
    return " ".join(words)

def build_description(fields):
    raw_description = (f"The year is {fields['year']}. \n\n You are tasked with designing a {fields['variant']} variant of a {fields['segment']} that is {fields['objective_attribute']} and {fields['subjective_attribute']}.")
    return correct_indefinite_article(raw_description)

if "fields" not in st.session_state:
    st.session_state.fields = generate_car_description()

if st.button("Generate Challenge"):
    st.session_state.fields = generate_car_description()
    description = build_description(st.session_state.fields)
    description_placeholder.text(description)

if st.button("Reroll Year"):
    st.session_state.fields["year"] = random.randint(
        yaml_data['year_range'][0], yaml_data['year_range'][1]
    )
    description = build_description(st.session_state.fields)
    description_placeholder.text(description)

if st.button("Reroll Variant"):
    st.session_state.fields["variant"] = weighted_random_choice(yaml_data['variants'])
    description = build_description(st.session_state.fields)
    description_placeholder.text(description)

if st.button("Reroll Attributes"):
    parent_segment = st.session_state.fields["parent_segment"]
    st.session_state.fields["subjective_attribute"] = random.choice(parent_segment['subjective_attributes'])
    st.session_state.fields["objective_attribute"] = random.choice(parent_segment['objective_attributes'])
    description = build_description(st.session_state.fields)
    description_placeholder.text(description)
