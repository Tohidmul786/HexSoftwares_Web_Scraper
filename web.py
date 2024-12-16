import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to fetch and parse the webpage
def fetch_page(url):
    try:
        # Send a get request to the webpage
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f'Error Fetching the page: {e}')
        return None
    
# Function to extract headings from the page
def extract_heading(soup):
    headings = soup.find_all('h1')  # Extract all h1 tags
    return [heading.text.strip() for heading in headings]

# Function to extract all links from the page
def extract_links(soup):
    links = soup.find_all('a', href=True)  # Extract all anchor tags with href attribute
    return [link['href'] for link in links]

# Function to extract paragraphs
def extract_parag(soup):
    paragraphs = soup.find_all('p')  # Extract p tags
    return [para.text.strip() for para in paragraphs]

# Function to save data to a CSV file inside a specific folder
def save_file(data, folder, filename, header):
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the full path for the CSV file
    file_path = os.path.join(folder, filename)

    # Save the data to the CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([header])  # Column header
        for item in data:
            writer.writerow([item])

# MAIN FUNCTION to run the scraper
def main():
    url = input("Enter the URL of the webpage to scrape: ")  # Input from user
    html_content = fetch_page(url)  # Fetch page content

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content

        # Pretty print the HTML (formatted HTML content)
        print("\nFormatted HTML Content (soup.prettify()):\n")
        print(soup.prettify())  # Print the prettified HTML

        # Extract different types of data
        print("\nExtracting Data...")

        headings = extract_heading(soup)
        print(f'\nHeadings (H1 tags) are: \n{headings}')

        links = extract_links(soup)
        print(f'\nLinks (Anchor tags):\n{links}')

        paragraphs = extract_parag(soup)
        print(f"\nParagraphs (P tags):\n{paragraphs}")

        # Define the folder to save files
        folder = 'scraped_data'

        # Save extracted data to CSV files inside the folder
        save_file(headings, folder, 'headings.csv', 'Headings')
        save_file(links, folder, 'links.csv', 'Links')
        save_file(paragraphs, folder, 'paragraphs.csv', 'Paragraphs')

        print("\nData has been saved to 'scraped_data/headings.csv', 'scraped_data/links.csv', and 'scraped_data/paragraphs.csv'.")

if __name__ == '__main__':
    main()
