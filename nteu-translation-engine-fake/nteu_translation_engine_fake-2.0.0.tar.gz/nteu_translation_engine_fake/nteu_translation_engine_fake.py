from aiohttp import web
from nteu_translation_engine_fake.translate import translate


class NTEUTranslationEngineFake:
    @staticmethod
    def run(host, port):
        app = web.Application()
        app.router.add_post(
            "/translate", translate
        )
        web.run_app(
            app,
            host=host,
            port=port,
            handle_signals=False
        )