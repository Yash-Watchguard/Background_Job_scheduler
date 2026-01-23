from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
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


def model_to_dynamo_with_keys(
    model: BaseModel,
    pk: str,
    sk: str
) -> dict:
    serializer = TypeSerializer()
    data = model.model_dump(by_alias=True)
    data["PK"] = pk
    data["SK"] = sk

    return {
        k: serializer.serialize(v)
        for k, v in data.items()
    }