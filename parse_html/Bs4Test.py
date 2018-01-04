# !/usr/bin/python3
# -*- encoding:utf-8 -*-

from bs4 import BeautifulSoup

html = '''
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
   <span class="first second">
    Hello World
   </span>
  </p>
  <div class="test">
  <!-- 这是注释  -->
  </div>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link2">
    Tillie
   </a>
   ; and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
'''

# soup = BeautifulSoup(open('demo.html'),'lxml')
# print(soup)

soup = BeautifulSoup(html,'lxml')
# print(soup)

# # 查找class为sister的a标签
# links = soup.find_all('a',{'class':'sister'})
# links = soup.find_all('a',class_='sister')
# # 获取a标签中的href属性
# for link in links:
#     # print(link)
#     a = link.get('href')
#     print(a)
#     print(link.get_text())

# span = soup.find('span',{'class':'first'})
# print(span)

# print(soup.a.string)

# print(soup.prettify())
