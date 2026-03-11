import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Load environment variables if dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all domains on all routes
CORS(app)

# Configure SQLAlchemy with a suitable database URI from .env
# Falls back to sqlite if DATABASE_URL is not set
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with your Flask app
db = SQLAlchemy(app)

# Define the Project model
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)

# Define the route for creating new projects
@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
        
    new_project = Project(
        name=data['name'], 
        description=data.get('description', '')
    )
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({
        'id': new_project.id, 
        'name': new_project.name, 
        'description': new_project.description
    }), 201

# Define the route for listing all projects
@app.route('/projects', methods=['GET'])
def list_projects():
    projects = Project.query.all()
    projects_data = [{
        'id': p.id, 
        'name': p.name, 
        'description': p.description
    } for p in projects]
    return jsonify({'projects': projects_data}), 200

# Run the app if this script is executed as the main program
if __name__ == '__main__':
    with app.app_context():
        # Create database tables for our data models
        db.create_all()
    
    # Run server on port 5000
    app.run(debug=True, port=5000)
