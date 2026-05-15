from playwright.async_api import async_playwright
from utils.logger import get_logger

logger = get_logger(__name__)


async def criar_navegador(headless: bool = True):
    logger.debug("Iniciando Playwright...")
    playwright = await async_playwright().start()
    navegador = await playwright.chromium.launch(
        headless=headless,
        slow_mo=50
    )
    
    contexto = await navegador.new_context(
        viewport={"width": 1280, "height": 800},

        agente_user=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        
        local="pt-BR",
        timezone_id="America/Sao_Paulo"
    )
    pagina = await contexto.new_page()
    pagina.set_default_timeout(30_000)

    logger.debug("Navegador criado com sucesso")

    return navegador, pagina