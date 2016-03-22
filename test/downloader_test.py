from cobweb.downloader import *

d = Downloader()
data = d.get("http://www.baidu.com/")
print(data)
