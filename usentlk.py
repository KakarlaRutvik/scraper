import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Ensure the necessary NLTK data files are downloaded
nltk.download('punkt')  # For tokenization
nltk.download('stopwords')  # For stopwords

# Define stop words in English
stop_words = set(stopwords.words('english'))

# Function to clean text using NLTK
def clean_text_with_nltk(text):
    """Clean the text by tokenizing, removing stopwords, and filtering non-alphabetic tokens."""
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Remove stopwords and non-alphabetic words
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    
    # Join the words back into a single string
    return ' '.join(filtered_words)

# Function to clean JSON content
def clean_json_content(data):
    """Clean the text content in a JSON object."""
    cleaned_data = {}
    
    for key, value in data.items():
        if isinstance(value, str):  # If the value is a string, clean it
            cleaned_data[key] = clean_text_with_nltk(value)
        elif isinstance(value, dict):  # If the value is a dictionary, clean it recursively
            cleaned_data[key] = clean_json_content(value)
        elif isinstance(value, list):  # If the value is a list, clean each string in the list
            cleaned_data[key] = [clean_text_with_nltk(item) if isinstance(item, str) else item for item in value]
        else:
            cleaned_data[key] = value  # Leave other data types untouched
    
    return cleaned_data

# Function to process all JSON files in a folder and save the cleaned data
def process_all_json_files(input_folder, output_folder):
    try:
        # Get a list of all JSON files in the input folder
        json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
        
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Loop through all the JSON files
        for json_file in json_files:
            input_file = os.path.join(input_folder, json_file)
            output_file = os.path.join(output_folder, f"cleaned_{json_file.replace('.json', '.txt')}")
            
            # Read the JSON file
            with open(input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Clean the data
            cleaned_data = clean_json_content(data)
            
            # Save the cleaned data to a .txt file
            with open(output_file, 'w', encoding='utf-8') as file:
                # Write the cleaned data as text (joining values into a single string per item)
                for key, value in cleaned_data.items():
                    if isinstance(value, str):
                        file.write(f"{key}: {value}\n")
                    elif isinstance(value, list):
                        file.write(f"{key}: {', '.join(value)}\n")
                    else:
                        file.write(f"{key}: {value}\n")
            
            print(f"Cleaned data has been saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_folder = '/workspaces/scraper/scraped_data'  # Folder containing the JSON files
output_folder = '/workspaces/scraper/txt_data'  # Folder where the cleaned text files will be saved

# Process all JSON files in the input folder
process_all_json_files(input_folder, output_folder)
