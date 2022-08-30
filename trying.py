# oauth_store = {}


# def generate_request_token():

#     import oauth2 as oauth
#     import urllib.request
#     from flask import render_template


#     request_token_url = 'https://api.twitter.com/oauth/request_token'

#     app_callback_url =  "http://localhost:5000/callback"
#     # app_callback_url = "http://65.21.61.196:5002/callback"

#     consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

#     client = oauth.Client(consumer)
#     resp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({
#                                     "oauth_callback": app_callback_url}))

#     if resp['status'] != '200':
#         error_message = 'Invalid response, status {status}, {message}'.format(
#             status=resp['status'], message=content.decode('utf-8'))
#         return render_template('error.html', error_message=error_message)

#     request_token = dict(urllib.parse.parse_qsl(content))

#     print(request_token)

#     oauth_token = request_token[b'oauth_token'].decode('utf-8')
#     oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

#     oauth_store[oauth_token] = oauth_token_secret

#     return oauth_token, oauth_token_secret
# generate_request_token()




# def get_mail_from_oauth_token(oauth_token, oauth_token_secret, oauth_verifier):
#     import oauth2 as oauth
#     import urllib.request

#     access_token_url = 'https://api.twitter.com/oauth/access_token'

#     # oauth_token =  "ZP5KKAAAAAABWfiwAAABgdk0zdY"     #request.args.get('oauth_token')
#     # oauth_verifier = ...   #request.args.get('oauth_verifier')
#     # oauth_denied =   ...   #request.args.get('denied')
    
#     print(oauth_token)
#     # oauth_token_secret = oauth_store[oauth_token]
#     print(oauth_token_secret)

#     consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
#     token = oauth.Token(oauth_token, oauth_token_secret)
#     token.set_verifier(oauth_verifier)
#     client = oauth.Client(consumer, token)

#     resp, content = client.request(access_token_url, "POST")
#     access_token = dict(urllib.parse.parse_qsl(content))

#     real_oauth_token = access_token[b'oauth_token'].decode('utf-8')
#     real_oauth_token_secret = access_token[b'oauth_token_secret'].decode(
#         'utf-8')

#     # Call api.twitter.com/1.1/users/show.json?user_id={user_id}
#     real_token = oauth.Token(real_oauth_token, real_oauth_token_secret)
#     real_client = oauth.Client(consumer, real_token)

#     verify_user_url = "https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true"

#     real_resp, real_content = real_client.request(verify_user_url , "GET")

#     import json
#     twitter_json_data = json.loads(real_content.decode('utf-8'))
#     twitter_email = twitter_json_data.get("email")
#     handle = twitter_json_data.get("screen_name")

#     print(twitter_email)


# # https://api.twitter.com/oauth/authorize?oauth_token=NlWjrwAAAAABWfiwAAABghvFhN8
# # get_mail_from_oauth_token(oauth_token, oauth_token_secret, oauth_verifier)


# import json

# data = '{"id":"09", "name": "Nitin", "department":"Finance"}'
# json_store = json.loads(data)

# print(json_store)

# data = json.load(f)



# https://express.adobe.com/sp/design/post/urn:aaid:sc:EU:6b3aface-541b-4828-b266-213ae0f7db01?workflow=quicktask





server {
    listen              443 ssl;
    server_name         bloverse.com;
    ssl_certificate     /etc/ssl/bloverse.com.pem;
    ssl_certificate_key /etc/ssl/bloverse.com.key;
    location / {
        proxy_pass http://website:5000;
    }
}



location / {
root /home/www/public_html/your_very_own_domain.com/public/;
index index.html;



// server {
//     listen   80;
//     // server_name  bloverse.com;
//     server_name     localhost;
//     rewrite ^/(.*) https://bloverse.com/$1 permanent;
//     location / {
//         proxy_pass http://website:5000;
//     }
// }
