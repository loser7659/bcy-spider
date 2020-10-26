import requests
import json
import re
import os
import threading

def Requests(url):
	head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
	n = 0
	while True:
		n += 1
		try:
			response = requests.get(url,headers = head,timeout = 10)
		except:
			pass
		else:
			if response.status_code == 200:
				return response
			if n >= 10:
				return False


def folder_mkdir():
	if os.path.exists(os.getcwd()+'\\pic'):
		pass
	else:
		os.mkdir(os.getcwd()+'\\pic')

	folder = os.getcwd()+'\\pic\\'

	return folder


def install_img(url,folder,name):
	try:
		img_content = Requests(url).content
	except:
		print('错误：{}     名称：{}'.fomat(url,name))
	else:
		open(folder+name,'wb').write(img_content)



def get_data(item_host_url):
	mode = 'thread'  #多线程下载模式
	folder = folder_mkdir()
	item_response = Requests(item_host_url)
	if item_response == False:
		return
	item_response.encoding = 'utf-8'
	try:
		item_data = re.findall('window.__ssr_data = JSON.parse\("(.*?)"\);\n      window._UID_ = \'0\';',item_response.text)[0].replace('\\"','"').replace('u002F','').replace('\\\\','/')
	except:
		pass
	else:
		item_img_data = json.loads(item_data,strict=False)['detail']['post_data']['multi']
		num = len(os.listdir(folder))
		print(num)
		for img_data in item_img_data:
			img_url = img_data['original_path']
			if img_url.find('jpg') >= 0:
				img_fomat = '.jpg'
			elif img_url.find('png') >= 0:
				img_fomat = '.png'
			else:
				img_fomat = '.jpg'

			num += 1
			name = str(num)+img_fomat
			if mode == 'thread':
				t = threading.Thread(target = install_img,args = (img_url,folder,name)).start()
				while True:
					if len(threading.enumerate()) <= 25:
						break
			else:
				install_img(img_url,folder,name)

if __name__ == '__main__':
	item_host_url = 'https://bcy.net/item/detail/6632162902138683652'
	get_data(item_host_url)
	print('下载完成')
