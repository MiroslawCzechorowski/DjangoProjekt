"""
OAuth2 Adapter for Battle.net

Resources:

* Battle.net OAuth2 documentation:
    https://dev.battle.net/docs/read/oauth
* Battle.net API documentation:
    https://dev.battle.net/io-docs
* Original announcement:
    https://us.battle.net/en/forum/topic/13979297799
* The Battle.net API forum:
    https://us.battle.net/en/forum/15051532/
"""
import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter, OAuth2CallbackView, OAuth2LoginView
)
from .provider import BattleNetProvider


def _check_errors(data):
    # The expected output from the Battle.net API follows this format:
    # {"id": 12345, "battletag": "Example#12345"}
    # The battletag is optional.
    if "error" in data:
        # For errors, we expect the following format:
        # {"error": "error_name", "error_description": "Oops!"}
        # For example, if the token is not valid, we will get:
        # {
        #   "error": "invalid_token",
        #   "error_description": "Invalid access token: abcdef123456"
        # }
        error = data["error"]
        desc = data.get("error_description", "")
        raise OAuth2Error("Battle.net error: %s (%s)" % (error, desc))
    elif "id" not in data:
        # If the id is not present, the output is not usable (no UID)
        raise OAuth2Error("Invalid data from Battle.net API: %r" % (data))


class BattleNetOAuth2Adapter(OAuth2Adapter):
    """
    OAuth2 adapter for Battle.net
    https://dev.battle.net/docs/read/oauth

    Region is set to us by default, but can be overridden with the
    `region` GET parameter when performing a login.
    Can be any of eu, us, kr, sea, tw or cn
    """
    provider_id = BattleNetProvider.id
    valid_regions = ("us", "eu", "kr", "sea", "tw", "cn")

    @property
    def battlenet_region(self):
        region = self.request.GET.get("region", "").lower()
        if region in self.valid_regions:
            return region
        return "us"

    @property
    def battlenet_base_url(self):
        region = self.battlenet_region
        if region == "cn":
            return "https://www.battlenet.com.cn"
        return "https://%s.battle.net" % ("us" if region == "sea" else region)

    @property
    def battlenet_api_url(self):
        if self.battlenet_region == "cn":
            return "https://api.battlenet.com.cn"
        return "https://%s.api.battle.net" % (self.battlenet_region)

    @property
    def access_token_url(self):
        return self.battlenet_base_url + "/oauth/token"

    @property
    def authorize_url(self):
        return self.battlenet_base_url + "/oauth/authorize"

    @property
    def profile_url(self):
        return self.battlenet_api_url + "/account/user"

    def complete_login(self, request, app, token, **kwargs):
        params = {"access_token": token.token}
        response = requests.get(self.profile_url, params=params)
        data = response.json()
        _check_errors(data)

        # Add the region to the data so that we can have it in `extra_data`.
        data["region"] = self.battlenet_region

        return self.get_provider().sociallogin_from_response(request, data)

    def get_callback_url(self, request, app):
        r = super(BattleNetOAuth2Adapter, self).get_callback_url(request, app)
        region = request.GET.get("region", "").lower()
        # Pass the region down to the callback URL if we specified it
        if region and region in self.valid_regions:
            r += "?region=%s" % (region)
        return r


oauth2_login = OAuth2LoginView.adapter_view(BattleNetOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(BattleNetOAuth2Adapter)
