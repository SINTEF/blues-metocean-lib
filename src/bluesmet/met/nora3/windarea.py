# This an autogenerated file
# 
# Generated with WindArea
from typing import Dict,Sequence,List
from dmt.blueprint import Blueprint
from dmt.namedentity import NamedEntity
from .blueprints.windarea import WindAreaBlueprint
from .field import Field

class WindArea(NamedEntity):
    """
    Keyword arguments
    -----------------
    description : str
         (default "")
    name : str
         (default None)
    label : str
         (default None)
    latitude : float
         Center of area, latitude(default 0.0)
    longitude : float
         Center of area, longitude(default 0.0)
    fields : List[Field]
    """

    def __init__(self , description="", latitude=0.0, longitude=0.0, **kwargs):
        super().__init__(**kwargs)
        self.description = description
        self.name = None
        self.label = None
        self.latitude = latitude
        self.longitude = longitude
        self.fields = list()
        for key, value in kwargs.items():
            if not isinstance(value, Dict):
                setattr(self, key, value)


    @property
    def blueprint(self) -> Blueprint:
        """Return blueprint that this entity represents"""
        return WindAreaBlueprint()


    @property
    def description(self) -> str:
        """"""
        return self.__description

    @description.setter
    def description(self, value: str):
        """Set description"""
        self.__description = value

    @property
    def name(self) -> str:
        """"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set name"""
        self.__name = value

    @property
    def label(self) -> str:
        """"""
        return self.__label

    @label.setter
    def label(self, value: str):
        """Set label"""
        self.__label = value

    @property
    def latitude(self) -> float:
        """Center of area, latitude"""
        return self.__latitude

    @latitude.setter
    def latitude(self, value: float):
        """Set latitude"""
        self.__latitude = float(value)

    @property
    def longitude(self) -> float:
        """Center of area, longitude"""
        return self.__longitude

    @longitude.setter
    def longitude(self, value: float):
        """Set longitude"""
        self.__longitude = float(value)

    @property
    def fields(self) -> List[Field]:
        """"""
        return self.__fields

    @fields.setter
    def fields(self, value: List[Field]):
        """Set fields"""
        if not isinstance(value, Sequence):
            raise Exception("Expected sequense, but was " , type(value))
        self.__fields = value
