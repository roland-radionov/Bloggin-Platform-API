import json
from datetime import datetime
from database import init_db, get_db
from flask import Flask, request, jsonify

app = Flask(__name__)

def validate_post_data(data):
    """Validate POST and PUT data"""

    if not data['title']:
        return "Title is required"
    if not data['content']:
        return "Content is required"
    
    return None

@app.route('/posts', methods=['GET'])
def get_all_posts():
    search_term = request.args.get('term')
    query = "SELECT * FROM posts"
    params = ()

    if search_term:
        pattern = f"%{search_term}%"
        query = """SELECT * FROM posts
                    WHERE title LIKE ?
                    OR content LIKE ?
                    OR category LIKE ?
                    ORDER BY id
                """
        params = (pattern, pattern, pattern)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        posts = []
        for row in cursor.fetchall():
            post = dict(row)

            if post.get('tags'):
                post['tags'] = json.loads(post['tags'])
            else:
                post['tags'] = []
            
            posts.append(post)
     
    if posts:
        return jsonify(posts), 200

    return jsonify([]), 200

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?",(id,))
        post_data = cursor.fetchone()
        
    if post_data:
        post_data = dict(post_data)

        if post_data['tags']:
            post_data['tags'] = json.loads(post_data['tags'])
        else:
            post_data['tags'] = []

        return jsonify(post_data), 200

    return jsonify({"message": f"Not found data for id {id}"}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    post_data = request.get_json()

    error = validate_post_data(post_data)
    if error:
        return jsonify({"message": error}), 400

    title = post_data.get('title')
    content = post_data.get('content')
    category = post_data.get('category')
    tags = json.dumps(post_data.get('tags'))

    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO posts (title, content, category, tags) VALUES (?,?,?,?)",
            (title, content, category, tags)
        )
        id = cursor.lastrowid
    
    return jsonify({"message": f"Succesfully created post with id {id}"}), 201

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE id = ?", (id,))

        if not cursor.fetchone():
            return jsonify({"message": f"Post {id} not found"}), 404
        
        cursor.execute("DELETE FROM posts WHERE id = ?", (id,))
    
    return "", 204

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    update_post_data = request.get_json()

    error = validate_post_data(update_post_data)
    if error:
        return jsonify({"message": error}), 400

    title = update_post_data.get('title')
    content = update_post_data.get('content')
    category = update_post_data.get('category')
    tags = json.dumps(update_post_data.get('tags'))
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE id = ?", (id,))

        if not cursor.fetchone():
            return jsonify({"message": f"Post {id} not found"}), 404
        
        cursor.execute(
            "UPDATE posts SET title = ?, content = ?, category = ?, tags = ?, updated_at = ? WHERE id = ?",
            (title, content, category, tags, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id)
        )
        conn.commit()

    return jsonify({"message": f"Succesfully changed post with id {id}"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)