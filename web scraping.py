from bs4 import BeautifulSoup
import requests
import pandas as pd

#df refers to -->  dataframe
# Create an empty Df to store the data
df = pd.DataFrame(columns=['Team Name', 'Year', 'Wins', 'Losses', 'OT Losses', 'Goals For (GF)', 'Goals Against (GA)', '+ / -', 'Win %'])

for n in range(0, 25):
    link = f'http://www.scrapethissite.com/pages/forms/?page_num={n}'
    rq = requests.get(link)
    
    # Check if the request was successful (status code 200)
    if rq.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(rq.text, 'html.parser')
        # Find the first table in the HTML
        table = soup.find('table')
        
        # Check if the table exists
        if table:
            # Extract data from each column in the web
            names = [name.text.strip() for name in table.find_all('td', class_='name')]
            years = [year.text.strip() for year in table.find_all('td', class_='year')]
            wins = [win.text.strip() for win in table.find_all('td', class_='wins')]
            loses = [lose.text.strip() for lose in table.find_all('td', class_='losses')]
            ot_loses = [ot_lose.text.strip() for ot_lose in table.find_all('td', class_='ot-losses')]
            gfs = [gf.text.strip() for gf in table.find_all('td', class_='gf')]
            gas = [ga.text.strip() for ga in table.find_all('td', class_='ga')]
            diffs = [diff.text.strip() for diff in table.find_all('td', class_='diff')]
            pcts = [pct.text.strip() for pct in table.find_all('td', class_='pct')]
            
            
            temp_df = pd.DataFrame({
                'Team Name': names,
                'Year': years,
                'Wins': wins,
                'Losses': loses,
                'OT Losses': ot_loses,
                'Goals For (GF)': gfs,
                'Goals Against (GA)': gas,
                '+ / -': diffs,
                'Win %': pcts
            })
            
            
            df = pd.concat([df, temp_df], ignore_index=True)
        else:
            print(f'No table found on page {n}')
    else:
        print(f'Error on page {n}, status code: {rq.status_code}')

# Display the final Df
df.to_excel('scraped_web.xlsx',index=False)
