from .enums import *
from typing import Optional, List

def get_printing_data(
    product_sides: int,
    product_chromaticity: AP24PrintingChromaticityEnum,
    product_format: AP24ProductFormatEnum,
    product_width: Optional[int] = None,
    product_height: Optional[int] = None,
    paper_type: Optional[str] = None,
    paper_feature: Optional[str] = None,
    paper_coating: Optional[str] = None,
    empty_pages: Optional[List[int]] = None,
    pruning: Optional[AP24PostprintPruningEnum] = None,
    paper_density_inner: Optional[AP24PaperDensityEnum] = None,
    paper_density_cover: Optional[AP24PaperDensityEnum] = None,
) -> dict:
    """Structure printing data for Click-Knock API."""
    return {
        "product_sides": product_sides,
        "product_chromaticity": product_chromaticity,
        "product_format": product_format,
        "product_width": product_width,
        "product_height": product_height,
        "paper_type": paper_type,
        "paper_feature": paper_feature,
        "paper_coating": paper_coating,
        "empty_pages": empty_pages,
        "pruning": pruning,
        "paper_density_inner": paper_density_inner,
        "paper_density_cover": paper_density_cover,
    }

def get_postprint_data(
    face_cover: Optional[AP24PostprintCoverFaceEnum] = None,
    back_cover: Optional[AP24PostprintCoverBackEnum] = None,
    lamination: Optional[AP24PostprintLaminationEnum] = None,
    spring: Optional[AP24PostprintSpringEnum] = None,
    stitching: Optional[AP24PostprintStitchingEnum] = None,
    bracer: Optional[AP24PostprintBracerEnum] = None,
    packing: Optional[AP24PostprintPackingEnum] = None,
    rounding: Optional[AP24PostprintRoundingEnum] = None,
) -> dict:
    """Structure postprint data for Click-Knock API."""
    return {
        "face_cover": face_cover,
        "back_cover": back_cover,
        "lamination": lamination,
        "spring": spring,
        "stitching": stitching,
        "bracer": bracer,
        "packing": packing,
        "rounding": rounding,
    }