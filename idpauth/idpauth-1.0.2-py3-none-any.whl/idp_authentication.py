"""
Custom Authenticator to use generic OAuth2 with JupyterHub
"""

import json
import os
import base64
import urllib
import uuid

from urllib.parse import quote, urlparse
from tornado import web
from tornado.auth import OAuth2Mixin
from tornado.log import app_log
from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from jupyterhub.handlers import BaseHandler, LogoutHandler
from jupyterhub.auth import Authenticator, LocalAuthenticator
from jupyterhub.utils import url_path_join
from traitlets import TraitType, Unicode, Bool, List, Dict, default, Union

def guess_callback_uri(protocol, host, hub_server_url):
    return '{proto}://{host}{path}'.format(
        proto=protocol, host=host, path=url_path_join(hub_server_url, 'oauth_callback')
    )

STATE_COOKIE_NAME = 'oauthenticator-state'

def _serialize_state(state):
    """Serialize OAuth state to a base64 string after passing through JSON"""
    json_state = json.dumps(state)
    return base64.urlsafe_b64encode(json_state.encode('utf8')).decode('ascii')

def _deserialize_state(b64_state):
    """Deserialize OAuth state as serialized in _serialize_state"""
    if isinstance(b64_state, str):
        b64_state = b64_state.encode('ascii')
    try:
        json_state = base64.urlsafe_b64decode(b64_state).decode('utf8')
    except ValueError:
        app_log.error("Failed to b64-decode state: %r", b64_state)
        return {}
    try:
        return json.loads(json_state)
    except ValueError:
        app_log.error("Failed to json-decode state: %r", json_state)
        return {}

class OAuthLoginHandler(OAuth2Mixin, BaseHandler):
    """Base class for OAuth login handler
    Typically subclasses will need
    """

    # these URLs are part of the OAuth2Mixin API
    # get them from the Authenticator object
    @property
    def _OAUTH_AUTHORIZE_URL(self):
        return self.authenticator.authorize_url

    @property
    def _OAUTH_ACCESS_TOKEN_URL(self):
        return self.authenticator.token_url

    @property
    def _OAUTH_USERINFO_URL(self):
        return self.authenticator.userdata_url

    def set_state_cookie(self, state):
        self._set_cookie(STATE_COOKIE_NAME, state, expires_days=1, httponly=True)

    _state = None

    def get_state(self):
        next_url = original_next_url = self.get_argument('next', None)
        if next_url:
            # avoid browsers treating \ as /
            next_url = next_url.replace('\\', quote('\\'))
            # disallow hostname-having urls,
            # force absolute path redirect
            urlinfo = urlparse(next_url)
            next_url = urlinfo._replace(
                scheme='', netloc='', path='/' + urlinfo.path.lstrip('/')
            ).geturl()
            if next_url != original_next_url:
                self.log.warning(
                    "Ignoring next_url %r, using %r", original_next_url, next_url
                )
        if self._state is None:
            self._state = _serialize_state(
                {'state_id': uuid.uuid4().hex, 'next_url': next_url}
            )
        return self._state

    def get(self):
        redirect_uri = self.authenticator.get_callback_url(self)
        extra_params = self.authenticator.extra_authorize_params.copy()
        self.log.info('[IDPAuthenticator] OAuth redirect: %r', redirect_uri)
        state = self.get_state()
        self.set_state_cookie(state)
        extra_params['state'] = state
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.authenticator.client_id,
            scope=self.authenticator.scope,
            extra_params=extra_params,
            response_type='code',
        )

class OAuthCallbackHandler(BaseHandler):
    """Basic handler for OAuth callback. Calls authenticator to verify username."""

    _state_cookie = None

    def get_state_cookie(self):
        """Get OAuth state from cookies
        To be compared with the value in redirect URL
        """
        if self._state_cookie is None:
            self._state_cookie = (
                    self.get_secure_cookie(STATE_COOKIE_NAME) or b''
            ).decode('utf8', 'replace')
            self.clear_cookie(STATE_COOKIE_NAME)
        return self._state_cookie

    def get_state_url(self):
        """Get OAuth state from URL parameters
        to be compared with the value in cookies
        """
        return self.get_argument("state")

    def check_state(self):
        """Verify OAuth state
        compare value in cookie with redirect url param
        """
        cookie_state = self.get_state_cookie()
        url_state = self.get_state_url()
        if not cookie_state:
            raise web.HTTPError(400, "OAuth state missing from cookies")
        if not url_state:
            raise web.HTTPError(400, "OAuth state missing from URL")
        if cookie_state != url_state:
            self.log.warning("OAuth state mismatch: %s != %s", cookie_state, url_state)
            raise web.HTTPError(400, "OAuth state mismatch")

    def check_error(self):
        """Check the OAuth code"""
        error = self.get_argument("error", False)
        if error:
            message = self.get_argument("error_description", error)
            raise web.HTTPError(400, "OAuth error: %s" % message)

    def check_code(self):
        """Check the OAuth code"""
        if not self.get_argument("code", False):
            raise web.HTTPError(400, "OAuth callback made without a code")

    def check_arguments(self):
        """Validate the arguments of the redirect
        Default:
        - check for oauth-standard error, error_description arguments
        - check that there's a code
        - check that state matches
        """
        self.check_error()
        self.check_code()
        self.check_state()

    def append_query_parameters(self, url, exclude=None):
        """JupyterHub 1.2 appends query parameters by default in get_next_url
        This is not appropriate for oauth callback handlers, where params are oauth state, code, etc.
        Override the method used to append parameters to next_url to not preserve any parameters
        """
        return url

    def get_next_url(self, user=None):
        """Get the redirect target from the state field"""
        state = self.get_state_url()
        if state:
            next_url = _deserialize_state(state).get('next_url')
            if next_url:
                return next_url
        # JupyterHub 0.8 adds default .get_next_url for a fallback
        if hasattr(BaseHandler, 'get_next_url'):
            return super().get_next_url(user)
        return url_path_join(self.hub.server.base_url, 'home')

    async def _login_user_pre_08(self):
        """login_user simplifies the login+cookie+auth_state process in JupyterHub 0.8
        _login_user_07 is for backward-compatibility with JupyterHub 0.7
        """
        user_info = await self.authenticator.get_authenticated_user(self, None)
        if user_info is None:
            return
        if isinstance(user_info, dict):
            username = user_info['name']
        else:
            username = user_info
        user = self.user_from_username(username)
        self.set_login_cookie(user)
        return user

    if not hasattr(BaseHandler, 'login_user'):
        # JupyterHub 0.7 doesn't have .login_user
        login_user = _login_user_pre_08

    async def get(self):
        self.check_arguments()
        user = await self.login_user()
        if user is None:
            # todo: custom error page?
            raise web.HTTPError(403)
        self.redirect(self.get_next_url(user))

class OAuthLogoutHandler(LogoutHandler):
    async def get(self):
        self.log.info('[OAuthLogoutHandler] get: %r', self.authenticator.logout_redirect_url)
        await self.current_user.save_auth_state(None)
        self.clear_login_cookie()
        if self.authenticator.logout_redirect_url:
            self.redirect(self.authenticator.logout_redirect_url)
            return
        await super().get()

class OAuthenticator(Authenticator):
    """Base class for OAuthenticators
    Subclasses must override:
    login_service (string identifying the service provider)
    authenticate (method takes one arg - the request handler handling the oauth callback)
    """

    login_handler = OAuthLoginHandler
    callback_handler = OAuthCallbackHandler
    logout_handler = OAuthLogoutHandler

    authorize_url = Unicode(
        config=True, help="""The authenticate url for initiating oauth"""
    )
    @default("authorize_url")
    def _authorize_url_default(self):
        return os.environ.get("OAUTH2_AUTHORIZE_URL", "")

    token_url = Unicode(
        config=True,
        help="""The url retrieving an access token at the completion of oauth""",
    )
    @default("token_url")
    def _token_url_default(self):
        return os.environ.get("OAUTH2_TOKEN_URL", "")

    userdata_url = Unicode(
        config=True,
        help="""The url for retrieving user data with a completed access token""",
    )
    @default("userdata_url")
    def _userdata_url_default(self):
        return os.environ.get("OAUTH2_USERDATA_URL", "")

    scope = List(
        Unicode(),
        config=True,
        help="""The OAuth scopes to request.
        See the OAuth documentation of your OAuth provider for options.
        For GitHub in particular, you can see github_scopes.md in this repo.
        """,
    )

    extra_authorize_params = Dict(
        config=True,
        help="""Extra GET params to send along with the initial OAuth request
        to the OAuth provider.""",
    )

    login_service = 'override in subclass'
    oauth_callback_url = Unicode(
        os.getenv('OAUTH_CALLBACK_URL', ''),
        config=True,
        help="""Callback URL to use.
        Typically `https://{host}/hub/oauth_callback`""",
    )

    client_id_env = ''
    client_id = Unicode(config=True)

    def _client_id_default(self):
        if self.client_id_env:
            client_id = os.getenv(self.client_id_env, '')
            if client_id:
                return client_id
        return os.getenv('OAUTH_CLIENT_ID', '')

    client_secret_env = ''
    client_secret = Unicode(config=True)

    def _client_secret_default(self):
        if self.client_secret_env:
            client_secret = os.getenv(self.client_secret_env, '')
            if client_secret:
                return client_secret
        return os.getenv('OAUTH_CLIENT_SECRET', '')

    validate_server_cert_env = 'OAUTH_TLS_VERIFY'
    validate_server_cert = Bool(config=True)

    def _validate_server_cert_default(self):
        env_value = os.getenv(self.validate_server_cert_env, '')
        if env_value == '0':
            return False
        else:
            return True

    def login_url(self, base_url):
        return url_path_join(base_url, 'oauth_login')


    def get_callback_url(self, handler=None):
        """Get my OAuth redirect URL

        Either from config or guess based on the current request.
        """
        if self.oauth_callback_url:
            return self.oauth_callback_url
        elif handler:
            return guess_callback_uri(
                handler.request.protocol,
                handler.request.host,
                handler.hub.server.base_url,
            )
        else:
            raise ValueError(
                "Specify callback oauth_callback_url or give me a handler to guess with"
            )

    def get_handlers(self, app):
        return [
            (r'/oauth_login', self.login_handler),
            (r'/oauth_callback', self.callback_handler),
            (r'/logout', self.logout_handler)
        ]

    async def authenticate(self, handler, data=None):
        raise NotImplementedError()

    _deprecated_oauth_aliases = {}

    def _deprecated_oauth_trait(self, change):
        """observer for deprecated traits"""
        old_attr = change.name
        new_attr, version = self._deprecated_oauth_aliases.get(old_attr)
        new_value = getattr(self, new_attr)
        if new_value != change.new:
            # only warn if different
            # protects backward-compatible config from warnings
            # if they set the same value under both names
            self.log.warning(
                "{cls}.{old} is deprecated in {cls} {version}, use {cls}.{new} instead".format(
                    cls=self.__class__.__name__,
                    old=old_attr,
                    new=new_attr,
                    version=version,
                )
            )
            setattr(self, new_attr, change.new)

    def __init__(self, **kwargs):
        # observe deprecated config names in oauthenticator
        if self._deprecated_oauth_aliases:
            self.observe(
                self._deprecated_oauth_trait, names=list(self._deprecated_oauth_aliases)
            )
        super().__init__(**kwargs)

class Callable(TraitType):
    """
    A trait which is callable.
    Classes are callable, as are instances
    with a __call__() method.
    """

    info_text = 'a callable'

    def validate(self, obj, value):
        if callable(value):
            return value
        else:
            self.error(obj, value)

class IDPAuthenticator(OAuthenticator):

    login_service = Unicode("OAuth 2.0", config=True)

    extra_params = Dict(help="Extra parameters for first POST request").tag(config=True)

    username_key = Union(
        [Unicode(os.environ.get('OAUTH2_USERNAME_KEY', 'username')), Callable()],
        config=True,
        help="""
        Userdata username key from returned json for USERDATA_URL.

        Can be a string key name or a callable that accepts the returned
        json (as a dict) and returns the username.  The callable is useful
        e.g. for extracting the username from a nested object in the
        response.
        """,
    )

    userdata_params = Dict(
        help="Userdata params to get user data login information"
    ).tag(config=True)

    userdata_method = Unicode(
        os.environ.get('OAUTH2_USERDATA_METHOD', 'GET'),
        config=True,
        help="Userdata method to get user data login information",
    )
    userdata_token_method = Unicode(
        os.environ.get('OAUTH2_USERDATA_REQUEST_TYPE', 'header'),
        config=True,
        help="Method for sending access token in userdata request. Supported methods: header, url. Default: header",
    )

    tls_verify = Bool(
        os.environ.get('OAUTH2_TLS_VERIFY', 'True').lower() in {'true', '1'},
        config=True,
        help="Disable TLS verification on http request",
        )

    basic_auth = Bool(
        os.environ.get('OAUTH2_BASIC_AUTH', 'True').lower() in {'true', '1'},
        config=True,
        help="Disable basic authentication for access token request",
        )

    logout_redirect_url = Unicode(help="""URL for logging out.""").tag(config=True)

    def _logout_redirect_url_default(self):
        return os.getenv('LOGOUT_REDIRECT_URL', '')

    def http_client(self):
        return AsyncHTTPClient(force_instance=True, defaults=dict(validate_cert=self.tls_verify))

    def _get_headers(self):
        headers = {"Accept": "application/json", "User-Agent": "JupyterHub"}

        if self.basic_auth:
            b64key = base64.b64encode(
                bytes("{}:{}".format(self.client_id, self.client_secret), "utf8")
            )
            headers.update({"Authorization": "Basic {}".format(b64key.decode("utf8"))})
        return headers

    async def _get_token(self, http_client, headers, params):
        self.log.info('[IDPAuthenticator] _get_token params: %r', json.dumps(params))

        if self.token_url:
            url = self.token_url
        else:
            raise ValueError("Please set the $OAUTH2_TOKEN_URL environment variable")

        req = HTTPRequest(
            url,
            method="POST",
            headers=headers,
            body=urllib.parse.urlencode(params),
        )

        self.log.info('[IDPAuthenticator] _get_token url: %r', url)

        resp = await http_client.fetch(req)

#         self.log.info('[IDPAuthenticator] _get_token resp.body: %r', resp.body)

        return json.loads(resp.body.decode('utf8', 'replace'))

    async def _get_user_data(self, http_client, token_response):
#         self.log.info('[IDPAuthenticator] _get_user_data token_response: %r', json.dumps(token_response))

        access_token = token_response['access_token']
        token_type = token_response['token_type']

        # Determine who the logged in user is
        headers = {
            "Accept": "application/json",
            "User-Agent": "JupyterHub",
            "Authorization": "{} {}".format(token_type, access_token),
        }
        if self.userdata_url:
            url = url_concat(self.userdata_url, self.userdata_params)
        else:
            raise ValueError("Please set the OAUTH2_USERDATA_URL environment variable")

        if self.userdata_token_method == "url":
            url = url_concat(self.userdata_url, dict(access_token=access_token))

        req = HTTPRequest(
            url,
            method=self.userdata_method,
            headers=headers,
        )

        self.log.info('[IDPAuthenticator] _get_user_data url: %r', url)
        self.log.info('[IDPAuthenticator] _get_user_data headers: %r', json.dumps(headers))

        resp = await http_client.fetch(req)

        self.log.info('[IDPAuthenticator] _get_user_data resp.body: %r', resp.body)

        return json.loads(resp.body.decode('utf8', 'replace'))

    def _create_auth_state(self, token_response, user_data_response):
        self.log.info('[IDPAuthenticator] _create_auth_state token_response: %r', json.dumps(token_response))
        self.log.info('[IDPAuthenticator] _create_auth_state user_data_response: %r', json.dumps(user_data_response))

        access_token = token_response['access_token']
        refresh_token = token_response.get('refresh_token', None)

        os.environ['ACCESS_TOKEN'] = access_token
        os.environ['ID_TOKEN'] = token_response['id_token']
        os.environ['CLIENT_ROLES'] = user_data_response['custom:tenant']

        scope = token_response.get('scope', '')
        if isinstance(scope, str):
            scope = scope.split(' ')

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'oauth_user': user_data_response,
            'scope': scope,
        }

    async def authenticate(self, handler, data=None):
        self.log.info('[IDPAuthenticator] authenticate')
        code = handler.get_argument("code")
        # TODO: Configure the curl_httpclient for tornado
        http_client = self.http_client()

        params = dict(
            redirect_uri=self.get_callback_url(handler),
            code=code,
            grant_type='authorization_code',
        )
        params.update(self.extra_params)

        headers = self._get_headers()

        token_resp_json = await self._get_token(http_client, headers, params)

        user_data_resp_json = await self._get_user_data(http_client, token_resp_json)

        self.log.info('[IDPAuthenticator] authenticate user_data_resp_json: %r', json.dumps(user_data_resp_json))

        if callable(self.username_key):
            name = self.username_key(user_data_resp_json)
        else:
            name = user_data_resp_json.get(self.username_key)
            if not name:
                self.log.error(
                    "OAuth user contains no key %s: %s", self.username_key, user_data_resp_json
                )
                return

        return {
            'name': name,
            'auth_state': self._create_auth_state(token_resp_json, user_data_resp_json)
        }

class LocalGenericOAuthenticator(LocalAuthenticator, IDPAuthenticator):

    """A version that mixes in local system user creation"""

    pass
