# 
# Generated with FieldPointBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class FieldPointBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="FieldPoint", package_path="met/nora3", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("latitude","number","",optional=False,default=0.0))
        self.add_attribute(Attribute("longitude","number","",optional=False,default=0.0))