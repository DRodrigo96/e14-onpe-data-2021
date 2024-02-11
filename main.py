# main.py
# ==================================================
# requirements
import typer
# defined
import scripts.links
import scripts.extraction
import scripts.cleaning
# --------------------------------------------------

app = typer.Typer()

@app.command()
def references() -> None:
    '''Extrae todas los links para descargar información desde
    la ONPE.
    '''
    scripts.links.retrieve_links()

@app.command()
def extraction() -> None:
    '''Usa los links del paso anterior para descargar la información.
    '''
    scripts.extraction.data_extraction()

@app.command()
def cleaning() -> None:
    '''Consolida la información descargada.
    '''
    scripts.cleaning.data_cleaning()

if __name__ == '__main__':
    app()
