from typing import List
from sqlalchemy.orm import Session
from database import schemas, models, connection_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, HTTPException

from utils.util_functions import Hasher
from utils.util_functions import authorize  # Didn't Apply the authorization to access the car api's.

router = APIRouter()
get_db = connection_db.get_db


@router.get(path='/', status_code=status.HTTP_200_OK, response_model=schemas.ShowCars, tags=['Get Particular Car'])
def get_car(reg_num: str, db: Session = Depends(get_db)):
    """
    Extract a car details for a given register number.

    :param reg_num: register number of car to be extracted.
    :param db: Database Session.
    :return: Car data json matched for a given reg_num & with status code.
    """

    car = db.query(models.Cars).filter(models.Cars.reg_num == reg_num)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Car found for given reg_num: {reg_num} found")
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(car.first())})


@router.post(path='/', status_code=status.HTTP_201_CREATED, tags=['Add Car'])
def add_car(request: schemas.Cars, db: Session = Depends(get_db)):
    """
    Add a new car to the inventory.

    :param request: Json payload with car details.
    :param db: Database Session.
    :return: Confirmation response with status code.
    """

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
    """
    Edit an existing car from the inventory.

    :param request: Json payload with updated car details.
    :param db: Database Session.
    :return: Confirmation response with status code.
    """

    cars = db.query(models.Cars).filter(models.Cars.reg_num == request.reg_num)

    if not cars.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Car found for given reg_num: {request.reg_num} found")
    cars.update(request.dict())
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_202_ACCEPTED, 'msg': 'Updated Successfully'})


@router.delete(path='/', status_code=status.HTTP_204_NO_CONTENT, tags=['Delete Given Car'])
def delete(reg_num: str, db: Session = Depends(get_db)):
    """
    Delete a car for a given register number from the inventory.

    :param reg_num: register number of car to be deleted.
    :param db: Database Session.
    :return: Confirmation response with status code.
    """

    car = db.query(models.Cars).filter(models.Cars.reg_num == reg_num)
    if not car.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Car found for given reg_num: {reg_num} found")
    car.delete()
    db.commit()
    return JSONResponse(content={'status_code': status.HTTP_204_NO_CONTENT,
                                 'msg': f'Car deleted successfully for {reg_num}'})


@router.get(path='/list', response_model=List[schemas.ShowCars], tags=['Get All Cars'])
def get_all_cars(db: Session = Depends(get_db)):
    """
    Get all available cars from the inventory. It includes all dealers cars.

    :param db: Database Session.
    :return: Details of all cars available in the inventory with status code.
    """

    cars = db.query(models.Cars).all()
    return JSONResponse(content={'status_code': status.HTTP_200_OK, 'msg': jsonable_encoder(cars)})
