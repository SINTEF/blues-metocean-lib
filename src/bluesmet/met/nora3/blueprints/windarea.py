# 
# Generated with WindAreaBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class WindAreaBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="WindArea", package_path="met/nora3", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("label","string","",optional=False))
        self.add_attribute(Attribute("latitude","number","Center of area, latitude",optional=False,default=0.0))
        self.add_attribute(Attribute("longitude","number","Center of area, longitude",optional=False,default=0.0))
        self.add_attribute(BlueprintAttribute("fields","met/nora3/Field","",True,Dimension("*")))