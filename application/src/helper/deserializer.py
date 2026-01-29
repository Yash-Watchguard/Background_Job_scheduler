from boto3.dynamodb.types import TypeDeserializer
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar( "T" , bound=BaseModel)

def dynamo_to_model(dynamo_object: dict , model: Type[T]) -> T:
    
    deserializer = TypeDeserializer()
    
    python_dict ={
        k:deserializer.deserialize(v)
        for k,v in dynamo_object.items()
    }
    return model(**python_dict)  

