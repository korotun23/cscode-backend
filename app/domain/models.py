from dataclasses import dataclass

@dataclass
class BarcodeType:
    encodeType: str
    height: float
    width: float
    showValue: bool

@dataclass
class BarcodePreview:
    barcodeType: BarcodeType
    data: str

@dataclass
class DatabaseFile:
    id: str
    path: str