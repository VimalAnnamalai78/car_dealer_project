from typing import List
from sqlalchemy.orm import Session
from database import schemas, models, connection_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, HTTPException

from utils.util_functions import Hasher
from utils.util_functions import authorize  # Dint Apply the  authoriziation to access the car api's.

router = APIRouter()
get_db = connection_db.get_db


@router.get(path='/', status_code=status.HTTP_200_OK, response_model=schemas.ShowCars, tags=['Get Particular Car'])
def get_car(reg_num: str, db: Session = Depends(get_db)):
    car = db.query(models.Cars).filter(models.Cars.reg_num == reg_num)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Car with reg_num: {reg_num} not found")
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(car.first())})


@router.post(path='/', status_code=status.HTTP_201_CREATED, tags=['Add Car'])
def add_car(request: schemas.Cars, db: Session = Depends(get_db)):
    car_exist = db.query(models.Cars).filter(models.Cars.reg_num == request.reg_num)
    if car_exist.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Car exists for given Registration Number {request.reg_num}")
    car = models.Cars(**request.dict())
    db.add(car)
    db.commit()
    db.refresh(car)
    return JSONResponse(content={'status_code': status.HTTP_201_CREATED,
                                 'msg': f'car added successfully for {request.reg_num}'})


@router.put(path='/', status_code=status.HTTP_202_ACCEPTED, tags=['Edit Cars'])
def edit_cars(request: schemas.Cars, db: Session = Depends(get_db)):
    cars = db.query(models.Cars).filter(models.Cars.reg_num == request.reg_num)

    if not cars.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No car matching with given{request.reg_num}")
    cars.update(request.dict())
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_202_ACCEPTED, 'msg': 'Updated Successfully'})


@router.delete(path='/', status_code=status.HTTP_204_NO_CONTENT, tags=['Delete Given Car'])
def delete(reg_num: str, db: Session = Depends(get_db)):
    car = db.query(models.Cars).filter(models.Cars.reg_num == reg_num)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cars with id {id} not found")
    car.delete()
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_204_NO_CONTENT,
                                 'msg': f'account deleted successfully for {reg_num}'})


@router.get(path='/list', response_model=List[schemas.ShowCars], tags=['Get All Cars'])
def get_all_cars(db: Session = Depends(get_db)):
    cars = db.query(models.Cars).all()
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(cars)})