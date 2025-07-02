from django.test import TestCase

# Create your tests here.
import requests
SERPAPI_API_KEY = "7c17e8d16f974503677717bc7627d163d348870502a53b7ab690a8cb601abc4a"

params = {
    "api_key": SERPAPI_API_KEY, 
    "engine": "amazon",
    "num": 10,
    "k": "Protein reconstructor treatments; Strengthening deep conditioners; Protein-rich leaveins"
}

search = requests.get("https://serpapi.com/search", params=params)
response = search.json()
print(response)


# from datetime import date

# # Get today's date
# today = date.today()

# # Define a specific date (e.g., a date in the future)
# specific_date = date(2026, 1, 15)  # January 15, 2026

# # Compare the dates
# if specific_date > today:
#     print(f"The specific date ({specific_date}) is greater than today ({today}).")
# else:
#     print(f"The specific date ({specific_date}) is not greater than today ({today}).")

# # Example with a date in the past
# past_date = date(2024, 6, 1) # June 1, 2024
# if past_date > today:
#     print(f"The past date ({past_date}) is greater than today ({today}).")
# else:
#     print(f"The past date ({past_date}) is not greater than today ({today}).")