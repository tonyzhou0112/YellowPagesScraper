# YellowPagesScraper
This python script allows users to scrape details of business based on keywords and location

Downloading the urls of yellow pages fron linkextractor.py

  Navigate to linkextractor.py
  Change the keywords in the list for the desired keywords to scrape (Restaurants, Towing etc)
  Change the lists to the requited location (CA,AL,NY etc)
  Run the file as scrapy runspider linkextractor.py
  The urls gets download according to the keywords name as Restaurants.txt, Towing.txt etc
  
  
  Navigate to newdo.py
  Change the filenames list data to the files download (Restaurants.txt, Towing.txt etc)
  Run the file as scrapy runspider newdo.py
  
  
  The script currently gather Name,Phone, Website, Addresss, Street, City, State, Zip, URL and Fax 
  
  
  

