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
from flask import redirect, url_for, flash

from mongodb.mongo_util import save_to_mongo_db, get_record_details, connect_to_mongo_db

MONGO_URL = env_config("MONGO_URL")

def save_email_to_db(email):
    
    collection = connect_to_mongo_db("landing_page_db", "email_addresses", MONGO_URL)

    search_query = {"email": email}

    result = get_record_details(search_query, collection)
    print(result)

    if result is  None:
        save_to_mongo_db(search_query, collection)

    flash('Twitter Authentication successful', "info")
    return redirect(url_for("landing_page.home"))




def save_twitter_handle_to_db(handle, twitter_email=""):
    collection = connect_to_mongo_db("landing_page_db", "handles", MONGO_URL)

    if twitter_email:

        search_query = {"handle": handle}

        result = get_record_details(search_query, collection)
        print(result)

        if result is  None:
            data = {
                "handle": handle,
                "email": twitter_email
            }
            save_to_mongo_db(data, collection)
        flash('Twitter Authentication successful', "info")
        return redirect(url_for("landing_page.home"))
    
    else:
        flash("Sorry! We couldn't get Email address attached to this Account. Kindly Fill in your email", "info")
        return redirect(url_for("landing_page.email"))

