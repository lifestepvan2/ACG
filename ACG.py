import random
import yaml
import tkinter as tk
from tkinter import messagebox
import os

# Load YAML data from the car_data.yaml file
def load_yaml_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    yaml_file = os.path.join(script_dir, 'car_data.yaml')  # Path to the YAML file
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

# Load the YAML data
yaml_data = load_yaml_data()

# Function to select a random variant based on weight
def weighted_random_choice(variants):
    choices = []
    for variant in variants:
        choices.extend([variant['name']] * variant['weight'])
    return random.choice(choices)

# Function to generate the text output
def generate_car_description(yaml_data):
    # Random year
    year = random.randint(yaml_data['year_range'][0], yaml_data['year_range'][1])
    
    # Random variant
    variant = weighted_random_choice(yaml_data['variants'])
    
    # Random segment
    segment = random.choice(list(yaml_data['subsegments']))
    
    # Get the parent segment for the chosen segment
    parent_segment = yaml_data['parent_segments'][segment['parent']]
    
    # Random subjective attribute from the parent segment
    subjective_attribute = random.choice(parent_segment['subjective_attributes'])
    
    # Random objective attribute from the parent segment
    objective_attribute = random.choice(parent_segment['objective_attributes'])
    
    # Construct the description
    description = f"a {variant} variant of a {subjective_attribute}, {objective_attribute} {segment['name']} from {year}"
    
    return description

# GUI Setup
class CarDescriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automation Challenge Generator")

        self.root.geometry("600x300")  # Width of 600px, Height of 300px


        # Text box to display the description
        self.description_text = tk.StringVar()
        self.description_label = tk.Label(root, textvariable=self.description_text, width=100, height=6)
        self.description_label.pack(pady=10)

        # Buttons
        self.generate_button = tk.Button(root, text="Generate Challenge", command=self.generate_challenge)
        self.generate_button.pack(pady=5)

        self.reroll_year_button = tk.Button(root, text="Reroll Year", command=self.reroll_year)
        self.reroll_year_button.pack(pady=5)

        self.reroll_variant_button = tk.Button(root, text="Reroll Variant", command=self.reroll_variant)
        self.reroll_variant_button.pack(pady=5)

        self.reroll_attributes_button = tk.Button(root, text="Reroll Attributes", command=self.reroll_attributes)
        self.reroll_attributes_button.pack(pady=5)

        # Store last generated description
        self.last_description = ""

    def generate_challenge(self):
        self.last_description = generate_car_description(yaml_data)
        self.description_text.set(self.last_description)

    def reroll_year(self):
        if not self.last_description:
            messagebox.showerror("Error", "No description to reroll!")
            return
        parts = self.last_description.split(" ")
        year = random.randint(yaml_data['year_range'][0], yaml_data['year_range'][1])
        parts[-1] = str(year)  # Replace the year part
        self.last_description = " ".join(parts)
        self.description_text.set(self.last_description)

    def reroll_variant(self):
        if not self.last_description:
            messagebox.showerror("Error", "No description to reroll!")
            return
        parts = self.last_description.split(" ")
        variant = weighted_random_choice(yaml_data['variants'])
        parts[1] = variant  # Replace the variant part
        self.last_description = " ".join(parts)
        self.description_text.set(self.last_description)

    def reroll_attributes(self):
        if not self.last_description:
            messagebox.showerror("Error", "No description to reroll!")
            return
        parts = self.last_description.split(" ")
        segment = random.choice(list(yaml_data['subsegments']))
        parent_segment = yaml_data['parent_segments'][segment['parent']]
        
        # Random subjective and objective attributes from the parent segment
        subjective_attribute = random.choice(parent_segment['subjective_attributes'])
        objective_attribute = random.choice(parent_segment['objective_attributes'])

        # Replace attributes in description
        parts[5] = subjective_attribute
        parts[6] = objective_attribute
        self.last_description = " ".join(parts)
        self.description_text.set(self.last_description)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CarDescriptionApp(root)
    root.mainloop()
