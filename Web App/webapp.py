from bs4 import BeautifulSoup
from flask import Flask
from flask import request
import codecs

# import orwell

# Global variables
app = Flask(__name__)


with(codecs.open('index.html')) as f:
	html_doc = f.read()

with(codecs.open('index_orig.html')) as of:
	old_html_doc = of.read()

def append_text_marked_with_rules(text, rules, doc):
	# text = orwell.marked_html_from_text(text, rules)	
	soup = BeautifulSoup(doc, 'html.parser')
	print(text)
	analyzed_text = soup.find(id='analyzed_text')
	analyzed_text.append(BeautifulSoup(text, 'html.parser'))
	return soup.prettify()


@app.route("/old")
def old_tag_text():
	print('Got args!')
	print(request.args)
	input_text = request.args.get('text', '')
	rules = request.args.get('rules', '').split(',')
	return append_text_marked_with_rules(input_text, rules, old_html_doc)


@app.route("/")
def tag_text():
	print('Got args!')
	print(request.args)
	input_text = request.args.get('text', '')
	rules = request.args.get('rules', '').split(',')
	return append_text_marked_with_rules(input_text, rules, html_doc)


@app.route('/markfile')
def mark_file():
	filename = request.args.get('filename', '')
	filename = 'static/' + filename
	rules = request.args.get('rules', '').split(',')
	try:
		file = open(filename, 'r')
		file_text = file.read()
		print('Read file!')
	except:
		return('Cannot open file ' + filename)
	return append_text_marked_with_rules(file_text, rules, html_doc)


if __name__ == "__main__":
    app.run()
