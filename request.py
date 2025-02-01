import requests
# r=requests.get('https://github.com/AmarapuDeepika')
# print(r)
# print(r.content)



# import requests
from bs4 import BeautifulSoup
# r=requests.get('https://github.com/AmarapuDeepika')
# print(r)
# soup=BeautifulSoup(r.content,'html.parser')
# print(soup.prettify())


##retrieve the specific content

# import requests
# from bs4 import BeautifulSoup
# r=requests.get('https://www.geeksforgeeks.org/python-web-scraping-tutorial/')
# print(r)
# soup=BeautifulSoup(r.content,'html.parser')
# s=soup.find('div', class_='wrapper single-page')
# content=soup.find_all('p')
# print(content)


## get the specific website title and name of tags

r=requests.get('https://www.geeksforgeeks.org/python-web-scraping-tutorial/')
soup=BeautifulSoup(r.content, 'html.parser')
print(soup.h1)
print(soup.h1.name)
print(soup.h1.parent.name)



## getting only the data without tags

# import requests
# from bs4 import BeautifulSoup
# r=requests.get('https://www.geeksforgeeks.org/python-web-scraping-tutorial/')
# soup=BeautifulSoup(r.content,'html.parser')
# s=soup.find('div', class_='wrapper single-page')
# content=s.find_all('p')
# for line in content:
#     print(line.text)


