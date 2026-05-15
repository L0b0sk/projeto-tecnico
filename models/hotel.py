from dataclasses import dataclass
from typing import Optional

@dataclass
class HotelResultado:

    provedor: str
    hotel: str
    url: str
    location : str
    check_in: str
    check_out: str
    preco_noite: float
    total_preco: float
    moeda: str
    data_scarping: str
    limpeza: Optional[float] = None
    outras_taxas: Optional[float] = None
    nota_hotel: Optional[float] = None
    num_avaliacoes: Optional[int] = None
    politica_cancelamento: Optional[str] = None
    
    