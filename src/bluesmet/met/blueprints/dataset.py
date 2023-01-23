# 
# Generated with DatasetBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class DatasetBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="Dataset", package_path="met", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string","",optional=False))
        self.add_attribute(Attribute("fromDate","string",""))
        self.add_attribute(Attribute("url","string",""))
        self.add_attribute(Attribute("latitudes","number","",Dimension("*"),default=0.0))
        self.add_attribute(Attribute("longitudes","number","",Dimension("*"),default=0.0))
        self.add_attribute(BlueprintAttribute("variables","met/DatasetVariable","",True,Dimension("*")))