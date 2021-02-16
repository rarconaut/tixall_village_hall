import os
from flask import Flask, render_template, session, url_for, request, redirect


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# View functions
#################################################

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