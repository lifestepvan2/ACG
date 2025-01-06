import random
import yaml
import os
import streamlit as st

description_placeholder = st.empty()
description_placeholder.text("")

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

    return {
        "year": year,
        "variant": variant,
        "subjective_attribute": subjective_attribute,
        "objective_attribute": objective_attribute,
        "segment": segment['name']
    }

def build_description(fields):
    return (f"a {fields['variant']} variant of a {fields['subjective_attribute']}, "
            f"{fields['objective_attribute']} {fields['segment']} from {fields['year']}")

# Streamlit App
st.title("Car Challenge Generator")

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
    segment = random.choice(list(yaml_data['subsegments']))
    parent_segment = yaml_data['parent_segments'][segment['parent']]
    st.session_state.fields["subjective_attribute"] = random.choice(parent_segment['subjective_attributes'])
    st.session_state.fields["objective_attribute"] = random.choice(parent_segment['objective_attributes'])
    st.session_state.fields["segment"] = segment['name']
    description = build_description(st.session_state.fields)
    description_placeholder.text(description)
