import bcrypt


async def create_hashed_password(password):
    salt_value = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt_value)
