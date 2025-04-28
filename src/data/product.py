
from typing import Literal


PRODUCT_CSS_SELECTOR_TYPE = Literal["name", "description", "price", "sku", "image", "brand"]

def product_css_selector(type: PRODUCT_CSS_SELECTOR_TYPE) -> str:
    if type == "name":
        return "#product_details > h1:nth-child(2)"
    
    if type == "description":
        return "#product_details > h1:nth-child(2)"
    if type == "price":
        return "#price"
    if type == "sku":
        return "#product_details > form > div > div.product_price.mt16 > h4 > div"
    if type == "image":
        return "#mainSlider > div > div.owl-stage-outer > div > div > div > div > img"
    if type == "brand":
        return "#product_details > form > div > div.product_price.mt16 > h4 > div > span:nth-child(2)"

