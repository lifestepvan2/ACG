import yaml
from collections import defaultdict

def invert_and_flatten_attributes(data, key):
    """
    Groups attributes by their keys and lists parent segments in a flat list.
    Args:
        data (dict): The YAML data loaded as a Python dictionary.
        key (str): The key to process ('subjective_attributes' or 'objective_attributes').

    Returns:
        dict: A dictionary with attributes as keys and parent segments as values.
    """
    inverted = defaultdict(list)
    parent_segments = data.get("parent_segments", {})

    for segment, attributes in parent_segments.items():
        for attr in attributes.get(key, []):
            inverted[attr].append(segment)

    # Convert lists to comma-separated strings
    return {attr: ",".join(sorted(segments)) for attr, segments in inverted.items()}

def restructure_yaml(input_file, output_file):
    try:
        # Load input YAML file
        with open(input_file, 'r') as infile:
            data = yaml.safe_load(infile)

        # Process subjective and objective attributes
        grouped_subjective_attributes = invert_and_flatten_attributes(data, 'subjective_attributes')
        grouped_objective_attributes = invert_and_flatten_attributes(data, 'objective_attributes')

        # Create output structure
        output_data = {
            "grouped_subjective_attributes": grouped_subjective_attributes,
            "grouped_objective_attributes": grouped_objective_attributes,
        }

        # Write to output YAML file
        with open(output_file, 'w') as outfile:
            yaml.dump(output_data, outfile, default_flow_style=False)

        print(f"Successfully processed and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = 'ACG\car_data.yaml'  # Replace with your input YAML filename
output_file = 'output.yaml'  # Replace with your desired output YAML filename
restructure_yaml(input_file, output_file)
