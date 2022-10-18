from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from database import models, connection_db, schemas
from utils.util_functions import Hasher
from utils.util_functions import create_access_token

from sqlalchemy.orm import Session

router = APIRouter()


@router.post(path='')
def login(request: schemas.Login, db: Session = Depends(connection_db.get_db)):
    """
    Login validation method.

    :param request: Payload with mobile number & password of a dealer.
    :param db: Database Session.
    :return: Confirmation response with status code.
    """

    dealer = db.query(models.Dealers).filter(
        models.Dealers.dealer_mobile == request.dealer_mobile)
    if not dealer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Mobile Number")

    dealer_data = dealer.first()
    if not Hasher.verify_password(request.dealer_password, dealer_data.dealer_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    access_token = create_access_token({"dealer_mobile": dealer_data.dealer_mobile})
    dealer.update({"access_token": access_token})
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': "logged-in successfully",
                                 'access_token': access_token, 'token_type': 'bearer'})
