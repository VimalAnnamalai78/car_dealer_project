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

#Note:
```commandline
# Almost 13 endpoints are added 
# Still Many Test cases to be handled but due to time constraints certain only scenarios been covered
# Certain cases not been handled 
#     ex:- before creating a dealer couldn't allow to create a car.
#     ex:- Hiding passwords in response, etc
# Still API authorization not added for many API endpoint except /restpassword because i need time to test.
# Attached POSTMAN JSON Request for your reference
```