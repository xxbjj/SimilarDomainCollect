SimilarDomainCollect 基于已知域名发现其他简单相似域名


0.1需求描述：

基于www.baidu.com挖掘 www.baidu.*** 相似网站

基于www.baidu.com挖掘 www.baidu***.com  相似网站

--------------------
0.2功能需求：

1、基于替换实现任意位置的fuzz支持

2、基于httpshttp访问状态判断

3、dns解析状态判断

4、输出结果可用分析

--------------------
0.3代码实现：

基于autoing/domain_fuzz修改实现,如有侵权提示请留言

https://github.com/autoing/domain_fuzz

FuzzDomain原理:

1、使用字符串替换$$处的字符,并进行访问测试。

2、根据不同的报错信息及响应状态判断域名是否存在。【即getip解析和http访问】

支持运行模式：可选dict(域名字典文件)模式(默认)或fuzz(字母排列组合)模式

字典模式：使用字典内的字符串 替换$$位置。默认使用dict-top-domain顶级域名字典

fuzz模式：生成随机的字符串 替换$$位置。

--------------------
0.4简单使用:
λ python3 similardomain.py -h
(['similardomain.py', '-h'],)
FUZZ任意位置的域名 Author by wineZERO

optional arguments:
  -h, --help            show this help message and exit
  -u [URL], --url [URL]
                        目标链接/域名：http://$$.mi.com 表示通过http协议爆破mi.com的子域名，$$为标记点，支持纯域名格式
  -uf [URLFILE], --urlfile [URLFILE]
                        目标链接/域名文件,适用于批量爆破统一域名的类似域名使用
  -of [OUTFILE], --outfile [OUTFILE]
                        输出文件：默认为脚本名称+时间戳
  -t [THREAD], --thread [THREAD]
                        线程：默认20个线程，该参数表示自定义线程数
  -o [OPTIONS], --options [OPTIONS]
                        请求模式：默认GET模式，加上该参数表示使用head请求方式
  -m [MODE], --mode [MODE]
                        运行模式：可选dict模式(默认)或fuzz模式
  -fl FILTERLEVEL, --filterlevel FILTERLEVEL
                        1:输出所有检测记录,2:(默认)输出所有可解析域名记录,3:仅输出可访问域名记录
  -fh FLAGHTTP, --flaghttp FLAGHTTP
                        1:(默认)继承输入url的协议类型,2:同时使用http/https协议,对于纯域名按照http/https协议处理
  -df [DICTFILE], --dictfile [DICTFILE]
                        字典文件：从指定域名字典文件读取字典,会自动处理.字符
  -fs [FUZZSTR], --fuzzstr [FUZZSTR]
                        fuzz字符串：short(默认)标识26个字母可能排序，long表示字母加上0-9,其他输入将直接传递到fuzzstr
  -fr FUZZRANGES, --fuzzranges FUZZRANGES4
                        fuzz范围：默认字典长度为1-4位数所有可能组合，加上该参数表示使用自定义长度。
                        
python3 similardomain.py -u http://baidu.$$.com			#使用http协议与默认域名字典爆破类似 【baidu.**.com】域名,输出能够被dns和request解析的请求

python3 similardomain.py -u http://baidu.$$.com -fl 3		#使用http协议与默认域名字典爆破类似 【baidu.**.com】域名,仅输出能够被request解析的请求

python3 similardomain.py -u http://baidu.$$.com -m dict -df domain.txt	#使用http协议与domain.txt域名字典爆破类似 【baidu.**.com】域名

python3 similardomain.py -u http://baidu.$$.com -m dict -df domain.txt	-fh 2	#使用http/https协议与domain.txt域名爆破类似 【baidu.**.com】域名

python3 similardomain.py -u http://baidu.$$.com -m fuzz -fs short	#使用http协议与26个字母组成字典爆破类似 【baidu.**.com】 域名

python3 similardomain.py -u http://baidu.$$.com -m fuzz -fs abdef	#使用http协议与abdef等字母组成字典爆破类似 【baidu.**.com】 域名

python3 similardomain.py -u http://baidu.$$.com -m fuzz -fs abdef -fh 2	#使用http/https协议与abdef等字母组成字典爆破类似 【baidu.**.com】 域名

输出默认为当前目录下的similardomain.py.result.csv文件

PS:csv格式使用excel或emeditor等编辑器 更便于对比排序。

--------------------
0.5更新记录:

update 1.2.1

简单支持指定文件输出名称

python3 similardomain.py -uf  target.txt -of output.txt

update 1.2

简单支持从文件输入批量域名进行FUZZ

python3 similardomain.py -uf  target.txt

update1.1

基本架构优化实现

--------------------
