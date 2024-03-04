from flask import Flask, request, jsonify
from dotenv import load_dotenv; load_dotenv()
from services.UserService import UserService
from flask_cors import CORS

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
        password = data.get("password")
        user_service = UserService()

        if user_service.check_user_id(user_id):
            success, message = user_service.udpate_user_info(user_id, full_name, email, phone_number, password)
        else:
            success, message = user_service.insert_user_info(full_name, email, phone_number, password)

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


@app.route("/api/forgot_password", methods=["POST"])
def forgot_password():
    try:
        data = request.get_json()
        user_id = data.get("userId")
        old_password = data.get('oldPassword')
        new_password = data.get("nePassword")

        if not user_id or not new_password:
            return jsonify({"error": "User ID and new password are required"}), 400

        user_service = UserService()
        success = user_service.reset_password(user_id, old_password, new_password)

        if success:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"error": "Failed to reset password"}), 401
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/api/contacts", methods=["POST"])
def upsert_user():
    try:
        data = request.json
        first_name = data.get("FirstName")
        last_name = data.get("LastName")
        phone_number = data.get("PhoneNumber")
        alt_phone_number = data.get("AltPhoneNumber")
        email = data.get("Email")
        birthday_date = data.get("BirthdayDate")
        address = data.get("Address")
        state = data.get("State")
        country = data.get("Country")
        user_service = UserService()

        if user_service.check_contact_existence(email):
            success, message = user_service.update_contact(email, first_name, last_name, phone_number, alt_phone_number, birthday_date, address, state, country)
        else:
            success, message = user_service.insert_contact(first_name, last_name, phone_number, alt_phone_number, email, birthday_date, address, state, country)

        status_code = 201 if success else 500
        return jsonify({"message": message}) if success else jsonify({"error": message}), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
