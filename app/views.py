import requests
import json
import os
from bs4 import BeautifulSoup
from flask import Flask, flash,redirect, render_template, render_template_string, request


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_element(ancestor, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return None
    
selectors = {
    "opinion_id": [None, "data-entry-id"],
    "author": ["span.user-post__author-name"],
    "recommendation": ["span.user-post__author-recomendation > em"],
    "score": ["span.user-post__score-count"],
    "purchased": ["div.review-pz"],
    "published_at": ["span.user-post__published > time:nth-child(1)","datetime"],
    "purchased_at": ["span.user-post__published > time:nth-child(2)","datetime"],
    "thumbs_up": ["button.vote-yes > span"],
    "thumbs_down": ["button.vote-no > span"],
    "content": ["div.user-post__text"],
    "pros": ["div.review-feature__col:has(> div.review-feature__title--positives) > div.review-feature__item",None, True],
    "cons": ["div.review-feature__col:has(> div.review-feature__title--negatives) > div.review-feature__item",None, True]
}
    

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/extraction', methods = ['POST', 'GET'])
def extraction():
    if request.method == 'POST':
        code = request.form['code']

        print(code)
        all_opinions = []
        url = f"https://www.ceneo.pl/{code}#tab=reviews"
        while(url):
            print(url)
            response = requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = {}
                for key, value in selectors.items():
                    single_opinion[key] = get_element(opinion,*value)
                all_opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+get_element(page, "a.pagination__next", "href")
            except TypeError:
                url = None

        try:
            os.mkdir("./opinions")
        except FileExistsError:
            pass
        with open(f"./opinions/{code}.json", "w", encoding="UTF-8") as jf:
            json.dump(all_opinions, jf, indent=4,ensure_ascii=False)
        flash('You have successfully entered code')
        return redirect('product/<int:code>', int(code))
    
    return render_template('extraction.html')

@app.route('/product/<int:code>')
def product(code):
    code = 96685108
    with open(f"./opinions/{code}.json", "r", encoding="UTF-8") as data:
        jsondata = data.read()
    return render_template('product.html',code=code, data=jsondata)

@app.route('/list')
def list_of_products():
    products = [filename.split(".")[0] for filename in os.listdir("./opinions")]
    return render_template("list_of_products.html.", products=products)

@app.route('/author')
def author():
    return render_template('author.html')





if __name__ == '__main__':
    app.run(debug=True)









