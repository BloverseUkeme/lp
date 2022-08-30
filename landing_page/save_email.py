from decouple import config as env_config
from flask import redirect, url_for, flash
from datetime import datetime
from uuid import uuid4

from mongodb.mongo_util import (
    save_to_mongo_db, get_record_details, connect_to_mongo_db, update_record)

MONGO_URL = env_config("MONGO_URL")



def register_twitter_handle_to_db(handle, username, profile_image, profile_bio, verified):

    collection = connect_to_mongo_db("landing_page_db", "twitter_handles", MONGO_URL)


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
                "username": username,
                "profile_image": profile_image,
                "profile_bio": profile_bio,
                "verified": verified
            }

        save_to_mongo_db(data, collection)

        flash('Twitter Authentication successful', "info")
        return redirect(url_for("landing_page.home"))


    else:
        flash(f'Twitter Account {handle},  Already Registered', "info")
        return redirect(url_for("landing_page.home"))

