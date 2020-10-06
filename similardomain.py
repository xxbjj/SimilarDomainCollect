import re
import time
import html
import sys
from argparse import ArgumentParser ,SUPPRESS
import queue
import requests
import threading
from itertools import product
from urllib.parse import urlparse
requests.packages.urllib3.disable_warnings()

##################
open_result=''

filename = sys.argv[0]+'.log'
logfile = open(filename,'a+',buffering=1) 
def output(*tuple):
	print(tuple)
	print(tuple,file=logfile)

def get_file_type(file_path):
	file_type = "gb2312"
	try:
		htmlf = open(file_path, 'r', encoding=file_type)
		htmlf.read()
	except UnicodeDecodeError:
		file_type = "utf-8"
	else:
		htmlf.close()
	return file_type
def load_file(dict_file):
	dict=''
	file_type = get_file_type(dict_file)
	try:	
		dict = open(dict_file,'r',encoding=file_type, errors='ignore') 
	except:
		output("请确认字典文件'+dict_file+’是否存在！！！！！")
		exit()
	dictList = dict.read().splitlines() 
	return dictList
##################
def get_title(response):
	encoding = response.apparent_encoding
	try:
		title =  re.findall(b'<title>(.*?)</title>',response.content,re.S|re.M|re.I)[0]
		try:
			return ''.join(html.unescape(re.sub('\s{2,}',' ',title.decode())).replace(' ','_').split()).replace('_',' ').strip()
		except Exception as e:
			try:
				return ''.join(html.unescape(re.sub('\s{2,}',' ',title.decode('gbk'))).replace(' ','_').split()).replace('_',' ').strip()
			except Exception as e:
				try:
					return ''.join(html.unescape(re.sub('\s{2,}',' ',title.decode(encoding.lower()))).replace(' ','_').split()).replace('_',' ').strip()
				except Exception as e:
					return ''
	except Exception as e:
		return ''
##################
class GetUrl(object):
	def __init__(self):
		super(GetUrl, self).__init__()
		self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'}

	def geturl(self,url):
		response=''
		try:
			if Options == "GET":
				response = requests.get(url, verify=False, headers=self.headers, allow_redirects=False,timeout = 5)
			if Options == "HEAD":
				response = requests.head(url, verify=False, headers=self.headers, allow_redirects=False,timeout = 5)
			try:
				location = response.headers['Location']
				self.host = urlparse(url)
				self.scheme = self.host.scheme
				self.netloc = self.host.netloc
				if location.lower().startswith("http"):
					url = location
				elif location.lower().startswith("/"):
					url = f'{self.scheme}://{self.netloc}{location}'
				elif location.lower().startswith("/") == False and self.netloc.split(':')[0] in location.lower():
					url = f'{self.scheme}://{location}'
				elif location.lower().startswith("/") == False and self.netloc.split(':')[0] not in location.lower():
					url = f'{self.scheme}://{self.netloc}/{location}'
				#return self.geturl(url)
				response.url=url
				self.geturl(url)
				return response
			except Exception as e:
				#output(e)
				return response
		except Exception as e:
			if  "getaddrinfo failed" in str(e):
				result = '{},getipError,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <2 : open_result.write(result+'\n')
			elif  "connect timeout" in str(e):
				result = '{},connTimeout,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <3 : open_result.write(result+'\n')
			elif  "read timeout" in str(e):
				result = '{},readTimeout,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <3 : open_result.write(result+'\n')
			elif  "Failed to establish" in str(e):
				result = '{},establishErroe,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <2 : open_result.write(result+'\n')
			elif  "SSLError" in str(e):
				result = '{},SSLError,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <2 : open_result.write(result+'\n')
			else:
				output(url,e)
				result = '{},otherError,NoBackurl,NoTitle,NoLenth'.format(url)
				output(result)
				if filter_level <2 : open_result.write(result+'\n')
			pass

class Asset(threading.Thread):
	def run(self):
		if input_url_list !=[]: 
			while True:
				while not waittask.empty():
					for url in input_url_list :
						urllist=[]
						url = url.replace('$$',f'{waittask.get()}').replace('..','.').strip()
						if flag_http >=2 :
							url = url.split('://')[-1]
						if 'http' not in url:
							urllist.extend(['http://'+url , 'https://'+url])
						else:
							urllist.append(url)
						for url in urllist:
							response = GetUrl().geturl(url)
							if response:
									status = response.status_code
									backurl = response.url
									title = get_title(response)
									length = len(str(response))
									if title:
										#output('进度：{:.2%} 原始链接：{} 状态码：{} 跳转链接：{} 标题：{}'.format(1-waittask.qsize()/sums,url,status,backurl,title))
										#output('原始链接：{} 状态码：{} 跳转链接：{} 标题：{}'.format(url,status,backurl,title))
										result = '{},{},{},"{}",len[{}]'.format(url,status,backurl,title,length)
										output(result)
										open_result.write(result+'\n')
									else:
										title = 'NoTitle'
										result = '{},{},{},NoTitle,len[{}]'.format(url,status,backurl,length)
										output(result)
										open_result.write(result+'\n')
				exit()
		else:
			output('input urls is Empty')
			exit()

def main():
	global open_result
	if out_file != None:
		result_file = out_file
	else:
		now_time = str(time.time()).split('.')[0]
		result_file ='{}.{}.csv'.format(sys.argv[0],now_time )
	output('result_file',result_file)
	open_result = open(result_file,'w+',buffering=1024) 
	for dicts in dictslist:
		waittask.put(''.join(dicts))
	dictslist.clear()
	global sums
	sums = waittask.qsize()
	for i in range(1,int(args.thread)):
		asset = Asset()
		asset.start()

	
if __name__ == '__main__':
	output(sys.argv)
	parser = ArgumentParser(description='FUZZ任意位置的域名 Author by wineZERO',prog="",usage=SUPPRESS)
	parser.add_argument('-u', '--url', default=None, nargs='?', help='目标链接/域名：http://$$.mi.com 表示通过http协议爆破mi.com的子域名，$$为标记点，支持纯域名格式')	
	parser.add_argument('-uf', '--urlfile', default=None, nargs='?', help='目标链接/域名文件,适用于批量爆破统一域名的类似域名使用')
	parser.add_argument('-of', '--outfile', default=None, nargs='?', help='输出文件：默认为脚本名称+时间戳')
	
	parser.add_argument('-t', '--thread', default=20, nargs='?', help='线程：默认20个线程，该参数表示自定义线程数')
	parser.add_argument('-o', '--options', default='get', nargs='?',help='请求模式：默认GET模式，加上该参数表示使用head请求方式')
	parser.add_argument('-m', '--mode', default='dict', nargs='?', help='运行模式：可选dict模式(默认)或fuzz模式')

	parser.add_argument('-fl', '--filterlevel', type=int, default=2, help='1:输出所有检测记录,2:(默认)输出所有可解析域名记录,3:仅输出可访问域名记录')
	parser.add_argument('-fh', '--flaghttp', type=int, default=1, help='1:(默认)继承输入url的协议类型,2:同时使用http/https协议,对于纯域名按照http/https协议处理')
	parser.add_argument('-df', '--dictfile', default='domain-top.txt', nargs='?', help='字典文件：从指定域名字典文件读取字典,会自动处理.字符')
	parser.add_argument('-fs', '--fuzzstr', default='short', nargs='?', help='fuzz字符串：short(默认)标识26个字母可能排序，long表示字母加上0-9,其他输入将直接传递到fuzzstr')
	parser.add_argument('-fr', '--fuzzranges', default='1-4', help='fuzz范围：默认字典长度为1-4位数所有可能组合，加上该参数表示使用自定义长度。')
	args = parser.parse_args()
	filter_level =  args.filterlevel
	flag_http = args.flaghttp
	out_file= args.outfile
	input_url_list = []
	input_url = args.url
	url_file = args.urlfile
	if input_url !=None:
		input_url_list.append(input_url)
	elif url_file !=None:
		input_url_list =load_file(url_file)
		print(input_url_list)
	else:
		output('No Any Target Input Error !!!')
		exit()
	if args.options.lower() == 'head':
		Options = 'HEAD'
	else:
		Options = 'GET'
	if args.mode.lower() == 'fuzz':
		#output("使用Fuzz模式")
		if args.fuzzstr == 'short':
			fuzzstr = 'abcdefghijklmnopqrstuvwxyz'
			output("使用Fuzz模式")
			output("fuzzstr",fuzzstr)
		elif args.fuzzstr.lower() == 'long':
			fuzzstr = 'abcdefghijklmnopqrstuvwxyz0123456789'
			output("使用Fuzz模式")
			output("fuzzstr",fuzzstr)
		else:
			fuzzstr = args.fuzzstr.strip()
			output("使用Fuzz模式")
			output("fuzzstr",fuzzstr)
		if len(args.fuzzranges.split('-')) == 2:
			dictslist = []
			start,end = int(args.fuzzranges.split('-')[0]),int(args.fuzzranges.split('-')[1])
			for i in range(start,end+1):
				result = product(fuzzstr, repeat=i)
				dictslist.extend(list(result))
		else:
			dictslist = []
			result = product(fuzzstr, repeat=int(args.fuzzranges))
			dictslist.extend(list(result))
	else:
		#output("使用Dict模式")
		if args.dictfile != '' :
			dictslist = []
			dictfile = args.dictfile 
			output("使用Dict模式：",dictfile)
			result = load_file(dictfile)
			#output(result)
			dictslist.extend(list(result))
	waittask = queue.Queue()
	main()
