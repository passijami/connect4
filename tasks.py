"""Invoke-komennot projektin ajamiseen.

Käyttö:
    poetry run invoke test
    poetry run invoke coverage
    poetry run invoke lint
"""

from invoke import task


@task
def test(c):
    """Aja yksikkötestit."""
    c.run("pytest src tests", pty=True)


@task
def coverage(c):
    """Aja testit ja näytä kattavuusraportti."""
    c.run("coverage run --branch -m pytest src tests", pty=True)
    c.run("coverage report -m", pty=True)


@task
def coverage_html(c):
    """Luo html-kattavuusraportti (htmlcov/index.html)."""
    c.run("coverage run --branch -m pytest src tests", pty=True)
    c.run("coverage html", pty=True)


@task
def lint(c):
    """Aja pylint koodin laadun tarkistukseen."""
    c.run("pylint src", pty=True)


@task
def benchmark(c):
    """Vertaa karsimatonta minimaxia ja alfa-beta-hakua."""
    c.run("python benchmark.py", pty=True)
