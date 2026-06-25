import pandas as pd
import sqlite3

conn = sqlite3.connect(r"C:\Users\vrutupatel\OneDrive\Desktop\uber project\UBER-DATA-ANALYSIS\RAW DATA\uber_data.db3")

trips     = pd.read_sql('SELECT * FROM trips', conn)
drivers   = pd.read_sql('SELECT * FROM drivers', conn)
riders    = pd.read_sql('SELECT * FROM riders', conn)
users     = pd.read_sql('SELECT * FROM users', conn)
locations = pd.read_sql('SELECT * FROM locations', conn)
payments  = pd.read_sql('SELECT * FROM payments', conn)
reviews   = pd.read_sql('SELECT * FROM reviews', conn)
cancels   = pd.read_sql('SELECT * FROM cancellations', conn)

print(f'Trips: {trips.shape}')
print(f'Drivers: {drivers.shape}')
print(f'Riders: {riders.shape}')
print('All tables loaded successfully!')