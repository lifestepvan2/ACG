import random
import yaml
import os

# Load YAML data from the car_data.yaml file
def load_yaml_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    yaml_file = os.path.join(script_dir, 'car_data.yaml')  # Path to the YAML file
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

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
    return f"a {variant} variant of a {subjective_attribute}, {objective_attribute} {segment['name']} from {year}"

import streamlit as st

st.title("Car Challenge Generator")
if st.button("Generate Challenge"):
    st.session_state.description = generate_car_description()
if "description" in st.session_state:
    st.write(st.session_state.description)
    if st.button("Reroll Year"):
        parts = st.session_state.description.split(" ")
        year = random.randint(yaml_data['year_range'][0], yaml_data['year_range'][1])
        parts[-1] = str(year)
        st.session_state.description = " ".join(parts)
    if st.button("Reroll Variant"):
        parts = st.session_state.description.split(" ")
        variant = weighted_random_choice(yaml_data['variants'])
        parts[1] = variant
        st.session_state.description = " ".join(parts)
    if st.button("Reroll Attributes"):
        parts = st.session_state.description.split(" ")
        segment = random.choice(list(yaml_data['subsegments']))
        parent_segment = yaml_data['parent_segments'][segment['parent']]
        subjective_attribute = random.choice(parent_segment['subjective_attributes'])
        objective_attribute = random.choice(parent_segment['objective_attributes'])
        parts[5] = subjective_attribute
        parts[7] = objective_attribute
        st.session_state.description = " ".join(parts)
