from flask import request, jsonify, current_app
import functools
import jwt

def require_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. ALWAYS ALLOW 'OPTIONS' REQUESTS FOR CORS PREFLIGHT
        if request.method == "OPTIONS":
            return jsonify({"message": "CORS preflight allowed"}), 200

        # 2. PROCEED WITH NORMAL SECURITY CHECKS
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized: Missing token"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=["HS256"]
            )
            
            if decoded.get("role") != "Admin":
                return jsonify({"error": "Forbidden: Admin access required"}), 403
                
        except Exception as e:
            return jsonify({"error": "Invalid or expired token"}), 401

        return func(*args, **kwargs)

    return wrapper