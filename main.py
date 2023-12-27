from flask import Flask, request
import pandas as pd
import pymysql

app = Flask(__name__)

@app.route('/mainPage', methods=['POST'])
def user_query():
    request_json = request.get_json()
    userId = request_json['userId']
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='0000', db='baemin')
    
    sql = """
    SELECT u.user_id, u.user_name, a.address
    FROM user u
    JOIN address a ON u.user_id = a.user_id
    WHERE u.user_id = %s AND isCurrentAddress = 1;
    """ % userId
    
    df1 = pd.read_sql_query(sql, conn)
    
    sql2 = """
    SELECT c.category_image, c.category_name
    FROM category c LIMIT 10;
    """
    
    df2 = pd.read_sql_query(sql2, conn)
    
    df_dict = {
        "address": df1['address'].tolist(),
        "category_image": df2['category_image'].tolist(),
        "category_name": df2['category_name'].tolist()
    }
    
    return df_dict

if __name__ == "__main__":
    app.run()
