# ebay_scraper
Methodology:
1. scrape using selenium (scraper.py)
2. automate scraping via git hub actions (every 3hrs)
3. clean the data scraped
4. add cleaning to automation so that it cleans the new data scraped and updates clean csv accordingly
5. visualize trends and plot charts and graphs using pandas, matplotlib, seaborn

Key Finding:
1. in EDA instead of having to create a new column "absolute discount" manually every time, create it in the cleaning script so that the values updated are already calculated and imported form the clean csv
2. most scraped data was from hour 19 for some reason 
3. most products are less than 200$
4. outlier are priced more than 400-500$




challenges: 
Cleaning logic is easy but syntax is still a bit unfamiliar, same for seaborn but its easy
