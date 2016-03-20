from cobweb.downloader import *

d = Downloader()
data = d.get("http://www.baidu.com/").decode('utf8')
print(data)
