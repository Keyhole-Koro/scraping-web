import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
import time
import os

user_input = input("Enter url: ")
#highest_url = "https://compe.japandesign.ne.jp/"


lower_links = []

def arrange_current_page(a_current_url):
	links = find_lower_pages(a_current_url)
	print("links",links)
	#lower_links.clear()
	#response = requests.get(a_current_url)
	#soup = BeautifulSoup(response.content, 'html.parser')
	#title = soup.title.string
	name = a_current_url.split("/")[2]
	name_except_toplevel = name.split(".")[0]
	#folder_name = a_current_url.split("/")
	if not os.path.exists(name_except_toplevel):
		os.mkdir(name_except_toplevel)
	os.chdir(name_except_toplevel)
	for link in links:
		print(link)
		read_page(link)
		time.sleep(0.5)
	os.chdir("..")
	print("Current working directory is:", os.getcwd())
	
def find_lower_pages(current_url)->list:
	current_page = requests.get(current_url)
	current_soup = BeautifulSoup(current_page.content, 'html.parser')
	a_tag = current_soup.find_all("a")
	for a in range(len(a_tag)):
		lower_links.append(a_tag[a].get('href'))
	return lower_links
		
def read_page(present_url):
	print(present_url)
	present_page = requests.get(present_url)
	present_soup = BeautifulSoup(present_page.content, 'html.parser')
	
	read_html(present_soup, present_url, present_page)
	download_images(present_soup, present_url)
	
	arrange_current_page(present_url)

def download_images(soup, page_url):
#use below code to aquire urls of images
	img_urls = [img["src"] for img in soup.find_all("img")]
	for img_url in img_urls:
		response = requests.get(page_url)
		soup = BeautifulSoup(response.content, 'html.parser')
		title = soup.title.string
		#extracted_url = page_url.replace(lowest_url, "")
		#new_url = extracted_url+img_url
		with open(title+".png", "wb") as img_file:
			img_file.write(requests.get(img_url).content)

		
def read_html(soup, page_url, got_page):
	response = requests.get(page_url)
	soup = BeautifulSoup(response.content, 'html.parser')
	title = soup.title.string
	with open(title+".html", "w", encoding=got_page.encoding)as txt:
	#with open(page_url, "w", encoding=got_page.encoding)as txt:
		txt.write(got_page.text)
		

arrange_current_page(user_input)
