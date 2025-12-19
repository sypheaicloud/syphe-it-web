import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_table(url):
    """
    Scrapes table data from a given URL and returns a pandas DataFrame.
    """
    try:
        # Add headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
       
        response = requests.get(url, headers=headers, timeout=10)
       
        # Check if the request was successful
        if response.status_code == 200:
            print('Request successful!')
        else:
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
            return None
       
        soup = BeautifulSoup(response.content, 'html.parser')
       
        # Print the title of the webpage to verify
        if soup.title:
            print(f'Page title: {soup.title.text}')
       
        # Try to find the table - first try by id, then by class, then just get first table
        table = soup.find('table', {'id': 'data-table'})
       
        if not table:
            # Try finding table by class
            table = soup.find('table', {'class': 'table'})
       
        if not table:
            # Just get the first table on the page
            table = soup.find('table')
            print('Using first table found on page')
       
        if not table:
            print('No table found on the page')
            return None
       
        # Extract all rows from the table
        rows = table.find_all('tr')
       
        if not rows:
            print('No rows found in the table')
            return None
       
        # Extract headers if they exist
        headers_row = rows[0].find_all('th')
        if headers_row:
            column_names = [th.text.strip() for th in headers_row]
            data_rows = rows[1:]  # Skip header row
        else:
            # If no headers, use the first row as data
            column_names = [f'Column{i+1}' for i in range(len(rows[0].find_all('td')))]
            data_rows = rows
       
        # Loop through the rows and extract data
        data = []
        for row in data_rows:
            cols = row.find_all('td')
            if cols:  # Only process rows that have td elements
                cols = [col.text.strip() for col in cols]
                data.append(cols)
       
        if not data:
            print('No data extracted from table')
            return None
       
        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data, columns=column_names)
       
        print(f'\nSuccessfully scraped {len(df)} rows')
        return df
       
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None
    except Exception as e:
        print(f'Error during scraping: {e}')
        return None




# Main execution
if __name__ == '__main__':
    url = 'https://admissions.nic.in/UPTAC/applicant/report/orcrreport.aspx?enc=Nm7QwHILXclJQSv2YVS+7hwSpVykA3HgnWxJU5ug/WL0iltkiRWoMZqp6sExKmRw'
   
    df = scrape_table(url)
   
    if df is not None:
        # Display the scraped data
        print('\nScraped Data:')
        print(df.head(10))  # Show first 10 rows
       
        # Optionally save to CSV
        # df.to_csv('scraped_data.csv', index=False)
        # print('\nData saved to scraped_data.csv')
    else:
        print('Failed to scrape data from the website')
