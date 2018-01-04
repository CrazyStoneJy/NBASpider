# !/usr/bin/python3
# -*- encoding:utf-8 -*-

from lxml import etree

def print_element(element):
    string = etree.tostring(element,pretty_print=True).decode('utf-8')
    print(string)
# 打开html文件
selector = etree.parse('demo.html')
# print_element(selector)
# 获取class为main的div标签
main_div = selector.xpath('//div[@class="main"]')
# print_element(main_div[0])
# 读取main_div中的div/p中的文字信息
# text = main_div[0].findtext('div/p')
# print(text)
# 获取main_div中的所有li标签
lis = main_div[0].findall('ul/li')
for li in lis:
    # print_element(li)
    link = li.find('a')
    # 获取a标签中href的属性
    url = link.get('href')
    # print(url)
    # 在循环中获取li的a标签的文字
    link_text = link.xpath('string(.)')
    print(link_text)

html = '''
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>Html parse demo</title>
</head>
<body>
<div class="main">
    <div class="first">
        <img src="http://www.sinaimg.cn/dy/slidenews/21_img/2017_27/41065_5741488_547160.jpg" width="200px" height="200px" alt="美女图片"/>
        <p>这是文字</p>
    </div>
    <ul class="first">
        <li><a href="http://www.baidu.com">百度</a></li>
        <li><a href="http://www.zhihu.com">知乎</a></li>
        <li><a href="http://www.google.com">google</a></li>
        <li><a href="http://www.qq.com">QQ</a></li>
    </ul>
</div>

</body>
</html>
'''
# html_selector = etree.HTML(html)
# print_element(html_selector)