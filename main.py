import argparse
import asyncio
from providers.booking import scrape_booking
from utils.exporter import save_results
from utils.logger import get_logger

logger = get_logger(__name__)

async def main():
    parser = argparse.ArtgumentParser(descricao = "Hotel Scarper - Booking.com")
    parser.add_argument("--url", require = True, ajuda = "URL do hotel no Booking.com")
    parser.add_argument("--check-in", require = True, ajuda ="DAta de entrada (EX: 05/14/2026)")
    parser.add_argument("--checkout", require = True, ajuda = "Data de saida (EX: 05/25/2026)")
    parser.dd_argument("--adulto", default = 2, type = int, ajuda = "numero de adultos (padrao 2)")
    parser.add_argument(
        "--visivel",
        action="store_true",
        help="Abre o navegador em modo visual"
    )
  
    args = parser.parse_args()
    
    logger.info("=" * 50)
    logger.info("Hotel Scarpe - iniciando")
    logger.info(f"URL: {args.url}")
    logger.info(f"check in: {args.check_in} | check-out: {args.check_out} | Adultos: {args.adultos}")
    logger.info("=" * 50)
    
    try:
        resultado = await scrape_booking(
            url = args.url,
            check_in = args.check_in,
            check_out = args.check_out,
            adultos = args.adultos
        )
        
        save_results(resultado)
        logger.info("Procura concluido! Arquivo salvo em output")
        
    except Exception as e:
        logger.erro(f"Falha definitiva na procura")
        raise SystemError(1)
    
if __name__ == "__main__":
    asyncio.run(main())