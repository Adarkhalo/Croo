import sys
import asyncio
from flask import request
from flask import jsonify
from flask import Flask
from package import DatabaseManager, Utility, Constant, ExceptionManager, Comment

app = Flask(__name__)  # create an app instance

database_manager = DatabaseManager.DatabaseManager(Constant.MYSQL_HOST, Constant.MYSQL_USER, Constant.MYSQL_PASSWORD,
                                                   Constant.MYSQL_DB)


@app.route('/saveComment', methods=['POST'])
def save_comment():
    data = request.json
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        user_comment = Comment.Comment(data['name'], data['email'], data['comment'])
        statement_comment = Utility.prepare_parameters_values_mysql(user_comment)
        loop.run_until_complete(
            database_manager.put(statement_comment['parameters'], 'Comments', statement_comment['values'],
                                 Constant.COMMENT_PUT, loop))
        return jsonify('Comment submitted')
    except:
        e = sys.exc_info()
        print(e)
        ExceptionManager.return_exception(Constant.COMMENT_PUT)


@app.route('/getComments', methods=['GET'])
def get_comments():

    def args_connector(args: str):
        valid_parameters = ['date', 'name', 'email']
        if args in valid_parameters:
            if args == 'date':
                args = 'inserted_on'
            return args
        else:
            ExceptionManager.return_exception(Constant.INVALID_SORT_PARAMETERS)

    try:
        sort_parameter = args_connector(request.args.get('sortby'))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        comments = loop.run_until_complete(
            database_manager.get(['*'], 'Comments', [], [], 'order by ' + sort_parameter,
                                 Constant.COMMENT_GET, loop))
        for comment in comments:
            comment['inserted_on'] = Utility.format_date(comment['inserted_on'])
        return jsonify(comments)
    except:
        e = sys.exc_info()
        print(e)
        ExceptionManager.return_exception(Constant.COMMENT_GET)


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app with debug to update changes while editing files

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
