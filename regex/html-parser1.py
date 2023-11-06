from html.parser import HTMLParser


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("{:5} : {}".format("Start", tag))
        for name, value in attrs:
            print(f"-> {name} > {value}")

    def handle_endtag(self, tag):
        print("{:5} : {}".format("End", tag))

    def handle_startendtag(self, tag, attrs):
        print("{:5} : {}".format("Empty", tag))


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
html = "".join(input() for _ in range(int(input())))
parser.feed(html)


INPUT = """<html><head><title>HTML Parser - I</title></head>\n
<body data-modal-target class='1'><h1>HackerRank</h1><br /></body></html>"""

OUTPUT = """Start : html
    Start : head
    Start : title
    End   : title
    End   : head
    Start : body
    -> data-modal-target > None
    -> class > 1
    Start : h1
    End   : h1
    Empty : br
    End   : body
    End   : html """
