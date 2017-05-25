import os
from flask import Flask
from flask_restful import Api

from components.server.api_conv_user import wrapApiConvUser
from components.repo.companyRepo import CompanyRepo
from components.store.cache import Cache

app = Flask(__name__)
api = Api(app)


filename = 'components/data/companies.csv' #conversation_seeder
relative_path_file = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
cachedata = Cache(relative_path_file)
compRepo = CompanyRepo(cachedata)

app.register_blueprint(wrapApiConvUser(compRepo))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)