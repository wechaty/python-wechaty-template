from typing import Optional
from dataclasses import dataclass

from dataclasses_json import dataclass_json



@dataclass_json
@dataclass
class NavMetadata:
    """nav metadata""" 
    view_url: Optional[str] = None
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author
