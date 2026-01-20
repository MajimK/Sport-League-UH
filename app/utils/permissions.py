from app.database.models.users import UserRole

ROLE_PERMISSIONS = {
    UserRole.admin: {"create_user","delete_user","update_user","register_player","comment_match","publish_match"},
    UserRole.manager: {"register_player", "publish_match"},
    UserRole.comunicator: {"comment_match", "publish_match"}
}
