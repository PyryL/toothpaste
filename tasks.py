from invoke import task

@task
def start(ctx):
    ctx.run("flask run", pty=True)

@task
def lint(ctx):
    ctx.run("pylint repositories/ routes/ utilities/ app.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest tests/", pty=True)
