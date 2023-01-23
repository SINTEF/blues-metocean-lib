# 
# Generated with FieldBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class FieldBlueprint(NamedEntityBlueprint):
    """"""

    def __init__(self, name="Field", package_path="met/nora3", description=""):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("label","string","",optional=False))
        self.add_attribute(Attribute("latitude","number","",Dimension("*"),default=0.0))
        self.add_attribute(Attribute("longitude","number","",Dimension("*"),default=0.0))
        self.add_attribute(BlueprintAttribute("points","met/nora3/FieldPoint","",True,Dimension("*")))