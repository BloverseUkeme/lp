from flask import render_template, request
from flask_restful import  Resource

from flask import request, Response, redirect, url_for


oauth_store = {}

CONSUMER_KEY="ek5jIPA1TTU94Wsrd04LxSdc9"
CONSUMER_SECRET="AbYLmDs5tqpoCL274o2KWvACM6fJI0WRScTaVlooRKosNxcROR"

def generate_request_token():

    import oauth2 as oauth
    import urllib.request
    from flask import render_template


    request_token_url = 'https://api.twitter.com/oauth/request_token'

    app_callback_url =  "http://localhost:5002/callback"
    # app_callback_url = "http://65.21.61.196:5002/callback"

    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    client = oauth.Client(consumer)
    resp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({
                                    "oauth_callback": app_callback_url}))

    if resp['status'] != '200':
        error_message = 'Invalid response, status {status}, {message}'.format(
            status=resp['status'], message=content.decode('utf-8'))
        return render_template('error.html', error_message=error_message)

    request_token = dict(urllib.parse.parse_qsl(content))

    oauth_token = request_token[b'oauth_token'].decode('utf-8')
    oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

    oauth_store[oauth_token] = oauth_token_secret

    # data = {oauth_token: oauth_token_secret}
    # import json
    # with open("oauth_token.json", "w") as oauth_token_file:
    #     json.dump(data, oauth_token_file)

    return oauth_token, oauth_token_secret


def get_mail_from_oauth_token(oauth_token, oauth_token_secret, oauth_verifier):
    import oauth2 as oauth
    import urllib.request

    access_token_url = 'https://api.twitter.com/oauth/access_token'


    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content))

    real_oauth_token = access_token[b'oauth_token'].decode('utf-8')
    real_oauth_token_secret = access_token[b'oauth_token_secret'].decode(
        'utf-8')

    # Call api.twitter.com/1.1/users/show.json?user_id={user_id}
    real_token = oauth.Token(real_oauth_token, real_oauth_token_secret)
    real_client = oauth.Client(consumer, real_token)

    verify_user_url = "https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true"

    real_resp, real_content = real_client.request(verify_user_url , "GET")

    import json
    twitter_json_data = json.loads(real_content.decode('utf-8'))

    twitter_email = twitter_json_data.get("email")
    handle = twitter_json_data.get("screen_name")

    return twitter_email, handle



class Home(Resource):
    def get(self):
        oauth_token, oauth_token_secret = generate_request_token()
        # print(oauth_token)
        return Response(response=render_template('index4.html', oauth_token=oauth_token))

    # def post(self):
    #     json_data = request.form.get("email")
    #     print(json_data)


    #     Response(response=render_template('index4.html'))
    #     return redirect(request.referrer)

class Email(Resource):
    def get(self):
        # oauth_token, oauth_token_secret = generate_request_token()
        # print(oauth_token)
        return Response(response=render_template('index3.html'))
        # return redirect(url_for("landing_page.email"))


    def post(self):
        # from landing_page.tasks.lpage import celery_start_save_email
        json_data = request.form.get("email")
        print(json_data)

        # save_email_to_db(json_data)
        # celery_start_save_email.apply_async((json_data,), queue="lpage")
        Response(response=render_template('index3.html'))

        return redirect(request.referrer)
        





class CallBack(Resource):
    def get(self):
        
        from save_email import save_twitter_handle_to_db

        oauth_verifier = request.args.get('oauth_verifier')
        oauth_token = request.args.get('oauth_token')

        oauth_token_secret = oauth_store[oauth_token]

        

        twitter_email, handle = get_mail_from_oauth_token(oauth_token, oauth_token_secret, oauth_verifier)

        # twitter_email = None
        result = save_twitter_handle_to_db(handle, twitter_email)

        return result #redirect(url_for("landing_page.home"))





# from flask_restful import Resource
# from flask import request, make_response, render_template

# class Registration(Resource):
#     def post(self):
#         print(request.form)
#         json_data = request.form.get("e_mail")
#         print("there")
#         print(json_data)

#         headers = {'Content-Type': 'text/html'}
#         return make_response(render_template("index.html"), headers)





print(oauth_store)