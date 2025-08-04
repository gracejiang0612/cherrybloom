#!/usr/bin/env python3
"""
Central Park Cherry Blossom Trees Scraper
Standalone Python script to scrape cherry blossom tree information and save to CSV
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import re

def scrape_cherry_blossom_data():
    """
    Scrape cherry blossom tree information from Central Park website
    Returns a list of dictionaries with place and description
    """
    base_url = "https://www.centralpark.com/things-to-do/attractions/map-of-cherry-blossom-trees-in-central-park/"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_data = []
    page = 1
    
    while True:
        # Construct URL for current page
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}#page={page}"
        
        print(f"Scraping page {page}...")
        
        try:
            # Make the request
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for h3 tags that might be place names
            headings = soup.find_all('h3')
            
            page_data_found = False
            for heading in headings:
                place_name = heading.get_text(strip=True)
                
                # Skip if it's not a location name (filter out navigation, etc.)
                if len(place_name) < 3 or place_name.lower() in ['search', 'menu', 'navigation']:
                    continue
                
                # Find the next paragraph that contains the description
                next_p = heading.find_next('p')
                if next_p:
                    description = next_p.get_text(strip=True)
                    
                    # Only add if we have meaningful data
                    if len(description) > 10:
                        all_data.append({
                            'place': place_name,
                            'description': description
                        })
                        page_data_found = True
                        print(f"  Found: {place_name}")
            
            # If no data found on this page, try alternative method
            if not page_data_found:
                # Look for divs with specific patterns
                entries = soup.find_all('div', class_=lambda x: x and any(word in x.lower() for word in ['entry', 'item', 'result', 'attraction']))
                
                for entry in entries:
                    heading = entry.find('h3') or entry.find('h2') or entry.find('h4')
                    if heading:
                        place_name = heading.get_text(strip=True)
                        description_elem = entry.find('p')
                        if description_elem:
                            description = description_elem.get_text(strip=True)
                            if len(description) > 10:
                                all_data.append({
                                    'place': place_name,
                                    'description': description
                                })
                                print(f"  Found: {place_name}")
            
            # Check if there are more pages
            next_link = soup.find('a', string=lambda x: x and 'Next' in x)
            if not next_link:
                break
                
            page += 1
            time.sleep(1)  # Be respectful with requests
            
        except requests.RequestException as e:
            print(f"Error scraping page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break
    
    return all_data

def save_to_csv(data, filename="central_park_cherry_blossoms.csv"):
    """
    Save the scraped data to a CSV file
    """
    if not data:
        print("No data to save!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False, encoding='utf-8')
    
    # Also save using csv module for better control
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['place', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    
    print(f"Data saved to {filename}")
    print(f"Total entries: {len(data)}")
    
    # Display first few entries
    print("\nFirst few entries:")
    for i, entry in enumerate(data[:5], 1):
        print(f"{i}. {entry['place']}: {entry['description'][:100]}...")

def main():
    """
    Main function to run the scraper
    """
    print("Starting Central Park Cherry Blossom Trees Scraper...")
    print("=" * 50)
    
    # Scrape the data
    cherry_blossom_data = scrape_cherry_blossom_data()
    
    if cherry_blossom_data:
        print(f"\nSuccessfully scraped {len(cherry_blossom_data)} entries!")
        
        # Save to CSV
        save_to_csv(cherry_blossom_data)
        
        # Verify the file was created
        try:
            verification_df = pd.read_csv("central_park_cherry_blossoms.csv")
            print(f"\nCSV file verification - Shape: {verification_df.shape}")
            print("Column names:", list(verification_df.columns))
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    else:
        print("No data was scraped. Please check the website structure or try a different approach.")

if __name__ == "__main__":
    main() 