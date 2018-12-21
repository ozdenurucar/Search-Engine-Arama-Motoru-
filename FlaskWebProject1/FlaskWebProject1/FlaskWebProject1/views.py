"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from FlaskWebProject1 import app
from FlaskWebProject1.functions import *
from FlaskWebProject1.classes import *

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/keyword_count')
def keyword_count():
    """Renders the keyword count page."""
    return render_template(
        'keyword_count.html',
        year=datetime.now().year,
    )

urls = [""]
keywords = [""]
websites=[""]

@app.route('/keyword_count/',methods = ["POST"])
def get_count():
    url = request.form["URL"]
    keyword = request.form["keyword"]
    count = get_keyword_count(url,keyword)
    return render_template('keyword_count.html', 
                           result = count,
                           year=datetime.now().year,)

@app.route('/URL_sorting/')
def URL_sorting():
    urls.clear()
    urls.append("")
    keywords.clear()
    keywords.append("")
    return render_template(
        'URL_sorting.html',
        year=datetime.now().year,

    )

@app.route('/URL_sorting/', methods = ["POST"])
def add_items():
    if 'add_url' in request.form:
        urls.append(request.form["URL"])
        print(urls)
    elif 'add_keyword' in request.form:
        keyword = request.form["keyword"]
        keywords.extend(keyword.split())
        print(keywords)
    elif 'results' in request.form:
        res = url_sorting(keywords,urls)    
        output = "<tr><th>PUAN</th><th>URL</th></tr>"
        for it in res[0][::-1]:
            if it[0] is not 0:
                output += "<tr>"
                output += "<td>%s</td><td>%s</td>" % (it[0],it[1])
                output += "</tr>" 
        
        output2 = "<tr><th>KEYWORDS</th><th>URLS</th></tr>"
        for it in res[1]:
            if it is not "": 
                output2 += "<tr><td>%s</td>" % (it)
                for iter in res[1][it][::-1]:
                    if iter[1] is not "":
                        output2 += "<td>%s</td><td>%s</td>" % (iter[0],iter[1])
                output2 += "</tr>"
        print(res)
        return render_template(
        'URL_sorting.html',
        table1 = output,
        table2 = output2,
        year=datetime.now().year,
        )
    elif 'reset' in request.form:
        urls.clear()
        urls.append("")
        keywords.clear()
        keywords.append("")
        output = ""
        output2 = ""
        return render_template(
        'URL_sorting.html',
        table1 = output,
        table2 = output2,
        year=datetime.now().year,
        )



    return render_template(
        'URL_sorting.html',
        year=datetime.now().year,
    )

@app.route('/website_sorting/')
def website_sorting():
    websites.clear()
    websites.append("")
    keywords.clear()
    keywords.append("")
    return render_template(
        'website_sorting.html',
        year=datetime.now().year,
    )

@app.route('/website_sorting/', methods = ["POST"])
def add_item():
    if 'add_website' in request.form:
        urls.append(request.form["WebSite"])
        print(urls)
    elif 'add_keyword' in request.form:
        keyword = request.form["keyword"]
        keywords.extend(keyword.split())
        print(keywords)
    elif 'results' in request.form:
        res = []
        for i in range(len(urls)):
            if urls[i] is not "":
                res.append(site(urls[i],keywords))
        output = "<tr><th>URL</th><th>ANAHTAR KELIME VE GECME SAYISI</th></tr>"
        for it in res:
            output += "<tr><th>%s</th>" % it.name
            key_count = it.get_keywords_counts()
            for word in key_count:
                output += "<th>%s</th><th>%s</th>" % (word,key_count[word])
            output += "</tr>"         
        output2 = "<tr><th>TREE</th></tr>"
        for it in res:
            output += "<tr><th>%s</th><th></th><th></th>" % (it.name)
            for words in it.keywords_counts:
                output += "<th>%s</th>th>%s</th>" % (words,it.keywords_counts[words])
            output += "</tr>"
            for page in it.second_depth:
                output += "<tr><th></th><th>%s</th>" % (page.name)
                for word in page.keywords_counts:
                    output += "<th>%s</th><th>%s</th>" % (word, page.keywords_counts[word])
                output += "</tr>"
                for sec_page in it.second_depth[page]:
                    output += "<tr><th></th><th></th><th>%s</th>" % (sec_page.name)
                    for word in sec_page.keywords_counts:
                        output += "<th>%s</th><th>%s</th>" % (word, sec_page.keywords_counts[word])
                    output += "</tr>"


        print(res)
        return render_template(
        'website_sorting.html',
        table1 = output,
        table2 = output2,
        year=datetime.now().year,
        )
    elif 'reset' in request.form:
        urls.clear()
        urls.append("")
        keywords.clear()
        keywords.append("")
        output = ""
        output2 = ""
        return render_template(
        'website_sorting.html',
        table1 = output,
        table2 = output2,
        year=datetime.now().year,
        )

    return render_template(
        'website_sorting.html',
        year=datetime.now().year,
    )

@app.route('/semantik_analiz/')
def semantik_analiz():
    websites.clear()
    websites.append("")
    keywords.clear()
    keywords.append("")
    return render_template(
        'semantik_analiz.html',
        year=datetime.now().year,
    )

@app.route('/semantik_analiz/', methods = ["POST"])
def add():
    if 'add_website' in request.form:
        websites.append(request.form["WebSite"])
        print(urls)
    elif 'add_keyword' in request.form:
        keyword = request.form["keyword"]
        keywords.extend(keyword.split())
        print(keywords)
    elif 'results' in request.form:
        res = get_synonyms(keywords)
        print(res)
        output="<tr><th> Yeni Anahtar Kelime Kümesi</th></tr>"
        for i in res:
            output += "<tr>"
            output += "<td>%s</td>" % i
            output += "</tr>" 
        return render_template(
        'semantik_analiz.html',
        table1=output,
        year=datetime.now().year,
        )
    elif 'reset' in request.form:
        urls.clear()
        urls.append("")
        keywords.clear()
        keywords.append("")
        output = ""
        return render_template(
        'semantik_analiz.html',
        table1 = output,
        year=datetime.now().year,
        )

    return render_template(
        'semantik_analiz.html',
        year=datetime.now().year,
    )