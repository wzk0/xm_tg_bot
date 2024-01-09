import requests
from bs4 import BeautifulSoup

domain='https://www.xmwav.com'
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}

def get_soup(part,params={}):
	r=requests.get(domain+part,params=params,headers=headers)
	return BeautifulSoup(r.text,features='html5lib')

def search(keyword):
	soup=get_soup('/index/search/',params={'action':1,'keyword':keyword})
	result=[]
	result_length=int(soup.find('span',style='font-size:18px;font-weight:bold; color:#F00').text)
	for a in soup.find_all('ul')[1].find_all('a'):
		name=a['title']
		song_id=int(a['href'].replace('.html','').replace('/mscdetail/',''))
		for s in a.find_all('span'):
			if ' 歌曲标签：' in str(s):
				tags=s.text.replace(' 歌曲标签：','').split(',')
			if ' 热度：' in str(s):
				hot=s.text.replace(' 热度：','')
			if '20' in str(s):
				upload_time=s.text
		result.append({'name':name,'song_id':song_id,'tags':tags,'upload_time':upload_time,'hot':hot})
	return {'length':result_length,'data':result}

def get_link(song_id):
	soup=get_soup('/mscdetail/%s.html'%song_id)
	temp_info=soup.find('div',class_='info-zi mb15')
	result=[]
	for a in temp_info.find_all('a'):
		temp_url=a['href']
		if 'www.xmwav.com' in str(temp_url):
			soup=get_soup(temp_url.replace('https://www.xmwav.com',''))
			script_content=soup.find('script').string
			start_index=script_content.find("'")+1
			end_index=script_content.rfind("#'")
			url=script_content[start_index:end_index]
			result.append({'quality':a.text.replace(' ','').replace('\n',''),'url':url})
		else:
			result.append({'quality':a.text.replace(' ','').replace('\n',''),'url':temp_url.replace('#','')})
	return result