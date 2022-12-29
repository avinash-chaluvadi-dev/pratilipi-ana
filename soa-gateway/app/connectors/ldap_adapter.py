from ldap3 import ALL, SAFE_SYNC, Connection, Server
from ldap3.core.exceptions import (LDAPBindError, LDAPException,
                                   LDAPSocketOpenError)

from app.core import constants, exceptions, logging
from app.core.config import settings
from app.utils.formatters import dict_keys_snake

logger = logging.getLogger(__name__)


class LdapAdapter:
    """A Util class for fetching info from AD using LDAP protocol"""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.is_function_acc = False
        self.connection = None

    def __del__(self):
        """Close Ldap Connection when Adapter object is being destroyed"""
        if self.connection:
            logger.info("Closing LDAP connection")
            self.connection.unbind()

    @property
    def default_query(self) -> str:
        if settings.LDAP_USERNAME == self.username:
            self.is_function_acc = True
            return f"CN={self.username},OU=serviceAccounts,OU=Entities,OU=usersAndGroups,DC={settings.LDAP_HOST_DOMAIN},DC=wellpoint,DC=com"
        return f"CN={self.username},OU=Associates,OU=usersAndGroups,DC={settings.LDAP_HOST_DOMAIN},DC=wellpoint,DC=com"

    @property
    def default_attributes(self) -> list:
        if self.is_function_acc:
            return ["cn", "displayName", "userPrincipalName"]
        return ["cn", "displayName", "mail", "userPrincipalName", "memberOf"]

    def get_server(self) -> Server:
        return Server(host=settings.LDAP_HOST, get_info=ALL)

    def authenticate(self) -> Connection:
        """Authenticate to LDAP
        :raises
            BadRequestException :  if invalid credentials are given
            InternalServerError :  When there is an internal error while connecting to AD
        """
        try:
            self.connection = Connection(
                self.get_server(),
                f"{self.username}{settings.LDAP_DOMAIN}",
                self.password,
                client_strategy=SAFE_SYNC,
                auto_bind=True,
            )
            logger.info("LDAP Connection established")
            return self.connection

        except LDAPBindError as e:
            logger.error(f"Error while authenticating to AD {str(e)}")
            raise exceptions.BadRequestException(
                message=constants.LOGIN_BAD_REQUEST,
            )
        except (LDAPSocketOpenError, LDAPException) as e:
            logger.error(f"Error while authenticating to AD {str(e)}")
            raise exceptions.InternalServerError(
                message=constants.GENERIC_INTERNAL_ERROR
            )

    def del_memberof(self, attributes):
        if "memberOf" in attributes:
            del attributes["memberOf"]
        return attributes

    def exc_query(self, query: str = None, attributes: list = None) -> dict:
        if not query:
            query = self.default_query
        if not attributes:
            attributes = self.default_attributes
        if not self.connection:
            raise exceptions.InternalServerError
        search_results = self.connection.extend.standard.paged_search(
            query,
            f"(CN={self.username})",
            attributes=attributes,
            paged_size=5,
        )
        attributes = list(search_results)[0]["attributes"]
        if not self.is_function_acc:
            for group in attributes["memberOf"]:
                if settings.AD_GROUP in group:
                    attributes["group"] = settings.AD_GROUP
                    break
            if "group" not in attributes:
                raise exceptions.ForbiddenException
            attributes = self.del_memberof(attributes)
        else:
            if "displayName" not in attributes:
                raise exceptions.ForbiddenException
            attributes["group"] = attributes["displayName"]
        return dict_keys_snake(attributes)
