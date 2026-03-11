import pandas as pd
import numpy as np

def clean_ebay_data(input_file, output_file):
    df = pd.read_csv(input_file)
    print(f"Initial row count: {len(df)}")

   #if there is no title or url (N/A) => drop 
    df = df[df['title'] != 'N/A'].dropna(subset=['title', 'item_url'])
    
    #clean numeric strings and change to float (price and original)
    def clean_currency(value):
        if pd.isna(value) or value == 'N/A':
            return np.nan

        clean_val = str(value).replace('$', '').replace(',', '').strip()
        try:
            return float(clean_val)
        except ValueError:
            return np.nan

    df['price'] = df['price'].apply(clean_currency)
    df['original_price'] = df['original_price'].apply(clean_currency)

    #handle missing values => if original price is missing assume its equal to price (no discount)
    df['original_price'] = df['original_price'].fillna(df['price'])
    
    #Standardize shipping (N/A -> Shipping info unavailable)
    df['shipping'] = df['shipping'].replace('N/A', 'Shipping info unavailable').fillna('Shipping info unavailable')

   #remove duplicate rows
    df.drop_duplicates(subset=['title', 'item_url'], keep='first', inplace=True)

    # absolute discount
    df['discount_amount'] = df['original_price'] - df['price']
    
    #discount percentage, np.where to avoid dividing by zero
    df['discount_percentage'] = np.where(
        df['original_price'] > 0,
        (df['discount_amount'] / df['original_price']) * 100,
        0
    )
    #outliers
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]

    df['price'] = df['price'].round(2)
    df['discount_percentage'] = df['discount_percentage'].round(2)

    #export clean data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}. Final row count: {len(df)}")

if __name__ == "__main__":
    clean_ebay_data('ebay_tech_deals.csv', 'cleaned_ebay_deals.csv')