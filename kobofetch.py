from koboextractor import KoboExtractor
import pandas as pd
import folium

my_token = 'a0cf7f53ebbe302eda9180f157d3ebb5d107ffa9'
form_id = 'amxqLY9raqMLGDeXtadZ32'
kobo_base_url= 'https://kf.kobotoolbox.org/api/v2'

# Initialize the instance of KoboExtractor
kobo = KoboExtractor(my_token, kobo_base_url)

# Function to fetch all data with pagination
def fetch_all_data(kobo, form_id):
    all_data = []
    start = 0
    limit = 1000  # You can adjust this limit as needed
    while True:
        data = kobo.get_data(form_id, query=None, start=start, limit=limit, submitted_after=None)
        results = data['results']
        if not results:
            break
        all_data.extend(results)
        start += limit
    return all_data

# Fetch all data
all_data = fetch_all_data(kobo, form_id)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(all_data)

# Assuming the data contains 'latitude' and 'longitude' columns
print(df.head())
print(f"Total records fetched: {len(df)}")

df[['latitude', 'longitude', 'acc', 'alt']] = df['Location'].str.split(' ', expand=True).astype(float)

# Create a map centered around the mean latitude and longitude
map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

# Add markers for each data point
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']]).add_to(map)

# Save the map as an HTML file
map.save(r'.\map2.html')
