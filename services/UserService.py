import hashlib
import logging
from services.DbService import DbService
from services.MailService import MailService

class UserService:
    def __init__(self):
        self.db = DbService()
        self.mail_service = MailService()
        self.class_name = __class__.__name__

    def generate_hashed_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def check_user_id(self, user_id):
        try:
            query = "SELECT UserId, FirstName, LastName, Email FROM [dbo].[User] WHERE UserId = ? and IsActive = 1"
            row = self.db.fetch_one(query, (user_id,))
            return True if row else False
        except Exception as e:
            error_message = (f"An error occurred while checking the user ID: {user_id}".format(str(e)))
            logging.error(error_message)
            return False

    def insert_user_info(self, full_name, email, phone_number, password):
        try:
            hashed_password = self.generate_hashed_password(password)
            self.mail_service.send_email(full_name, password, email, "hi saurabh")
            query = """INSERT INTO [User] (Name, Email, Password, PhoneNumber) VALUES (?, ?, ?, ?)"""

            success, message = self.db.insert(query, (full_name, email, hashed_password, phone_number))
            if success:
                return True, "Data inserted successfully"
            else:
                return False, message
        except Exception as e:
            error_message = "An error occurred while inserting user info: {}".format(str(e))
            logging.error(error_message)
            return False, error_message

    def udpate_user_info(self, user_id, full_name, email, phone_number, city, state):
        try:
            query = """ UPDATE [User] 
                        SET 
                            FirstName = COALESCE(?, FirstName),
                            Email = COALESCE(?, Email),
                            Phone = COALESCE(?, Phone),
                            City = COALESCE(?, City),
                            State = COALESCE(?, State),
                            ModifyDate = GETDATE() 
                        WHERE UserId = ?"""
            success, message = self.db.execute(query, (full_name, email, phone_number, city, state, user_id))
            if success:
                return True, "Data updated successfully"
            else:
                return False, message
        except Exception as e:
            error_message = "An error occurred while updating user info: {}".format(str(e))
            logging.error(error_message)
            return False, error_message

    def get_all_user_data(self):
        try:
            query = "Select * from [User] where IsActive = 1"
            rows = self.db.fetch_all(query)
            data = []
            for row in rows:
                data.append(
                    {
                        "UserId": row.UserId,
                        "FirstName": row.FirstName,
                        "LastName": row.LastName,
                        "Email": row.Email,
                        "Phone": row.Phone,
                        "City": row.City,
                        "State": row.State,
                        "Password": row.Password,
                        "IsActive": row.IsActive,
                        "CreatedDate": row.CreatedDate,
                        "ModifyDate": row.ModifyDate,
                    }
                )

            return True, data
        except Exception as e:
            return False, str(e)

    def user_login(self, email, password):
        try:
            query = "SELECT FirstName, Email, Password, Phone FROM [User] WHERE Email = ? AND IsActive = 1 order by UserId desc"
            rows = self.db.fetch_all(query, (email,))
            if rows:
                for user_data in rows:
                    stored_password = user_data[2]
                    if stored_password == password:
                        return True, user_data
                return False, "Incorrect password"
            else:
                return False, "User not found"
        except Exception as e:
            error_message = "An error occurred while user login time: {}".format( str(e))
            logging.error(error_message)
            return False, error_message

    def reset_password(self, user_id, old_password, new_password):
        try:
            query = "UPDATE [dbo].[User] SET Password = ? WHERE UserId = ? AND Password = ? AND IsActive = 1"
            row = self.db.execute(query, (new_password, user_id, old_password))
            return row.rowcount > 0
        except Exception as e:
            error_message = "An error occurred while updating the user's password: {}".format(str(e))
            logging.error(error_message)
            return False
