from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

with open("config.json", "r") as read_file:
    data = json.load(read_file)

EMAIL = data["EMAIL"]
PASSWORD = data["PASSWORD"]
LINK = data["LINK"]
options = Options()
driver = webdriver.Chrome("C:/Users/Priyans Nishithkumar/Desktop/chromedriver.exe",chrome_options=options)
driver.get("https://www.linkedin.com/login")
try:
    email = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
except:
	print("No")

email = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
key = driver.find_element_by_class_name("btn__primary--large")
email.send_keys(EMAIL)
password.send_keys(PASSWORD)
key.click()
driver.implicitly_wait(10)
driver.get(LINK)
elem = driver.find_element_by_class_name("feed-shared-update-v2__comments-container")
all_a_tags = elem.find_elements_by_tag_name("a")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
s = set()
while True:
	try: 
		more_comments = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.ID, "show_prev")))
		more_comments.click()
		try:
			all_comments = WebDriverWait(elem, 2000).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
			all_comments = elem.find_elements_by_tag_name("article")
		except:
			print("Error1")
		old_s = s.copy()
		s.update(all_comments)
		if (old_s == s):
			break
	except:
		print("Error")
		break
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
all_links = []
all_names = {}
for item in s:
	link = item.find_element_by_tag_name("a")
	link_name = link.get_attribute("href")
	all_links.append(link_name)
	experience = []
	link_clicked = driver.get(link_name)
	try:
		profile = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "flex-1")))
	except:
		print("Profile not parsed")
	profile = driver.find_element_by_class_name("flex-1")
	name = driver.find_element_by_class_name("break-words").text
	profession = driver.find_element_by_tag_name("h2").text
	location = driver.find_elements_by_class_name("pv-top-card-v3--list")[1].find_element_by_tag_name("li").text
	section_exp = driver.find_element_by_id("oc-background-section")
	section_exp_items = section_exp.find_elements_by_tag_name("ul")
	for item in section_exp_items:
		list_items = item.find_elements_by_tag_name("li")
		for item1 in list_items:
			experience.append(item1.text)
	all_names[name] = {'profession':profession, 'location':location, 'experience':experience}
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")	
	try:
		profile = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "pv-skill-categories-section")))
		skills = driver.find_element_by_class_name("pv-skill-categories-section")
		all_names[name]['skills'] = skills.text
	except:
		print("skills not found")
	try:
		accom = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "pv-accomplishments-section")))
		accomplishments = driver.find_element_by_class_name("pv-accomplishments-section")
		all_names[name]['accomplishments'] = accomplishments.text
	except:
		print("accomplishments not found")	
	try:
		show_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pv-profile-section__card-action-bar")))
		show_more.click()
		show_more = driver.find_element_by_id("skill-categories-expanded")
		all_names[name]['skills'] += show_more.text
	except:
		print("more not found")
	print(all_names[name])
