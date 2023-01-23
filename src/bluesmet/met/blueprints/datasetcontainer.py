# 
# Generated with DatasetContainerBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class DatasetContainerBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="DatasetContainer", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",optional=False))
        self.add_attribute(BlueprintAttribute("containers","met/DatasetContainer","",True,Dimension("*")))
        self.add_attribute(BlueprintAttribute("datasets","met/Dataset","",True,Dimension("*")))