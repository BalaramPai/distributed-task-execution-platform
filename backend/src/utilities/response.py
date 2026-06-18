# src/utilities/response.py

def success_response(message='Sucessful',data=None):
    return {
        "status" : True,
        "data" : data if data is not None else [],
        "message" : message,
        "error" : None
    }
    
def error_response(message="Error",error=None):
    return {
        "status": False,
        "data" : [],
        "message" : message,
        "error" : error if error is not None else "Something went wrong"
    }