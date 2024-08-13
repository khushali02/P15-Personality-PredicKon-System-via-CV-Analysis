import os
import re
import string
import csv
import PyPDF2
import textract
import spacy
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Helper functions

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
        return ""

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {e}")
        try:
            # Fallback to Textract if PyPDF2 fails
            return textract.process(file_path).decode('utf-8')
        except Exception as textract_error:
            print(f"Textract failed for {file_path}: {textract_error}")
            return ""

def preprocess_text(text):
    """Preprocess text by removing punctuation, tokenizing, removing stopwords, and lemmatizing."""
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return ' '.join(lemmatized_tokens)

def extract_text_based_on_file(file_path):
    """Extract and preprocess text based on file type."""
    if file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return ""

    return preprocess_text(text)

def extract_features_from_resumes(folder_path):
    """Extract preprocessed text from all resumes in a folder."""
    extracted_texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            if text:  # Only add if text is not empty
                extracted_texts.append(text)
    return extracted_texts

def extract_tfidf_features(texts, max_features=1000):
    """Extract TF-IDF features from the given texts."""
    tfidf_vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_features = tfidf_vectorizer.fit_transform(texts)
    return tfidf_features, tfidf_vectorizer

def extract_name(filename, row_number):
    """Extract name from the filename or use a default based on row number."""
    name_pattern = r'(.+?)\.(pdf|docx)'
    match = re.search(name_pattern, filename)
    return match.group(1) if match else f"resume_{row_number}"

def extract_contact_info(text):
    """Extract email addresses and phone numbers from the text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}\b|\d{4}[-.\s]??\d{3}[-.\s]??\d{4}\b)'
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    return ', '.join(emails + phones)

def extract_education(text, education_file='education.txt'):
    """Extract education details based on keywords."""
    try:
        with open(education_file, 'r', encoding='utf-8') as file:
            education_keywords = [line.strip().lower() for line in file]
    except Exception as e:
        print(f"Error reading education file: {e}")
        return ""

    lowercase_text = text.lower()
    education_details = [keyword for keyword in education_keywords if keyword in lowercase_text]
    return ', '.join(education_details)

def extract_work_experience(text, work_exp_file='workExp.txt'):
    """Extract work experience details based on keywords."""
    try:
        with open(work_exp_file, 'r', encoding='utf-8') as file:
            experience_keywords = [line.strip().lower() for line in file]
    except Exception as e:
        print(f"Error reading work experience file: {e}")
        return ""

    lowercase_text = text.lower()
    experience_details = [keyword for keyword in experience_keywords if keyword in lowercase_text]
    return ', '.join(experience_details)

def extract_skills(text, skills_file='skills.txt'):
    """Extract skills based on keywords."""
    try:
        with open(skills_file, 'r', encoding='utf-8') as file:
            skills_keywords = [line.strip().lower() for line in file]
    except Exception as e:
        print(f"Error reading skills file: {e}")
        return ""

    lowercase_text = text.lower()
    skills_list = [skill for skill in skills_keywords if skill in lowercase_text]
    return ', '.join(skills_list)

def construct_dataset(folder_path):
    """Construct a dataset from the resumes in the given folder."""
    dataset = []
    row_number = 1
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            if not text:
                continue

            name = extract_name(filename, row_number)
            contact_info = extract_contact_info(text)
            education = extract_education(text)
            work_experience = extract_work_experience(text)
            skills = extract_skills(text)
            row_number += 1

            resume_data = {
                'Filename': filename,
                'Name': name,
                'Contact Information': contact_info,
                'Education': education,
                'Work Experience': work_experience,
                'Skills': skills,
            }
            dataset.append(resume_data)
    return dataset

def save_dataset_to_csv(dataset, output_file):
    """Save the dataset to a CSV file."""
    fieldnames = ['Filename', 'Name', 'Contact Information', 'Education', 'Work Experience', 'Skills']
    if not os.path.isfile(output_file):
        # Write headers only if the file does not exist
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)
    else:
        # Append to the file if it already exists
        with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(dataset)

if __name__ == "__main__":
    folder_path = r"C:\Developer\PycharmProjects\personality-Prediction-System-via-CV-Analysis\uploads"

    if not os.path.exists(folder_path):
        print("Folder path doesn't exist.")
    else:
        # Extract preprocessed text from resumes
        extracted_texts = extract_features_from_resumes(folder_path)
        
        # Extract and structure data from resumes
        dataset = construct_dataset(folder_path)

        # Extract TF-IDF features
        tfidf_features, tfidf_vectorizer = extract_tfidf_features(extracted_texts)

        # Save the structured dataset to a CSV file
        output_file = 'resume_dataset.csv'
        save_dataset_to_csv(dataset, output_file)
        print(f"Dataset saved to {output_file}")

        # Display TF-IDF features
        feature_names = tfidf_vectorizer.get_feature_names_out()
        print("TF-IDF Features:")
        print(feature_names)
        print("\nTF-IDF Matrix:")
        print(tfidf_features.toarray())
