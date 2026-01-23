
from fastapi import UploadFile, status
from errors.app_exception import AppException
from constants.error_messages import invalid_scipt_extension,s3_uload_error
from constants.custom_error_code_registry import Bad_Request,S3_script_Upload_error

class S3Service:
    def __init__(self, s3_client, bucket_name:str):
        self.s3_client= s3_client
        self.bucket_name = bucket_name
        
    def upload_script(self, file:UploadFile, job_id:str)->str:
        
        # first check the .py
        if not file.filename or not file.filename.endswith(".py"):
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST,message=invalid_scipt_extension,error_code=Bad_Request)
        
        object_key = f"jobs/{job_id}/script.py"
        
        try:
            self.s3_client.upload_fileobj(
                Fileobj=file.file,
                Bucket=self.bucket_name,
                Key=object_key,
                ExtraArgs={
                    "ContentType": "text/x-python"
                }
            )
        except Exception as e:
            raise AppException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"{s3_uload_error}{str(e)}",
                error_code=S3_script_Upload_error
            )
        
        return f"s3://{self.bucket_name}/{object_key}"