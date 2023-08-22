from flask import Flask, render_template, request
from langchain.chat_models import ChatOpenAI  # Adjust the import based on your actual setup
import os
from langchain.agents import *
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
import creds

os.environ['OPENAI_API_KEY'] = creds.open_ai_api_key
os.environ["SERPAPI_API_KEY"] = creds.serpapi_api_key


db_user = "personalproject"
db_password = "student"
db_host = "localhost"
db_name = "hushproject"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo")


from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit


toolkit = SQLDatabaseToolkit(db=db,llm=llm)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True )
    bot_response = agent_executor.run(user_message)
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)