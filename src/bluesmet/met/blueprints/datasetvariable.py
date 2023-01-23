# 
# Generated with DatasetVariableBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class DatasetVariableBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="DatasetVariable", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",optional=False))
        self.add_attribute(Attribute("name","string","",optional=False))
        self.add_attribute(Attribute("unit","string",""))
        self.add_attribute(Attribute("dimensions","string",""))