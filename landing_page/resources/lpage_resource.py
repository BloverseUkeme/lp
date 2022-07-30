from flask import render_template, request, Response, redirect, url_for
from flask_restful import  Resource
from decouple import config as env_config
from landing_page.extensions import oauth





CONSUMER_KEY = env_config("CONSUMER_KEY") 
CONSUMER_SECRET = env_config("CONSUMER_SECRET") 

class Home(Resource):
    def get(self):

        return Response(response=render_template('landing.html'))


class Email(Resource):
    def get(self):

        return Response(response=render_template('email.html'))


    def post(self):
        from landing_page.save_email import save_email_to_db
        # from landing_page.tasks.lpage import celery_start_save_email
        json_data = request.form.get("email")
        print(json_data)

        # celery_start_save_email.apply_async((json_data,), queue="lpage")

        result = save_email_to_db(json_data)
        
        return result

class Twitter(Resource):

    def get(self):
        TWITTER_CLIENT_ID = CONSUMER_KEY
        TWITTER_CLIENT_SECRET = CONSUMER_SECRET

        print("here")

        oauth.register(
                name='twitter',
                client_id=TWITTER_CLIENT_ID,
                client_secret=TWITTER_CLIENT_SECRET,
                request_token_url='https://api.twitter.com/oauth/request_token',
                request_token_params=None,
                access_token_url='https://api.twitter.com/oauth/access_token',
                access_token_params=None,
                authorize_url='https://api.twitter.com/oauth/authenticate',
                authorize_params=None,
                api_base_url='https://api.twitter.com/1.1/',
                client_kwargs=None,
            )

        # redirect_uri = url_for('twitter_auth', _external=True)
        redirect_uri = "http://localhost:5002/twitter/auth/"
        
        return oauth.twitter.authorize_redirect(redirect_uri)


class Twitter_Oauth(Resource):
    def get(self):
        from landing_page.save_email import save_twitter_handle_to_db

        token = oauth.twitter.authorize_access_token()
        resp = oauth.twitter.get('account/verify_credentials.json?include_email=true')
        profile = resp.json()
    

        handle = profile.get("screen_name")
        email = profile.get("email")
        result = save_twitter_handle_to_db(handle, email)

        return result

