# Description for stochastic process at a sector.
# Generated with WindCurrentBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class WindCurrentBlueprint(NamedEntityBlueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="WindCurrent", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("level","number","measured level.",default=0.0))
        self.add_attribute(Attribute("speed","number","the scatter data for speed.",Dimension("*"),Dimension("*"),default=0.0))
        self.add_attribute(Attribute("direction","number","the scatter data for direction.",Dimension("*"),Dimension("*"),default=0.0))