# Description for stochastic process at a sector.
# Generated with WaveBlueprint
from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from dmt.blueprints.namedentity import NamedEntityBlueprint

class WaveBlueprint(NamedEntityBlueprint):
    """Description for stochastic process at a sector."""

    def __init__(self, name="Wave", package_path="met/scatter", description="Description for stochastic process at a sector."):
        super().__init__(name,package_path,description)
        self.add_attribute(Attribute("description","string","",default=""))
        self.add_attribute(Attribute("name","string",""))
        self.add_attribute(Attribute("occurence","number","the scatter data for occurrence of Hs-Tp.",Dimension("*"),Dimension("*"),default=0.0))