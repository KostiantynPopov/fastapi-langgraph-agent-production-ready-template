from enum import Enum

class AP24PrintingChromaticityEnum(str, Enum):
    """Printing type."""
    BLACK_AND_WHITE = "black_and_white"
    COLOR = "color"

class AP24ProductFormatEnum(str, Enum):
    """Product format."""
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"
    A7 = "A7"
    EF = "EF"
    BC_90_50 = "BC_90_50"
    BC_85_55 = "BC_85_55"
    PHOTO_9_13 = "PHOTO_9_13"
    PHOTO_10_15 = "PHOTO_10_15"
    PHOTO_15_21 = "PHOTO_15_21"
    PHOTO_13_18 = "PHOTO_13_18"
    PHOTO_21_30 = "PHOTO_21_30"
    PHOTO_30_40 = "PHOTO_30_40"
    CUSTOM = "CUSTOM"

class AP24PaperDensityEnum(str, Enum):
    """Paper density."""
    DENSITY_80 = "80"
    DENSITY_90 = "90"
    DENSITY_100 = "100"
    DENSITY_115 = "115"
    DENSITY_130 = "130"
    DENSITY_150 = "150"
    DENSITY_170 = "170"
    DENSITY_200 = "200"
    DENSITY_250 = "250"
    DENSITY_300 = "300"
    DENSITY_350 = "350"

class AP24PostprintPruningEnum(str, Enum):
    """Pruning type."""
    NONE = "none"
    ALL = "all"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class AP24PostprintLaminationEnum(str, Enum):
    """Lamination type."""
    NONE = "none"
    GLOSSY = "glossy"
    MATTE = "matte"

class AP24PostprintCoverFaceEnum(str, Enum):
    """Cover face type."""
    NONE = "none"
    GLOSSY = "glossy"
    MATTE = "matte"

class AP24PostprintCoverBackEnum(str, Enum):
    """Cover back type."""
    NONE = "none"
    GLOSSY = "glossy"
    MATTE = "matte"

class AP24PostprintSpringEnum(str, Enum):
    """Spring type."""
    NONE = "none"
    PLASTIC = "plastic"
    METAL = "metal"

class AP24PostprintStitchingEnum(str, Enum):
    """Stitching type."""
    NONE = "none"
    STAPLE = "staple"
    THERMO = "thermo"

class AP24PostprintBracerEnum(str, Enum):
    """Bracer type."""
    NONE = "none"
    TWO = "two"
    FOUR = "four"

class AP24PostprintPackingEnum(str, Enum):
    """Packing type."""
    NONE = "none"
    PACK = "pack"
    BOX = "box"

class AP24PostprintRoundingEnum(str, Enum):
    """Rounding type."""
    NONE = "none"
    ALL = "all"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
