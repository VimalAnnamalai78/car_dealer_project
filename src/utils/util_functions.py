from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from database import schemas, models, connection_db

get_db = connection_db.get_db
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


def create_access_token(to_encode: dict):
    return jwt.encode(to_encode, 'secret_key', algorithm="HS256")


async def authorize(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        dealer_mobile: str = payload.get("dealer_mobile")
        if dealer_mobile is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == dealer_mobile)
        if not dealer:
            raise credentials_exception
        return dealer
