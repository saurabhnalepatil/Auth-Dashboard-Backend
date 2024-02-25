from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.UserService import UserService
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/api/user", methods=["POST"])
def upsert_user():
    try:
        data = request.json
        user_id = data.get("userId")
        full_name = data.get("fullName")
        email = data.get("email")
        phone_number = data.get("phoneNumber")
        city = data.get("city")
        state = data.get("state")
        user_service = UserService()

        if user_service.check_user_id(user_id):
            success, message = user_service.udpate_user_info(user_id, full_name, email, phone_number, city, state)
        else:
            success, message = user_service.insert_user_info(full_name, email, phone_number, city, state)
            

        status_code = 201 if success else 500
        return jsonify({"message": message}) if success else jsonify({"error": message}), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/user", methods=["GET"])
def get_all_user():
    try:
        user_service = UserService()
        success, data = user_service.get_all_user_data()
        if success:
            return jsonify(data), 200
        else:
            return jsonify({"error": data}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user_service = UserService()
        if user_service.user_login(username, password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
