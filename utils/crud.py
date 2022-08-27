from sqlalchemy.orm import Session

import models.tokens as models


def get_token(db: Session):
    """
    Get token from database
    :param db:
    :return: Token if exists, None otherwise
    """
    token = db.query(models.Token).first()
    return token.token if token else None


def create_or_update_token(db: Session, token: str, expire: int):
    """
    Create or update a token
    :param db:
    :param token:
    :param expire:
    :return: None
    """
    db_token = db.query(models.Token).first()
    if db_token:
        db_token.token = token
        db_token.expire = expire
    else:
        db_token = models.Token(token, expire)
        db.add(db_token)
    db.commit()
