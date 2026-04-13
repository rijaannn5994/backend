from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.inventory_routes import inventory_bp
from routes.supplier_routes import supplier_bp
import jwt
import datetime

app = Flask(__name__)
CORS(app)

app.register_blueprint(inventory_bp, url_prefix="/api")
app.register_blueprint(supplier_bp, url_prefix="/api")

# Secret key used to encrypt the tokens (Keep this safe!)
app.config['SECRET_KEY'] = 'my_super_secret_assignment_key'

# NEW LOGIN ROUTE
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    code = data.get("code")
    
    role = None
    # Check the access code provided by the frontend
    if code == "5555":
        role = "Admin"
    elif code == "0000":
        role = "Staff"
        
    if role:
        # Generate a secure token that lasts for 2 hours
        token = jwt.encode({
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({"token": token, "role": role}), 200

    return jsonify({"error": "Invalid Access Code"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5001)