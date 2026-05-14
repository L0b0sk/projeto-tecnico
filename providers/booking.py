from datetime import datetime, timezone
import asyncio
from models.hotel import HotelResultado
from utils.brower import create_browser
from utils.formatter import (
    clean_price,
    clean_text,
    clean_rating,
    clean_review_count,
    extract_currency,
    count_nights,
)

# Logger do projeto
from utils.logger import get_logger

# Cria logger para este módulo
logger = get_logger(__name__)
MAX_RETRIES = 3
RETRY_DELAY = 2
PAGE_LOAD_WAIT = 3000  # milissegundos


async def scrape_booking(url: str, check_in: str, check_out: str, adults: int) -> HotelResult:
    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"Tentativa {attempt}/{MAX_RETRIES} — Booking.com")
        
        try:
            result = await _do_scrape(url, check_in, check_out, adults)
            logger.info("Scraping concluído com sucesso!")
            return result
        
        except Exception as e:
            logger.warning(f"Tentativa {attempt} falhou: {type(e).__name__}: {e}")
            
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * (2 ** (attempt - 1))
                logger.info(f"Aguardando {wait}s antes da próxima tentativa...")
                await asyncio.sleep(wait)
                
            else:
                logger.error(f"Todas as {MAX_RETRIES} tentativas falharam para: {url}")
                raise


async def _do_scrape(url: str, check_in: str, check_out: str, adults: int) -> HotelResult:
    url_com_params = (
        f"{url}"
        f"?checkin={check_in}"
        f"&checkout={check_out}"
        f"&group_adults={adults}"
        f"&no_rooms=1"
    )

    logger.debug(f"Acessando: {url_com_params}")
    browser, page = await create_browser()

    try:
        await page.goto(url_com_params, wait_until="domcontentloaded")
        await page.wait_for_timeout(PAGE_LOAD_WAIT)
        
        
        hotel_name = ""
        try:
            hotel_name = clean_text(
                await page.locator("h2.pp-header__title").first.inner_text()
            )
        except Exception:
            try:
                hotel_name = clean_text(
                    await page.locator("h2").first.inner_text()
                )
            except Exception:
                logger.warning("Nome do hotel não encontrado")

        logger.info(f"Hotel: {hotel_name}")


        location = ""
        try:
            location = clean_text(
                await page.locator('[data-testid="address"]').first.inner_text()
            )
        except Exception:
            try:
                location = clean_text(
                    await page.locator(".hp_address_subtitle").first.inner_text()
                )
            except Exception:
                logger.warning("Localização não encontrada")


        raw_price = ""
        total_price = 0.0
        currency = "BRL"

        try:
            raw_price = await page.locator(
                '[data-testid="price-and-discounted-price"]'
            ).first.inner_text()

            total_price = clean_price(raw_price)
            currency = extract_currency(raw_price)

        except Exception:
            try:
                raw_price = await page.locator(".prco-valign__middle-helper").first.inner_text()
                total_price = clean_price(raw_price)
                currency = extract_currency(raw_price)
            except Exception:
                logger.warning("Preço não encontrado")

        logger.info(f"Preço total: {currency} {total_price}")
        noites = count_nights(check_in, check_out)
        preco_por_noite = round(total_price / noites, 2) if total_price > 0 else 0.0
        limpeza = None
        outras_taxas = None

        try:
            taxas_texto = await page.locator(
                '[data-testid="taxes-and-charges"]'
            ).first.inner_text()

            outras_taxas = clean_price(taxas_texto)
        except Exception:
            pass
        rating_hotel = None

        try:
            rating_texto = await page.locator(
                '[data-testid="review-score-component"]'
            ).first.inner_text()

            rating_hotel = clean_rating(rating_texto)
        except Exception:
            try:
                rating_texto = await page.locator(
                    ".bui-review-score__badge"
                ).first.inner_text()
                rating_hotel = clean_rating(rating_texto)
            except Exception:
                pass 

        logger.info(f"Rating: {rating_hotel}")


        num_avaliacoes = None

        try:
            avaliacoes_texto = await page.locator(
                '[data-testid="review-score-component"]'
            ).first.inner_text()

            num_avaliacoes = clean_review_count(avaliacoes_texto)
        except Exception:
            pass


        politica_cancelamento = None

        try:
            politica_cancelamento = clean_text(
                await page.locator(
                    '[data-testid="cancellation-policy"]'
                ).first.inner_text()
            )
        except Exception:
            try:
                politica_cancelamento = clean_text(
                    await page.locator(".bui-badge--constructive").first.inner_text()
                )
            except Exception:
                pass  


        data_scraping = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        result = HotelResult(
            provider="booking",
            hotel=hotel_name,
            url=url,
            location=location,
            check_in=check_in,
            check_out=check_out,
            preco_por_noite=preco_por_noite,
            total_price=total_price,
            currency=currency,
            data_scraping=data_scraping,
            limpeza=limpeza,
            outras_taxas=outras_taxas,
            rating_hotel=rating_hotel,
            num_avaliacoes=num_avaliacoes,
            politica_cancelamento=politica_cancelamento,
        )

    finally:
        await browser.close()
        logger.debug("Navegador fechado")

    return result