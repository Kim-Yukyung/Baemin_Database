from flask import Flask, request
import pandas as pd
import pymysql

app = Flask(__name__)
@app.route('/likePage', methods=['POST'])

def user_query():
    request_json = request.get_json()
    userId = request_json['userId']

    conn = pymysql.connect(host='localhost', port=3306, user='root', password='0000', db='baemin')

    sql = """
    SELECT store.store_image, store.store_name, menus.menu_concat AS menu,
	    ROUND(IFNULL(review_avg.average_rating, 0), 1) average_rating,
	    COALESCE(review_avg.total_reviews, 0) AS total_reviews,
	    CONCAT( store.min_delivery_time, '분 ~ ', store.max_delivery_time, '분') delivery_time, 
	    CONCAT(
		    CASE 
			    WHEN delivery_cost.min_tip = delivery_cost.max_tip 
			    THEN CONCAT(delivery_cost.min_tip, '원')
			    ELSE CONCAT(delivery_cost.min_tip, '원 ~ ', delivery_cost.max_tip, '원')
		    END) AS delivery_tip,
	    CONCAT(delivery_cost.min_order, '원') minimum_order
    FROM baemin.like
    RIGHT JOIN store ON store.store_id = baemin.like.store_id
    JOIN deliveryTip ON store.store_id = deliveryTip.store_id
    LEFT JOIN (
        SELECT store_id, AVG(rating) AS average_rating,
            COUNT(*) AS total_reviews
            FROM Review
            GROUP BY store_id) 
        AS review_avg ON review_avg.store_id = store.store_id
    JOIN (
        SELECT store.store_id, 
            SUBSTRING_INDEX(GROUP_CONCAT(menu.menu_name ORDER BY menu.menu_id), ',', 2) as menu_concat
        from menu
        join store on menu.store_id = store.store_id
        group by store.store_id) 
    AS menus ON menus.store_id = store.store_id
    JOIN (
        select store_id, min(minimum_order) min_order,
        min(delievery_tip) min_tip, max(delievery_tip) max_tip from deliveryTip group by store_id)
    AS delivery_cost ON store.store_id = delivery_cost.store_id
    WHERE baemin.like.user_id = %s;    
    """ % userId
    df = pd.read_sql_query(sql, conn)
    
    rows_list = []
    for index, row in df.iterrows():
        row_dict = {
            "store_image": row['store_image'],
            "store_name": row['store_name'],
            "menu": row['menu'],
            "average_rating": row['average_rating'],
            "total_reviews": row['total_reviews'],
            "delivery_time": row['delivery_time'],
            "delivery_tip": row['delivery_tip'],
            "minimum_order": row['minimum_order']
        }
        rows_list.append(row_dict)

    return rows_list

if __name__ == "__main__":
    app.run()
