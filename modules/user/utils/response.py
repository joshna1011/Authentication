from fastapi.responses import JSONResponse

def success_response(data=None, message="success"):
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": message,
            "data": data,
        }
    )

def failure_response(message="failed", status_code=400, data=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "failure",
            "message": message,
            "data": data,
        }
    )
