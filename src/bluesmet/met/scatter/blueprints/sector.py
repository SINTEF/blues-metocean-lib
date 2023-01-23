# Description for stochastic process at a sector.
# Generated with SectorBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class SectorBlueprint(NamedEntityBlueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="Sector", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("direction","number","sector direction.",default=0.0))
        self.add_attribute(Attribute("sectorSize","number","sector size.",default=0.0))
        self.add_attribute(BlueprintAttribute("wave","met/scatter/Wave","the scatter data for wave.",True))
        self.add_attribute(BlueprintAttribute("wind","met/scatter/WindCurrent","the scatter data for wind at different levels.",True,Dimension("*")))
        self.add_attribute(BlueprintAttribute("current","met/scatter/WindCurrent","the scatter data for current at different levels.",True,Dimension("*")))