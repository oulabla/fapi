from pydantic import BaseModel, annotated_types
from enum import Enum
from typing import Optional, Union
import datetime
import time

from pydantic.fields import Field

class ProductType(str, Enum):
    standard = "standard"
    custom = "custom"
    model = "model"

class ProductModel(BaseModel):
    id: int
    type: ProductType
    name: str
    description: str
    price: float
    created_at: Optional[datetime.datetime] = time.time()

class ProductStandardModel(ProductModel):
    type: Optional[ProductType] = ProductType.standard
    supplier: str

class ProductCustomModel(ProductModel):
    type: Optional[ProductType] = ProductType.custom
    info: str

class ProductBase(BaseModel):
    __root__: Union[ProductCustomModel, ProductStandardModel] = Field(..., discriminator='type')

# ProductBase = Annotated[Union[ProductStandardModel, ProductCustomModel], Field(discriminator='type')]

