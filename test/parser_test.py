from cobweb.parser import *

html_ = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body>
"""


# 自定义解析器
def parser_content(self):
    self.content = self.soup.head
    return self

parser = Parser(None, parser_content)

parser.set_base_url('http://example.com/')
parser.set_html(html_).parse_content().parse_url()

print(parser.get_content())
print(parser.get_url())
