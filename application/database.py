from application.auth.models import User, Role


def init_db(db, user_manager):
    db.create_all()
    admin_role = find_or_create_role(db, "admin")
    db.session.commit()


def find_or_create_role(db, name):
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=role)
        db.session.add(role)
    return role


def find_or_create_user(db, user_manager, name, username, password, role=None):
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User(
            name=name,
            username=username,
            password=user_manager.password_manager.hash_password(password),
        )
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

