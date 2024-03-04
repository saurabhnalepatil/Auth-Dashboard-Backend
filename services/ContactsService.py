import logging
from services.DbService import DbService

class UserService:
    def __init__(self):
        self.db = DbService()
        self.class_name = __class__.__name__

    def check_contact_id(self, contact_id):
        try:
            query = "SELECT UserId, FirstName, LastName, Email FROM [dbo].[User] WHERE Id = ? and IsActive = 1"
            row = self.db.fetch_one(query, (contact_id,))
            return True if row else False
        except Exception as e:
            error_message = (f"An error occurred while checking the user ID: {contact_id}".format(str(e)))
            logging.error(error_message)
            return False

    def insert_contact_info(self, first_name, last_name, phone_number, alt_phone_number, email, birthday_date, address, state, country):
        try:
            query = """INSERT INTO UserInfo (FirstName, LastName, PhoneNumber, AltPhoneNumber, Email, BirthdayDate, Address, State, Country) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            success, message = self.db.insert(query, (first_name, last_name, phone_number, alt_phone_number, email, birthday_date, address, state, country))
            if success:
                return True, "Data inserted successfully"
            else:
                return False, message
        except Exception as e:
            error_message = "An error occurred while inserting user info: {}".format(str(e))
            logging.error(error_message)
            return False, error_message

    def update_user_info(self, user_id, first_name, last_name, phone_number, alt_phone_number, email, birthday_date, address, state, country):
        try:
            query = """UPDATE UserInfo 
                    SET FirstName = COALESCE(?, FirstName),
                        LastName = COALESCE(?, LastName),
                        PhoneNumber = COALESCE(?, PhoneNumber),
                        AltPhoneNumber = COALESCE(?, AltPhoneNumber),
                        Email = COALESCE(?, Email),
                        BirthdayDate = COALESCE(?, BirthdayDate),
                        Address = COALESCE(?, Address),
                        State = COALESCE(?, State),
                        Country = COALESCE(?, Country)
                    WHERE UserID = ?"""

            success, message = self.db.execute(query, (first_name, last_name, phone_number, alt_phone_number, email, birthday_date, address, state, country, user_id))
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
            query = '''SELECT [Id]
                        ,[FirstName]
                        ,[LastName]
                        ,[Email]
                        ,[PhoneNumber]
                        ,[AltPhoneNumber]
                        ,[City]
                        ,[State]
                        ,[Password]
                        ,[CreateDate]
                        ,[ModifyDate]
                    FROM [dbo].[Contacts] WHERE IsActive = 1'''
            rows = self.db.fetch_all(query)
            data = []
            for row in rows:
                data.append(
                    {
                        "UserId": row.Id,
                        "FirstName": row.FirstName,
                        "LastName": row.LastName,
                        "Email": row.Email,
                        "Phone": row.PhoneNumber,
                        "altPhone": row.AltPhoneNumber,
                        "City": row.City,
                        "State": row.State,
                        "Password": row.Password,
                        "CreatedDate": row.CreateDate,
                        "ModifyDate": row.ModifyDate,
                    }
                )
            
            logging.info("Successfully retrieved all user data.")
            return True, data
        except Exception as e:
            error_message = "An error occurred while inserting user info: {}".format(str(e))
            logging.error(error_message)
            return False, str(e)

