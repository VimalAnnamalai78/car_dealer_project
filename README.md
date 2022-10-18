# CARDEALER VENDOR APP

# Python Version 3.10.4

# Windows: Environment Setup
```commandline
python3 -m venv ..\cardealer_python_env
..\vendor_python_env\Scripts\activate
pip install -r src\requirements.txt
```
# Windows: Start Cardealer FastAPI App
```commandline
cd src\
uvicorn main:app --reload
```

# Linux: Environment Setup
```commandline
python3 -m venv ../cardealer_python_env
source ../cardealer_python_env/bin/activate
pip install -r src/requirements.txt
```
# Linux: Start Cardealer FastAPI App
```commandline
cd src/
uvicorn main:app --reload
```

# Swagger Docs: All Endpoint are available here
```commandline
http://127.0.0.1:8000/docs
```

#API ROUTES FOR DEALER
    # POST - http://localhost:8000/dealer/signup
    # PUT  - http://localhost:8000/cars
    # GET  - http://localhost:8000/dealer/list
    # GET  - http://localhost:8000/dealer?dealer_mobile=4565152467
    # DEL  - http://localhost:8000/dealer?dealer_mobile=4565152467
    # POST - http://localhost:8000/login
    # PATCH - http://localhost:8000/dealer/forgetpassword
    # PATCH - http://localhost:8000/dealer/resetpassword


#API ROUTES FOR CARS
    # POST - http://localhost:8000/cars
    # PUT  - http://localhost:8000/cars
    # GET  - http://localhost:8000/cars/list
    # GET  - http://localhost:8000/cars?reg_num=XX 07 34099
    # DEL  - http://localhost:8000/cars?reg_num=XX 07 3408

#Note:
    # Why FastApi?
        Frank Answer is :-Since it is a minimalistic  & quick project. Moreover during my experience 
        i worked with django but not with Fastapi also i used this chance to learn this framework.

        Technically in project i would consider the frameworks based on the requirements & nature of the application only.

    # Almost 13 endpoints are added above & Attached POSTMAN JSON Request for your reference
    # Still Many Test cases to be handled but due to time constraints I have covered certain scenarios only.
    # Below things i planned to add but due to time, i suppose to limit with basic needs. 
         1) Async/await 
         2) Hiding passwords in response
         3) Before creating a dealer shouldn't allow to create a car.
         4) API authorization not added for many API endpoint except /restpassword because i need time to test.
    
