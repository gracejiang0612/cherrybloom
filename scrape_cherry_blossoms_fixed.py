#!/usr/bin/env python3
"""
Central Park Cherry Blossom Trees Scraper - Fixed Version
Scrapes cherry blossom tree information from Central Park website and saves to CSV
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def scrape_cherry_blossom_data():
    """
    Scrape cherry blossom tree information from Central Park website
    Returns a list of dictionaries with place and description
    """
    url = "https://www.centralpark.com/things-to-do/attractions/map-of-cherry-blossom-trees-in-central-park/"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Scraping Central Park cherry blossom data...")
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Based on the website structure, we need to find the specific cherry blossom entries
        # The cherry blossom locations are typically in h3 tags with specific content
        all_data = []
        
        # Look for h3 tags that contain cherry blossom location names
        headings = soup.find_all('h3')
        
        # Define the expected cherry blossom locations based on the website content
        cherry_locations = [
            'Reservoir',
            'The Glade', 
            'Cherry Hill',
            'Pilgrim Hill',
            'Cedar Hill',
            'Metropolitan Museum of Art',
            'Great Lawn',
            'East Green',
            'Bethesda Fountain',
            'Delacorte Theater',
            'Ramble',
            'Nell Singer Lilac Walk',
            'East Meadow',
            'Trefoil Arch',
            'Wagner Cove'
        ]
        
        for heading in headings:
            place_name = heading.get_text(strip=True)
            
            # Check if this is one of the cherry blossom locations
            if place_name in cherry_locations:
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
                        print(f"Found: {place_name}")
        
        # If we didn't find the expected locations, try a different approach
        if not all_data:
            print("Trying alternative scraping method...")
            
            # Look for any h3 tags that might be location names
            for heading in headings:
                place_name = heading.get_text(strip=True)
                
                # Skip navigation and other non-location content
                if (len(place_name) < 3 or 
                    place_name.lower() in ['search', 'menu', 'navigation', 'tags', 'visitor info', 'most popular', 'about us', 'follow us'] or
                    '?' in place_name or
                    'are you planning' in place_name.lower()):
                    continue
                
                # Find the next paragraph
                next_p = heading.find_next('p')
                if next_p:
                    description = next_p.get_text(strip=True)
                    
                    # Only add if description seems relevant (mentions cherry, blossom, tree, etc.)
                    if (len(description) > 20 and 
                        any(word in description.lower() for word in ['cherry', 'blossom', 'tree', 'yoshino', 'kwanzan', 'flower'])):
                        all_data.append({
                            'place': place_name,
                            'description': description
                        })
                        print(f"Found: {place_name}")
        
        return all_data
        
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

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
    
    # Display all entries
    print("\nAll scraped entries:")
    for i, entry in enumerate(data, 1):
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
            print(f"Number of entries: {len(verification_df)}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    else:
        print("No data was scraped. Please check the website structure or try a different approach.")

if __name__ == "__main__":
    main() 