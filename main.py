import requests
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)
search_types = ['List All', 'Random', 'All Male', 'All Female', 'By Name', 'By Species']
sex_choice = ['Male', 'Female']


class SearchForm(FlaskForm):
    type = RadioField(choices=search_types, validators=[DataRequired()])
    text = StringField("Enter Elephant's Name or Species")
    submit = SubmitField("Search")


URL = 'https://elephant-api.herokuapp.com/elephants'
url = []
url.append(f'{URL}')
url.append(f'{URL}/random')
url.append(f'{URL}/sex/')
url.append(f'{URL}/sex/')
url.append(f'{URL}/name/')
url.append(f'{URL}/species/')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    # Show all elephants.
    response = requests.get(url=url[0]).json()
    if form.validate_on_submit():
        index = search_types.index(form.type.data)
        query_url = url[index]
        if index == 2:
            query_url = query_url + 'male'
        elif index == 3:
            query_url = query_url + 'female'
        elif index > 3:
            query_url = query_url + form.text.data
        # API does not work when name has > 1word.
        if index == 4:
            print(response)
            for elephant in response:
                if elephant['name'].lower() == form.text.data.lower():
                    response = []
                    response.append(elephant)
                    break
        else:
            result = requests.get(url=query_url)
            # API return empty when no data. Bug in API that name has space will return empty result.
            if result.status_code == 200 and result.text != '':
                result = result.json()
                if type(result) is dict:
                    # Single item will return as dict instead of list.
                    response.append(result)
                else:
                    response = result
    return render_template("index.html", form=form, data=response)


if __name__ == "__main__":
    app.run(debug=True)