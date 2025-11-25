from ldap3 import Server, Connection, ALL, SUBTREE
from config import Query
from config import LDAPConfig

def check_ldap(username: str, password: str ):
    try:
        ldap_address = LDAPConfig.LDAP_SERVER
        ldap_user    = LDAPConfig.LDAP_ADMIN
        ldap_password= LDAPConfig.LDAP_PASS


        server = Server(ldap_address, get_info=ALL)
        conn = Connection(
            server,
            ldap_user,
            ldap_password,
            auto_bind=True,
        )

        # 2. Buscar el DN del usuario
        search_filter = f"(uid={username})"  # Puede ser 'sAMAccountName', 'cn', etc. según tu LDAP
        conn.search(
            search_base="dc=uh,dc=cu",
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=["Title","cn","sn","ou","Categoria","CI"],
        )

        if not conn.entries:
            return Query.ERROR_NOT_FOUND, {}

        entry = conn.entries[0]
        user_dn = entry.entry_dn
        user_category = entry.Categoria.value
        user_data = {
            "ci": entry.CI.value
        }
        
        # 3. Intentar autenticar con las credenciales del usuario
        user_conn = Connection(server, user_dn, password, auto_bind=True)

        # Si llegamos aquí, la autenticación fue exitosa
        user_conn.unbind()
        
        return Query.APPROVED, user_data

    except Exception as e:
        if "invalidCredentials" in str(e):
            return Query.ERROR_PASSWORD, {}
        else:
            return Query.ERROR_SERVICE, {}
        
def search_user(username: str):
    try:
        ldap_address = LDAPConfig.LDAP_SERVER
        ldap_user    = LDAPConfig.LDAP_ADMIN
        ldap_password= LDAPConfig.LDAP_PASS


        server = Server(ldap_address, get_info=ALL)
        conn = Connection(
            server,
            ldap_user,
            ldap_password,
            auto_bind=True,
        )
        print("1")
        # 2. Buscar el DN del usuario
        search_filter = f"(uid={username})"  # Puede ser 'sAMAccountName', 'cn', etc. según tu LDAP
        conn.search(
            search_base="dc=uh,dc=cu",
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=["Title","cn","sn","ou","Categoria","CI","mail"],
        )
        print("2")
        if not conn.entries:
            return Query.ERROR_NOT_FOUND, {}

        entry = conn.entries[0]
        print("4")
        user_data = {
            "mail": entry.mail.value,
            "ci": entry.CI.value
        }
        print("3")
        
        return Query.APPROVED, user_data

    except Exception as e:
        if "invalidCredentials" in str(e):
            return Query.ERROR_PASSWORD, {}
        else:
            return Query.ERROR_SERVICE, {}
