import os
import pandas as pd

# Define file paths
file_path = 'extracted_details.csv'
traits_file = 'traits.txt'
output_file_path = 'extracted_detailsWith_traits.csv'

# Check if the extracted details file exists, and create it with appropriate headers if it doesn't
if not os.path.isfile(file_path):
    pd.DataFrame(columns=['Filename', 'Name', 'Contact Information', 'Education', 'Work Experience', 'Skills']).to_csv(file_path, index=False)

# Load the extracted details from the CSV file
data = pd.read_csv(file_path)

# Function to read personality traits associations from the traits file
def read_traits_from_file(file_path):
    traits_mapping = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                trait, skills = line.strip().split(':')
                trait = trait.strip()
                skills = [skill.strip() for skill in skills.split(',')]
                traits_mapping[trait] = skills
    except Exception as e:
        print(f"Error reading traits file: {e}")
    return traits_mapping

# Load the traits mapping
traits_mapping = read_traits_from_file(traits_file)

# Function to assign personality traits based on skills
def assign_personality_traits(row):
    traits_scores = {trait: 0 for trait in traits_mapping}
    if pd.notna(row['Skills']):  # Ensure 'Skills' is not NaN
        for trait, associated_skills in traits_mapping.items():
            for skill in associated_skills:
                if skill in row['Skills']:
                    traits_scores[trait] += 1
    return pd.Series(traits_scores)

# Apply the function to the dataframe to assign personality traits
personality_traits = data.apply(assign_personality_traits, axis=1)

# Concatenate the original data with the assigned personality traits
data_with_traits = pd.concat([data, personality_traits], axis=1)

# Save the updated data to a new CSV file
data_with_traits.to_csv(output_file_path, index=False)

print(f"Data with personality traits saved to {output_file_path}.")
