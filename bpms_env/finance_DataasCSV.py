import pandas as pd

# Example data
data = {
    'company_name': ['Company A', 'Company B'],
    'report_type': ['Income Statement', 'Balance Sheet'],
    'period_start': ['2020-01-01', '2020-01-01'],
    'period_end': ['2020-12-31', '2020-12-31'],
    'total_revenue': [5000000, 8000000],
    'operating_income': [2000000, 3000000],
    'net_income': [1500000, 2500000],
    'total_assets': [10000000, 12000000],
    'total_liabilities': [4000000, 5000000],
    'cash_from_operations': [2500000, 2700000],
    'cash_from_investing': [-500000, -600000],
    'cash_from_financing': [1000000, 1200000]
}

# Convert to a DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv('financial_data.csv', index=False)
