from tweetsent import create_app, db
from tweetsent.models import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}