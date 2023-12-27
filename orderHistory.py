from flask import Flask, request
import pandas as pd
import pymysql

app = Flask(__name__)
@app.route('/orderListPage', methods=['POST'])

def user_query():
    request_json = request.get_json()
    userId = request_json['userId']

    conn = pymysql.connect(host='localhost', port=3306, user='root', password='0000', db='baemin')
  
    sql = """
    SELECT 
        CONCAT(DATE_FORMAT(baemin.order.order_datetime, '%%m월 %%d일'), ' (',
        CASE 
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 1 THEN '일'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 2 THEN '월'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 3 THEN '화'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 4 THEN '수'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 5 THEN '목'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 6 THEN '금'
            WHEN DAYOFWEEK(baemin.order.order_datetime) = 7 THEN '토'
            ELSE '' 
        END, ')') AS formatted_datetime,
        baemin.order.order_status,
        store.store_name, store.store_image,
        IF(
            COUNT(menu.menu_id) > 1, 
            CONCAT((SELECT menu_name FROM menu WHERE menu_id = MIN(ordermenu.menu_id)), 
                ' 외 ', COUNT(menu.menu_id) - 1, '개'), 
            CONCAT((GROUP_CONCAT(menu.menu_name ORDER BY menu.menu_id SEPARATOR ', ')), ' 1개')
        ) AS menu,
        CAST(totalPrices.total_price AS UNSIGNED) AS total_price,
        CAST(totalPrices.discount_price AS UNSIGNED) AS discount_price
    FROM baemin.order
    LEFT JOIN ordermenu ON baemin.order.order_id = ordermenu.order_id
    LEFT JOIN menu ON ordermenu.menu_id = menu.menu_id
    LEFT JOIN store ON menu.store_id = store.store_id
    LEFT JOIN coupon ON baemin.order.order_id = coupon.order_id
    LEFT JOIN delivery ON baemin.order.order_id = delivery.order_id
    LEFT JOIN (
        SELECT order_summary.order_id,
            CASE
                WHEN coupon_price.order_id IS NOT NULL AND coupon_price.isRatio = 0 
                    THEN coupon_price.coupon_info
                WHEN coupon_price.order_id IS NOT NULL AND coupon_price.isRatio = 1 
                    THEN total_menu_price * (coupon_price.coupon_info/100)
                ELSE NULL
            END AS discount_price,
            order_summary.total_menu_price + delivery.delievery_tip - 
            CASE
                WHEN coupon_price.order_id IS NOT NULL AND coupon_price.isRatio = 0 
                    THEN coupon_price.coupon_info
                WHEN coupon_price.order_id IS NOT NULL AND coupon_price.isRatio = 1 
                    THEN total_menu_price * (coupon_price.coupon_info/100)
                ELSE 0 
            END AS total_price
        FROM (
            SELECT 
                baemin.order.order_id,
                SUM(menu.price * ordermenu.quantity) AS total_menu_price
            FROM baemin.order 
            LEFT JOIN ordermenu ON baemin.order.order_id = ordermenu.order_id
            LEFT JOIN menu ON ordermenu.menu_id = menu.menu_id
            GROUP BY baemin.order.order_id
        ) AS order_summary
        LEFT JOIN (
            SELECT 
                baemin.order.order_id, coupon.isRatio,
                coupon.discount AS coupon_info
            FROM baemin.order 
            LEFT JOIN coupon ON baemin.order.order_id = coupon.order_id
        ) AS coupon_price ON coupon_price.order_id = order_summary.order_id
        LEFT JOIN delivery ON order_summary.order_id = delivery.order_id
    ) AS totalPrices ON totalPrices.order_id = baemin.order.order_id
    WHERE baemin.order.user_id = %s
    GROUP BY baemin.order.order_datetime, baemin.order.order_status, 
        store.store_name, store.store_image, totalPrices.total_price, totalPrices.discount_price;
    """ % userId
    df = pd.read_sql_query(sql, conn)
    
    rows_list = []
    for index, row in df.iterrows():
        row_dict = {
            "formatted_datetime": row['formatted_datetime'],
            "order_status": row['order_status'],
            "store_name": row['store_name'],
            "store_image": row['store_image'],
            "menu": row['menu'],
            "total_price": row['total_price'],
            "discount_price": row['discount_price']
        }
        rows_list.append(row_dict)

    return rows_list

if __name__ == "__main__":
    app.run()
