from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

import sys

# This search ought to return all groups to which the user belongs.
# django_auth_ldap uses this to determine group heirarchy.

# -- docker env
BASE_DN = os.environ.get('BASE_DN', 'dc=example,dc=com')
GROUP_TYPE = os.environ.get('GROUP_TYPE', 'TRUE_LDAP')
LDAP_REQUIRE_GROUP = os.environ.get('REQUIRE_LDAP_GROUP', 'CN=NETBOX_USERS,DC=example,DC=com')
GROUP_IS_ACTIVE = os.environ.get('GROUP_IS_ACTIVE', 'cn=active,ou=groups,dc=example,dc=com')
GROUP_IS_STAFF = os.environ.get('GROUP_IS_STAFF', 'cn=staff,ou=groups,dc=example,dc=com')
GROUP_IS_SUPERUSR = os.environ.get('GROUP_IS_SUPERUSER', 'cn=superuser,ou=groups,dc=example,dc=com')
# --

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(BASEDN,
                                    ldap.SCOPE_SUBTREE,
                                    "(objectClass=group)")

if GROUP_TYPE == "AD":
    AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
elif GROUP_TYPE == "TRUE_LDAP":
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
else:
    print("GROUP_TYPE value betwen AD or TRUE_LDAP")
    sys.exit(2)

# Define a group required to login.
AUTH_LDAP_REQUIRE_GROUP = REQUIRE_LDAP_GROUP

# Define special user types using groups. Exercise great caution when assigning superuser status.
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": GROUP_IS_ACTIVE,
        "is_staff": GROUP_IS_STAFF,
        "is_superuser": GROUP_IS_SUPERUSER
    }

# For more granular permissions, we can map LDAP groups to Django groups.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache groups for one hour to reduce LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
