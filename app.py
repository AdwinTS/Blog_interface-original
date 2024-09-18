from flask import Flask, request, jsonify, render_template
import bcrypt
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"
BLOGS_FILE = "blogs.json"

def load_datafromfile(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_data_after_updation(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password').encode('utf-8')
    users = load_datafromfile(USERS_FILE)
    
    if username in users:
        return jsonify({"message": "Username already exists."}), 400
    
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    users[username] = hashed_password.decode('utf-8')
    save_data_after_updation(USERS_FILE, users)
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def authenticate_user():
    data = request.json
    username = data.get('username')
    password = data.get('password').encode('utf-8')
    users = load_datafromfile(USERS_FILE)
    
    if username not in users:
        return jsonify({"message": "Username not found."}), 400
    
    hashed_password = users[username].encode('utf-8')
    if bcrypt.checkpw(password, hashed_password):
        return jsonify({"message": "Login successful!", "username": username})
    else:
        return jsonify({"message": "Incorrect password."}), 400

@app.route('/create_blog', methods=['POST'])
def create_blog():
    data = request.json
    username = data.get('username')
    title = data.get('title')
    content = data.get('content')
    blogs = load_datafromfile(BLOGS_FILE)
    
    if username not in blogs:
        blogs[username] = []
    
    blogs[username].append({"title": title, "content": content})
    save_data_after_updation(BLOGS_FILE, blogs)
    return jsonify({"message": "Blog post created successfully!"})

@app.route('/modify_blog', methods=['POST'])
def modify_blog():
    data = request.json
    username = data.get('username')
    index = int(data.get('index'))  # Convert to integer
    new_title = data.get('new_title')
    new_content = data.get('new_content')
    blogs = load_datafromfile(BLOGS_FILE)
    
    if username not in blogs or index >= len(blogs[username]):
        return jsonify({'message': 'Invalid blog index or username'}), 400
    
    # Modify the blog
    blogs[username][index] = {'title': new_title, 'content': new_content}
    save_data_after_updation(BLOGS_FILE, blogs)
    return jsonify({'message': 'Blog post modified successfully'})

@app.route('/delete_blog', methods=['POST'])
def delete_blog():
    data = request.json
    username = data.get('username')
    index = int(data.get('index'))  # Convert to integer
    blogs = load_datafromfile(BLOGS_FILE)
    if username not in blogs or index >= len(blogs[username]):
        return jsonify({'message': 'Invalid blog index or username'}), 400

    # Delete the blog
    blogs[username].pop(index)
    save_data_after_updation(BLOGS_FILE, blogs)
    return jsonify({'message': 'Blog post deleted successfully'})

@app.route('/get_blogs', methods=['GET'])
def get_blogs():
    username = request.args.get('username')
    blogs = load_datafromfile(BLOGS_FILE)
    if username not in blogs:
        return jsonify({'message': 'User not found.'}), 404
    return jsonify({'blogs': blogs[username]})

if __name__ == "__main__":
    app.run(debug=True)

