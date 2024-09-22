from flask import Flask, render_template
from os import read
from pickle import FALSE, TRUE
from pandas.io.parsers.readers import read_csv
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import smtplib
import re
#import mailtrap as mt
import textile 
import html

# create list for areas of interest
l = ["Russia", "China", "Chinese", "Iran", "Iranian", "Iranian","Microsoft", "Cisco"]

data1 = ''

def url1():
    global data1
    global l
    url = "https://thehackernews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='story-link')

    for article in articles:
        header = article.find('h2', class_='home-title').get_text()
        description = article.find('div', class_='home-desc').get_text()
        #print(article['href'])
        response1 = requests.get(article['href'])
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        cves = re.findall(r'CVE-\d{4}-\d{4,}', str(soup1))
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\[\.\]\d{1,3}', str(soup1))

        if any(word in header for word in l) or any(word in description for word in l):
            cves = str(cves)
            cves = cves.replace("[", "")
            cves = cves.replace("]", "")
            ips = str(ips)
            ips = ips.replace("[", "")
            ips = ips.replace("]", "")
            data = header+ ":" + "\n\n" + description[0:500]+"..." + "\n\n" + "CVEs \n" + cves + "\n" + "IPs\n" + ips + "\n\n" +article['href'] + "\n\n" + "\n\n"
            data = str(data)
            data = re.sub(r'\t', '',data)
            data1 = data1 + "\n\n\n\n" + data

def url2():
  global data1
  global l
  url = "https://www.bleepingcomputer.com/"
  response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'})
  soup = BeautifulSoup(response.text, 'html.parser')
  articles = soup.find_all('li')


  for article in articles:
    header = article.find('h4')
    description = article.find('p')
    link = article.find('a', href=True)
    #link = str(link['href'])
    #link = re.findall(r'(?:https?|ftp):\/\/[^\s/$.?#].[^\s]+', link)
    

    if header is not None and description is not None:
      header1 = header.text.strip()
      description1 = description.text.strip()
      
      if any(word in header1 for word in l) or any(word in description1 for word in l):
        response1 = requests.get(link['href'])
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        cves = re.findall(r'CVE-\d{4}-\d{4,}', str(soup1))
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', str(soup1))
        cves = str(cves)
        ips = str(ips)
        ips = ips.replace("0.0.1.1", "")
        ips = ips.replace("1.1.1.1", "")
        ips = ips.replace("\'", '')
        ips = ips.replace(",", ' ')
        cves = cves.replace("[", "")
        cves = cves.replace("]", "")
        ips = ips.replace("]", "")
        ips = ips.replace("[", "")
        data = header1 + ":" + "\n\n" + description1[0:500] + "..." + "\n\n" + "CVEs \n" + cves + "\n" + "IPs\n" + ips + "\n\n" + str(link['href']) + "\n\n"
        data = data
        data1 = data1 + "\n\n\n\n" + data


def convert_to_html():
   global data1
   url_pattern = r'http[s]?://[^\s]+'
   data1 = textile.textile(data1)
   for x in data1:
    url = re.search(url_pattern, x)
    url = str(url).replace("<p>","")
    print("URL:" + url)



    #if x.startswith(word1):
      #x1 = x.replace("<p>", "")
      #x1 = "<a href=" + x1 + ">" + "</a>"


if __name__ == "__main__":
  url1()
  url2()
  convert_to_html()
  print("Intel Gathered...\n\nConverted to html.....\n\n")

  with open('intel.txt', 'w') as f:
    f.write(data1)
    f.close()
    print("intel.txt created....\n\n")


######### Add reformat html code here ##########


# Make all of the links clickable
def process_file1(input_file, output_file):
    # Define the regex pattern to find URLs surrounded by <p> and </p>
    pattern = re.compile(r'<p>(http[s]?://[^\s]+)</p>')

    # Read the content of the file
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace <p> and </p> with HTML anchor tags
    updated_content = pattern.sub(r'<a href="\1">\1</a>', content)

    # Write the updated content back to the file
    with open(output_file, 'w') as file:
        file.write(updated_content)

# Specify your input and output file paths
input_file_path = 'intel.txt'   # Change this to your actual input file path
output_file_path = 'final.txt' # Change this to your desired output file path

# Call the function to process the file
process_file1(input_file_path, output_file_path)


print("final.txt Updated")