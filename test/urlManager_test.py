from cobweb.urlManager import *


u = UrlManager()
u.add_new('http://www.foo.com/')
u.add_new('http://www.bar.com/')

u.move(u.get_wait_url())
print(u.urls_done, u.urls_wait)
