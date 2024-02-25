from . import base, autonomous
from typing import TypedDict
import types


class ModuleTypes(TypedDict):
    autonomous: types.ModuleType
    base: types.ModuleType


Types: ModuleTypes = {
    "autonomous": autonomous,
    "base": base,
}
