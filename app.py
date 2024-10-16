from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a strong secret key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Define the User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Define the Task model for the database

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Make sure this line exists
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """ Home route that redirects to login or task manager depending on login status """
    if 'user' in session:
        return redirect(url_for('task_manager_page'))
    return redirect(url_for('login'))

# ----------- Sign Up Route ------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(phone=phone).first()
        if existing_user:
            return "User with this email or phone number already exists. Please login or use a different email/phone."

        new_user = User(full_name=full_name, email=email, phone=phone, address=address, dob=dob, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.email
        return redirect(url_for('task_manager_page'))

    return render_template('signup.html')

# ----------- Login Route ------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_phone = request.form['email_or_phone']
        password = request.form['password']
        user = User.query.filter((User.email == email_or_phone) | (User.phone == email_or_phone)).first()

        if user and user.password == password:
            session['user'] = user.email
            return redirect(url_for('task_manager_page'))
        else:
            return "Invalid login credentials. Please try again or signup."
    
    return render_template('login.html')

# ----------- Task Manager Route (Requires Login) ------------
@app.route('/task_manager', methods=['GET', 'POST'])
def task_manager_page():
    """
    Route for the task management page where users can add and view tasks.
    """
    # Check if the user is logged in by checking the session
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_email = session['user']  # Get the user's email from the session
    user = User.query.filter_by(email=user_email).first()  # Fetch the user from the database

    # Check if the user object is None (not found in the database)
    if user is None:
        return redirect(url_for('login'))  # Redirect to login if user not found

    # Handle POST request for adding a task
    if request.method == 'POST':
        # Get task data from the form
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()  # Convert string to date
        priority = request.form['priority']  # Get priority from the form

        # Create a new task instance
        new_task = Task(title=title, description=description, due_date=due_date, priority=priority, user_id=user.id)
        db.session.add(new_task)  # Add the new task to the session
        db.session.commit()  # Commit changes to the database
        return redirect(url_for('task_manager_page'))  # Redirect to task manager page

    # Fetch all tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('task_manager.html', tasks=tasks)  # Render the task manager template

# ----------- Show Previous Tasks Route ------------
@app.route('/previous_tasks')
def previous_tasks():
    """
    Route to show all previous tasks for the logged-in user.
    """
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if not

    user_email = session['user']  # Get the user's email from the session
    user = User.query.filter_by(email=user_email).first()  # Fetch the user from the database
    
    # Fetch all tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('previous_tasks.html', tasks=tasks)  # Render the previous tasks template
# ----------- Logout Route ------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

#----------task editing----------------------

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)  # Fetch the task by ID

    if task is None:
        return "Task not found", 404  # Return an error if the task does not exist

    if request.method == 'POST':
        # Update task fields with form data
        task.title = request.form['title']
        task.description = request.form['description']
        
        # Convert due_date from string to date object
        due_date_str = request.form['due_date']
        task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Adjusted to the correct format
        
        task.priority = request.form['priority']
        task.status = request.form['status']
        
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('previous_tasks'))  # Redirect to the previous tasks page

    return render_template('edit_task.html', task=task)  # Render the edit task template

#----------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)  # Use a different port