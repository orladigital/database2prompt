from dataclasses import dataclass
from typing import Dict, Optional, List

@dataclass
class ColumnMetadata:
    """Metadata for a database column"""
    description: str
    business_rules: Optional[str] = None
    value_examples: Optional[List[str]] = None
    constraints: Optional[str] = None
    data_type_info: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class TableMetadata:
    """Metadata for a database table"""
    description: str
    domain: Optional[str] = None
    update_frequency: Optional[str] = None
    owner: Optional[str] = None
    tags: Optional[List[str]] = None
    columns: Dict[str, ColumnMetadata] = None

    def __post_init__(self):
        if self.columns is None:
            self.columns = {}
