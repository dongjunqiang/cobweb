from cobweb.logger import *

l = Logger('/Users/itsmikej/code/python/Cobweb/log/')
l.do_log_simple('foo')
l.do_log('foo', [1, 2, 3], 'default')
