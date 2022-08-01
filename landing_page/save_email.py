# from decouple import config as env_config
# from mongodb.mongo_util import save_to_mongo_db, get_record_details, connect_to_mongo_db

# MONGO_URL = env_config("MONGO_URL")

# def save_email_to_db(email):
    
#     collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

#     search_query = {"email": email}

#     result = get_record_details(search_query, collection)


#     if result is  None:
#         save_to_mongo_db(search_query, collection)

#     return email


# def save_twitter_handle_to_db(handle):
#     collection = connect_to_mongo_db("landing_page_db", "handles", MONGO_URL)

#     search_query = {"handle": handle}

#     result = get_record_details(search_query, collection)

#     if result is  None:
#         save_to_mongo_db(search_query, collection)

#     return handle



from decouple import config as env_config
from flask import redirect, url_for, flash, render_template, Response
from datetime import datetime
from uuid import uuid4
import random
import string
from flask_mail import Message, Mail
import re

from mongodb.mongo_util import (
    save_to_mongo_db, get_record_details, connect_to_mongo_db, update_record)

MONGO_URL = env_config("MONGO_URL")



def create_access_key():
    string_upper = string.ascii_uppercase

    str_section = [random.choice(string_upper) for a in range(2)]

    int_section = [str(random.randint(10,99))]

    str_section_2 = [random.choice(string_upper) for a in range(2)]

    code = "".join(str_section + int_section + str_section_2)

    return code


def validate_email(email):
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if ( re.fullmatch(email_pattern, email) ):
        return True
    else:
        return False


def send_mail(email, template="",  access_code=""):

    mail = Mail()
    msg = Message(subject="Hello. Welcome",
                    sender=("Bloverse no-reply", "no-reply@gmail.com"),
                    recipients=[email])

        
    msg.html = render_template(template_name_or_list=template, email=email, access_code=access_code)
    mail.send(msg)




# def save_email_to_db(email):
    
#     collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

#     search_query = {"email": email}

#     result = get_record_details(search_query, collection)
#     print(result)

#     if result is  None:
#         save_to_mongo_db(search_query, collection)
#         flash('Twitter Authentication successful', "info")

#     flash('Twitter Account Already Registered', "info")
#     return redirect(url_for("landing_page.home"))




# def save_twitter_handle_to_db(handle, twitter_email=""):
#     collection = connect_to_mongo_db("landing_page_db", "handles", MONGO_URL)

#     if twitter_email:

#         search_query = {"handle": handle}

#         result = get_record_details(search_query, collection)
#         print(result)

#         if result is  None:
#             data = {
#                 "handle": handle,
#                 "email": twitter_email
#             }
#             save_to_mongo_db(data, collection)
#             flash('Twitter Authentication successful', "info")

#         flash('Twitter Account Already Registered', "info")
#         return redirect(url_for("landing_page.home"))
    
#     else:
#         flash("Sorry! We couldn't get Email address attached to this Account. Kindly Fill in your email", "info")
#         return redirect(url_for("landing_page.email"))




def register_twitter_handle_to_db(handle, email=''):
    collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

    if email:
        is_valid_email = validate_email(email)

        if is_valid_email:        

            search_query = {"handle": handle}

            result = get_record_details(search_query, collection)

            if result is  None:

                access_code = create_access_key()
                date_registered = datetime.now()
                date_registered_str = str(date_registered)

                data = {
                        "user_id": str(uuid4()),
                        "handle": handle,
                        "email": email,
                        "status": "REGISTERED", 
                        "access_code": access_code,
                        "date_registered": date_registered_str,
                        "username": "",
                        "profile_image": "",
                        "profile_bio": ""

                    }

                send_mail(email, template='email.html', access_code=access_code)
                save_to_mongo_db(data, collection)

                flash('Twitter Authentication successful', "info")
                return redirect(url_for("landing_page.home"))


            else:
                flash(f'Twitter Account {handle},  Already Registered', "info")
                return redirect(url_for("landing_page.home"))

        else: ## this probably should never get to run
            return {
                    'status': False,
                    'message': f"Invalid Email format"
                    }, 403


    else: ## if twitter mail is absent:
        search_query = {"handle": handle}

        result = get_record_details(search_query, collection)

        if result is  None:
            date_registered = datetime.now()
            date_registered_str = str(date_registered)

            data = {
                    "user_id": str(uuid4()),
                    "handle": handle,
                    "status": "REGISTERED", 
                    "date_registered": date_registered_str,
                    "username": "",
                    "profile_image": "",
                    "profile_bio": ""

                }
            save_to_mongo_db(data, collection)
            flash("Sorry! We couldn't get an Email address attached to your Twitter Account. Kindly Fill in your email", "info")
            return redirect(url_for("landing_page.email", handle=handle))
            # return Response(response=render_template('landing_email.html', handle=handle))

        
        flash(f'Twitter Account {handle},  Already Registered', "info")
        return redirect(url_for("landing_page.home"))






def register_email_to_db(email, handle):

    """  
        - This first validates the Incoming Email. Result is True/False
        - Then Checks if the EMail is in the db/collection.
        - Sends the templated mail, if not  
    """

    is_valid_email = validate_email(email)

    if is_valid_email:

        collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

        search_query = {"handle": handle}
        search_query_2 = {"email": email}

        search_result = get_record_details(search_query, collection)
        search_result_2 = get_record_details(search_query_2, collection)
        print(search_result)

        if search_result and search_result.get("email"):
            flash(f'Already Registered', "info")
            return redirect(url_for("landing_page.home"))

        elif search_result and search_result.get("email") !=  email:
            access_code = create_access_key()

            search_result['email'] = email
            search_result['access_code'] = access_code

            new_values = {"$set" : search_result}
            update_record(collection, search_query, new_values)

            send_mail(email, template='email.html' , access_code=access_code)

            flash('Twitter Authentication successful', "info")
            return redirect(url_for("landing_page.home"))

        elif search_result and search_result.get("email") ==  email:
            flash(f'{email},  Already Registered', "info")
            return redirect(url_for("landing_page.home"))

        elif search_result and search_result.get("email"):
            flash(f'Already Registered', "info")
            return redirect(url_for("landing_page.home"))



        elif search_result_2:
            flash(f'{email},  Already Registered', "info")
            return redirect(url_for("landing_page.home"))
        # else:
        #     flash(f'{email},  Already Registered', "info")
        #     return redirect(url_for("landing_page.home"))

    else:
        flash(f'Wrong email format for {email}', "error")
        return redirect(url_for("landing_page.email"))




# def update_register_twitter_handle_to_db(handle, email):
#     is_valid_email = validate_email(email)

#     if is_valid_email:

#         collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

#         search_query = {"handle": handle}
#         search_query_2 = {"email": email}
    
#         search_result = get_record_details(search_query, collection)
#         search_result_2 = get_record_details(search_query_2, collection)

#         if search_result:
#             access_code = create_access_key()

#             search_result['email'] = email
#             search_result['access_code'] = access_code

#             new_values = {"$set" : search_result}
#             update_record(collection, search_query, new_values)

#             send_mail(email, template='index.html' , access_code=access_code)
        
#             return {
#                     'status': True,
#                     'message': f"{email} registered"
#                 }, 200

#         elif search_result is None:
#             result = register_twitter_handle_to_db(handle, twitter_mail=email)
#             return result


#         elif search_result_2:
#             return {
#                     'status': False,
#                     'message': f"The Email: {email} already registered"
#                 }, 401

#     else:
#         return {
#                     'status': False,
#                     'message': f"Invalid Email format"
#                 }, 403
