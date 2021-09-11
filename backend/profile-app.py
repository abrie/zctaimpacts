from werkzeug.middleware.profiler import ProfilerMiddleware
import app

a = app.create_app()
a.config["PROFILE"] = True
a.wsgi_app = ProfilerMiddleware(a.wsgi_app, restrictions=[5])
a.run(debug=True)
