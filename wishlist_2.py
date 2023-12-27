from flask import Flask, request
import pandas as pd
import pymysql

app = Flask(__name__)
@app.route('/like', methods=['POST'])

def user_query():
    request_json = request.get_json()
    userIdx = request_json['userIdx']
    storeIdx = request_json['storeIdx']
    
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='0000', db='baemin')
  
    sql = """
           SELECT 
            (SELECT EXISTS(
                SELECT * FROM user WHERE user_id = %s)) AND 
            (SELECT EXISTS(
                SELECT * FROM store WHERE store_id = %s))
            AS isExist;
    """ %(userIdx, storeIdx)
    
    isExist = pd.read_sql_query(sql, conn)['isExist'].tolist()[0]
    print(isExist)

    if isExist:
        sql = """
            SELECT exists (
                SELECT * from baemin.like
                WHERE baemin.like.user_id = %s
                    AND baemin.like.store_id = %s)
                AS isLike;
            """ %(userIdx, storeIdx)
        
        isLike = pd.read_sql_query(sql, conn)['isLike'].tolist()[0]

        if isLike:
            sql = """
                DELETE FROM baemin.like WHERE user_id = %s AND store_id = %s
            """ %(userIdx, storeIdx)
            conn.cursor().execute(sql)
            conn.commit()

            return 'Remove from Like'
            
        else:
            sql = """
                INSERT INTO baemin.LIKE values (%s, %s, now());
            """ %(userIdx, storeIdx)
            conn.cursor().execute(sql)
            conn.commit()

            return 'Add to Likd'
        
    else:
        return 'User or store does not exist'

if __name__ == "__main__":
    app.run()
