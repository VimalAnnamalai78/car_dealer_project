from typing import List
from sqlalchemy.orm import Session
from database import schemas, models, connection_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, HTTPException

from utils.util_functions import Hasher
from utils.util_functions import authorize


router = APIRouter()
get_db = connection_db.get_db


@router.get(path='/', status_code=status.HTTP_200_OK, response_model=schemas.ShowDealers, tags=['Get Particular Dealers'])
def get_dealer(dealer_mobile: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == dealer_mobile)

    if not dealer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dealer is not exist for given mobile number: {dealer_mobile}")

    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg' : jsonable_encoder(dealer.first())})


@router.get(path='/list', response_model=List[schemas.ShowDealers], tags=['Get All Dealers'])
def get_all_dealer(db: Session = Depends(get_db)):
    dealers = db.query(models.Dealers).all()
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(dealers)})


@router.post(path='/signup', status_code=status.HTTP_201_CREATED, tags=['Create Dealers/Signup Dealers'])
def create_dealer(request: schemas.Dealers, db: Session = Depends(get_db)):
    existing_dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == request.dealer_mobile)
    if existing_dealer.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"dealer already exist for given mobile no: {request.dealer_mobile}")
    request.dealer_password = Hasher.get_password_hash(request.dealer_password)
    dealer = models.Dealers(**request.dict())
    db.add(dealer)
    db.commit()
    db.refresh(dealer)
    return JSONResponse(content={'status_code': status.HTTP_201_CREATED,
                                 'msg': f'account created successfully for {request.dealer_mobile}'})


@router.put(path='/', status_code=status.HTTP_202_ACCEPTED, tags=['Edit Dealers'])
def edit_dealer(request: schemas.UpdateDealers, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == request.dealer_mobile)

    if not dealer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dealer is not exist for given mobile number: {request.dealer_mobile}")
    dealer.update(request.dict())
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_202_ACCEPTED, 'msg': 'Updated Successfully'})


@router.delete(path='/', status_code=status.HTTP_204_NO_CONTENT, tags=['Delete Given Dealers'])
def delete(dealer_mobile: int, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == dealer_mobile)
    if not dealer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dealers with id {id} not found")
    dealer.delete()
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_204_NO_CONTENT,
                                 'msg': f'account deleted successfully for {dealer_mobile}'})


@router.patch(path='/resetpassword', status_code=status.HTTP_202_ACCEPTED, tags=['Dealers Reset Password'])
def reset_password(request: schemas.ResetPassword, dealer: schemas.ShowDealers = Depends(authorize),
                   db: Session = Depends(get_db)):
    if dealer:
        if Hasher.verify_password(request.old_password, dealer.first().dealer_password):
            request.dealer_password = Hasher.get_password_hash(request.dealer_password)
            del request.old_password
            dealer.update(request.dict())
            db.commit()
            return JSONResponse(content={'status_code': status.HTTP_202_ACCEPTED, 'msg': 'Updated Successfully'})
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"incorrect old password is given")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dealer with mobile number : {request.dealer_mobile} is not found")


@router.patch(path='/forgetpassword', status_code=status.HTTP_202_ACCEPTED, tags=['Dealers Forget Password'])
def forget_password(request: schemas.Login, db: Session = Depends(get_db)):
    dealer = db.query(models.Dealers).filter(models.Dealers.dealer_mobile == request.dealer_mobile)
    request.dealer_password = Hasher.get_password_hash(request.dealer_password)

    if not dealer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"dealer with mobile number : {request.dealer_mobile} is not found")
    dealer.update(request.dict())
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_202_ACCEPTED, 'msg': 'Updated Successfully'})


@router.get(path='/listcars', response_model=List[schemas.ShowDealers], tags=['Get All Cars Of the Dealer'])
def get_dealer_cars(dealer_id: int, db: Session = Depends(get_db)):
    cars = db.query(models.Cars).filter(models.Cars.dealer_id == dealer_id).all()

    if not cars:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No car is exist for given dealer id: {dealer_id}")

    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(cars)})