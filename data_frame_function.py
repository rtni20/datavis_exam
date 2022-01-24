import pandas as pd

def get_weather_data():
    # Change file path here
    weather_nyc = pd.read_csv(r'C:\Users\rikke\Documents\AAU\3. semester\DV\datavis_exam\KNYC.csv', sep=';')
    return weather_nyc