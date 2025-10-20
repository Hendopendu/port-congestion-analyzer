# scripts/real_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

print("=" * 60)
print("🚢 PORT CONGESTION SCRAPER - STARTING")
print("=" * 60)

def test_scraping():
    """Practice scraping on a training website"""
    print("\n📝 Step 1: Learning to scrape (practice site)...")
    
    try:
        # This is a website made for practicing web scraping
        url = "https://webscraper.io/test-sites/e-commerce/allinone"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"🌐 Connecting to {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for errors
        
        print("✅ Successfully connected to website!")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"📄 Page title: {soup.title.string if soup.title else 'No title'}")
        
        # Extract some product names (practice)
        products = []
        product_elements = soup.find_all('a', class_='title')  # Find product titles
        
        for product in product_elements[:5]:  # Get first 5 products
            product_name = product.get('title', 'No title')
            products.append(product_name)
            print(f"📦 Found product: {product_name}")
        
        return products
        
    except Exception as e:
        print(f"❌ Error during practice scraping: {e}")
        return []

def create_sample_port_data():
    """Create realistic sample data for our port analysis"""
    print("\n📊 Step 2: Creating sample port data...")
    
    # Realistic sample data
    ports = ['Shanghai', 'Los Angeles', 'Rotterdam', 'Singapore', 'Hamburg']
    
    data = []
    for i in range(10):  # Create 10 days of data
        for port in ports:
            date = f"2024-01-{i+1:02d}"
            # Realistic ranges: 5-30 ships waiting, $1500-3000 freight rates
            ships_waiting = (i * 2 + len(port)) % 25 + 5
            freight_rate = 1500 + (i * 100) + (len(port) * 50)
            
            data.append({
                'date': date,
                'port': port,
                'ships_waiting': ships_waiting,
                'freight_rate_usd': freight_rate
            })
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_path = '/app/data/port_congestion_data.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Created sample data with {len(df)} records")
    print(f"💾 Saved to: {csv_path}")
    print("\n📈 Sample of the data:")
    print(df.head())
    
    return df

def analyze_data(df):
    """Do some basic analysis on our data"""
    print("\n📊 Step 3: Analyzing the data...")
    
    # Basic statistics
    avg_ships = df['ships_waiting'].mean()
    avg_rate = df['freight_rate_usd'].mean()
    
    print(f"📊 Average ships waiting: {avg_ships:.1f}")
    print(f"💰 Average freight rate: ${avg_rate:.0f}")
    
    # Find the most congested port
    most_congested = df.groupby('port')['ships_waiting'].mean().idxmax()
    max_congestion = df.groupby('port')['ships_waiting'].mean().max()
    
    print(f"🚨 Most congested port: {most_congested} ({max_congestion:.1f} ships avg.)")
    
    # Simple correlation
    correlation = df['ships_waiting'].corr(df['freight_rate_usd'])
    print(f"📈 Correlation between congestion and rates: {correlation:.2f}")

def main():
    """Main function"""
    print("Starting web scraping project...")
    
    # Step 1: Practice scraping
    products = test_scraping()
    
    # Step 2: Create our port data
    df = create_sample_port_data()
    
    # Step 3: Analyze the data
    analyze_data(df)
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Web scraper is working!")
    print("Next: We'll replace sample data with real shipping data")
    print("=" * 60)

if __name__ == "__main__":
    main()