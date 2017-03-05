import requests
from PIL import Image
from bs4 import BeautifulSoup


s=requests.session()
headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            'Connection': 'keep-alive',
            'Referer':"http://jwxt.bupt.edu.cn/",
}
response = s.get('http://jwxt.bupt.edu.cn/validateCodeAction.do?random=',headers=headers)
with open('cha.jpg','wb') as f:
    f.write(response.content)
    f.close()
try:
    im=Image.open('cha.jpg')
    im.show()
    im.close()
except:
    print("请到当前目下去找cha.jpg输入验证码")
cha_code=input("请输入验证码")

headers1={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Referer":"http://jwxt.bupt.edu.cn/jwLoginAction.do",
    "Connection":"keep-alive",
}
postdata={
    "type":"sso",
    "zjh":"*****",#输入学号
    "mm":"*****",#输入密码
    "v_yzm":cha_code,
}

response1=s.post('http://jwxt.bupt.edu.cn/jwLoginAction.do',data=postdata,headers=headers1)
# print(response1.text)
headers2={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Referer":"http://jwxt.bupt.edu.cn/gradeLnAllAction.do?type=ln&oper=qb",
    "Connection":"keep-alive",
}
url="http://jwxt.bupt.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA%B5%DA%D2%BB%D1%A7%C6%DA(%C7%EF)(%C8%FD%D1%A7%C6%DA)#qb_2016-2017%E5%AD%A6%E5%B9%B4%E7%AC%AC%E4%B8%80%E5%AD%A6%E6%9C%9F(%E7%A7%8B)(%E4%B8%89%E5%AD%A6%E6%9C%9F)"
response2=s.post(url,headers=headers2)
html=response2.text
# print(html)
soup=BeautifulSoup(html,'lxml')
all_tr=soup.find_all('tr', class_='odd')
# print(all_tr)
total=[]
for td in all_tr:
    tdd=td.find_all('td')
    if str(tdd[5].get_text().strip().replace('\r\n',''))=="任选":
        continue
    item=[]#0为科目名称1为学分2为成绩
    kemu=tdd[2].get_text().strip().replace('\r\n','')#2为科目名称 4为学分 5为类型
    item.append(kemu)
    xuefen=tdd[4].get_text().strip().replace('\r\n','')
    item.append(xuefen)
    score=td.find_all('p')[0].get_text().replace('\xa0','')
    if score=="免修":
        score='90'
    item.append(score)
    total.append(item)


print(total)


total_xuefen=0
total_fenshu=0
for i in total:
    total_xuefen+=float(i[1])
    total_fenshu+=float(i[1])*float(i[2])

GPA=(total_fenshu)/(total_xuefen)
print(GPA)


