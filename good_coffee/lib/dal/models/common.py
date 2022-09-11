import typing as t

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base: t.Any = declarative_base(metadata=metadata)
