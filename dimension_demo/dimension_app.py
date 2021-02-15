import os
from forms import AddForm, DelForm
from flask import Flask, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
# heroku_database_url = 'postgres://tutdwubbdbjifp:08e0b6d5f87f94b7881b70ccb4e97925ac07a62e5b9040121532d6e6f2dccda6@ec2-34-230-167-186.compute-1.amazonaws.com:5432/d1523ss5ad4q8a'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/job_changer"
# app.config['SQLALCHEMY_DATABASE_URI'] = heroku_database_url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db = SQLAlchemy(app)
Migrate(app, db)

#######################
# Models
#######################

class Person(db.Model):

    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    relevant_experience = db.Column(db.Text)
    education_level = db.Column(db.Text)
    major_discipline = db.Column(db.Text)
    company_type = db.Column(db.Text)
    company_size = db.Column(db.Text)
    
    def __init__(self,gender,relevant_experience,education_level,major_discipline,company_type,company_size):
        self.gender = gender
        self.relevant_experience = relevant_experience
        self.education_level = education_level
        self.major_discipline = major_discipline
        self.company_type = company_type
        self.company_size = company_size
        
    def __repr__(self):
        return f'Gender: {self.gender}, Experience: {self.relevant_experience}, Education: {self.education_level}, Major: {self.major_discipline}, ' \
               f'Industry: {self.company_type}, Company Size: {self.company_size}'

    
######
# View functions

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/add', methods=['GET','POST'])
def add_person():
    form = AddForm()
        
    
    if form.validate_on_submit():
        gender = form.gender.data
        relevant_experience = form.relevant_experience.data
        education_level = form.education_level.data
        major_discipline = form.major_discipline.data
        company_type = form.company_type.data
        company_size = form.company_size.data

        new_entry = Person(gender,relevant_experience,education_level,major_discipline,company_type,company_size)
        db.session.add(new_entry)        
        db.session.commit()    

        return redirect(url_for('list_person'))
    
    return render_template('add.html',form=form)


@app.route('/list')
def list_person():
    person = Person.query.all()  
    person = str(person[-1])

    return render_template('list.html', person=person)

@app.route('/predict')
def Model_Prediction():
    # gender = Person.query.all()
    # Gender
    # gender = str(gender[-1]).split()[1].replace(',','')
    # Experience
    # experience = Person.query.all()
    # experience = str(experience[-1]).split()[3:6]
    # experience = ','.join(experience).replace(',',' ')
    
    X = 'Are you likely to change jobs: '
    
    # load model
    # model = joblib.load("HR_LRmodel_trained_V2.h5")
    # # Survey Predictions
    # prediction = model.predict(X)
    # print(f"First 10 Predictions:   {prediction}")
    # print("Model: " + model.__class__.__name__)
    return render_template('predict.html', X=X)

@app.route('/delete', methods=['GET', 'POST'])
def delete_person():

    form = DelForm()
    
    if form.validate_on_submit():
        id = form.id.data
        person = Person.query.get(id)
        try:  
            db.session.delete(person)
            db.session.commit()   
        except:
            db.session.rollback()     

        return redirect(url_for('list_person'))
    
    return render_template('delete.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)