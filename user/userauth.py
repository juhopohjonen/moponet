# Module for implementing OAuth2.0 for Moponet (Discord)

import uuid
import requests
from flask import Blueprint, Flask, redirect, render_template, \
     request, request_tearing_down, abort, session, url_for

from app import app, configuration
import app as appfile
from user.user import user
import models

import datahandling

# add scopes
SCOPES = [
    'identify',
    'email'
]

# create DiscordUser object+return
def createDiscordUser(discord_uid, related_username):
    DiscordUser = models.DiscordUser
    current = DiscordUser(
        discord_uid=discord_uid,
        related_username=related_username
    )

    return current

class discordApiCall:

    def __init__(self, scopes, discordConfigObj):
        self.scopes = scopes
        self.discordConfigObj = discordConfigObj

        
        self.clientId = discordConfigObj['CLIENT_ID']
        self.clientSecret = discordConfigObj['CLIENT_SECRET']
        self.apiEndpoint = discordConfigObj['API_ENDPOINT']
        
        self.redirectUrl = discordConfigObj['redirect_url']

    def getUrl(self):
        discordConfigObj = self.discordConfigObj

        redirectUrl = self.redirectUrl

        #  convert scopes to str
        #  which discord accepts 
    
        scopeStr = '%20'.join(SCOPES)

        # Generate URL for OAuth
        self.urlList = [
            'https://discord.com/api/oauth2/authorize?',
            'response_type=code&' +
            'client_id=' + self.clientId + "&" +
            'scope=' + scopeStr + '&' +
            'redirect_uri=' + redirectUrl
        ]

        return ''.join(self.urlList)
    

    # method for exchanging code.
    
    def exchangeCode(self, code):    
        data = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirectUrl
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        r = requests.post('%s/oauth2/token' % self.apiEndpoint, data=data, headers=headers)
        r.raise_for_status()
        return r.json()


    # function for retrieving user data
    # from discord's oauth2.0 api
    def retrieve_user(self, access_token):
        endpoint = self.discordConfigObj['USER_INFO_ENDPOINT']
        
       
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        

        r = requests.get(endpoint, headers=headers)
        r.raise_for_status()
        return r.json()

    def __str__(self):
        return f"<discordApiCall Object>"

    
    
@user.route('/discord/auth')
def discord_login():

    # if has 'code' argument in url
    # then the user is redirected
    # from discord (user has authenticated)

    code = request.args.get('code')
    
    caller = discordApiCall(
        scopes=SCOPES,
        discordConfigObj=configuration['discord_oauth']
    )

    if not code:
        url = caller.getUrl()
        return redirect(url)


    # retrieve access token and
    # get the user


    try:
        firstCallResult = caller.exchangeCode(code)
        access_token = firstCallResult['access_token']
    except:
        return f"Virhe palvelinpyynnössä. Onkohan kirjautumiskoodisi virheellinen? \
            Yritä uudelleen."
    user = caller.retrieve_user(access_token)

    # try to fetch user if exists already
    # if not => create new DiscordUser and User object.

    DiscordUser = models.DiscordUser
    User = models.User

    discord_username = user['username']
    discord_user_id = user['id']
    discord_email = user['email']

    
    discordUserInDb = DiscordUser.query.filter_by(
        discord_uid=discord_user_id
    ).first()

    existingUsername = User.query.filter_by(
        username=discord_username
    ).first()

    # make sure too that there is not user in
    # the database with a same username.

    if discordUserInDb == None and existingUsername == None:
        current_user = User(
            username=discord_username,
            email=discord_email,
            isDiscordUser=1
        )

        discordUser = createDiscordUser(
            discord_user_id,
            current_user.username
        )

        
        # Add objects into db + commit changes
        appfile.db.session.add(current_user)
        appfile.db.session.add(discordUser)
        appfile.db.session.commit()


    elif not discordUserInDb:
        return f"Valitettavasti Discordissa käyttämäsi käyttäjänimi on jo otettu käyttöön."
    
    else:
        # fetch

        current_DiscordUser = DiscordUser.query.filter_by(
            discord_uid = discord_user_id
        ).first()

        current_user = User.query.filter_by(
            username=current_DiscordUser.related_username
        ).first()

    # log user in (add session obj) + redirect to index
    SessionObject = datahandling.sessionObject

    current_session = SessionObject(
        user_id=User.query.filter_by(username=current_user.username).first().id
    )

    print(f'dict: {current_session.generate_dict()}')
    session['object'] = current_session.generate_dict()
    return redirect(url_for('home'))