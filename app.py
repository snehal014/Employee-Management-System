from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Yogesh%40123@localhost:3306/pythondb1'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(20), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        office = request.form['office']
        age = request.form['age']
        start_date = request.form['start_date']
        new_employee = Employee(name=name, position=position, office=office, age=age, start_date=start_date)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.position = request.form['position']
        employee.office = request.form['office']
        employee.age = request.form['age']
        employee.start_date = request.form['start_date']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
