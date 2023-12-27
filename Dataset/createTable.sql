CREATE TABLE `User` (
	`user_id`	INT	NOT NULL,
	`user_name`	VARCHAR(10)	NOT NULL,
	`nickname`	VARCHAR(20)	NOT NULL,
	`review_num`	INT	NOT NULL,
	`rating_average`	DOUBLE	NOT NULL
);

CREATE TABLE `Address` (
	`address_id`	INT	NOT NULL,
	`address_name`	VARCHAR(10)	NULL,
	`address`	VARCHAR(80)	NOT NULL,
	`user_id`	INT	NOT NULL,
	`isCurrentAddress`	TINYINT(1)	NOT NULL,
	`address_code`	INT	NOT NULL
);

CREATE TABLE `Order` (
	`order_id`	INT	NOT NULL,
	`order_datetime`	TIMESTAMP	NOT NULL,
	`order_status`	VARCHAR(20)	NOT NULL,
	`payment_info`	VARCHAR(80)	NOT NULL,
	`request_notes`	VARCHAR(50)	NULL,
	`user_id`	INT	NOT NULL,
	`store_id`	INT	NOT NULL
);

CREATE TABLE `Menu` (
	`menu_id`	INT	NOT NULL,
	`menu_name`	VARCHAR(20)	NOT NULL,
	`price`	INT	NOT NULL,
	`menu_picture_url`	TEXT	NULL,
	`store_id`	INT	NOT NULL
);

CREATE TABLE `OrderMenu` (
	`order_id`	INT	NOT NULL,
	`menu_id`	INT	NOT NULL,
	`quantity`	INT	NOT NULL
);

CREATE TABLE `Store` (
	`store_id`	INT	NOT NULL,
	`store_name`	VARCHAR(20)	NOT NULL,
	`store_address`	VARCHAR(50)	NOT NULL,
	`address_code`	INT	NOT NULL,
	`store_image`	TEXT	NOT NULL,
	`min_delivery_time`	INT	NOT NULL,
	`max_delivery_time`	INT	NOT NULL
);

CREATE TABLE `Category` (
	`category_id`	INT	NOT NULL,
	`category_name`	VARCHAR(20)	NOT NULL,
	`category_image`	TEXT	NOT NULL
);

CREATE TABLE `Like` (
	`user_id`	INT	NOT NULL,
	`store_id`	INT	NOT NULL,
	`date`	TIMESTAMP	NOT NULL
);

CREATE TABLE `DeliveryTip` (
	`delivery_tip`	INT	NOT NULL,
	`store_id`	INT	NOT NULL,
	`minimum_order`	INT	NOT NULL,
	`maximum_order`	INT	NULL
);

CREATE TABLE `Coupon` (
	`coupon_id`	INT	NOT NULL,
	`user_id`	INT	NOT NULL,
	`store_id`	INT	NOT NULL,
	`coupon_name`	VARCHAR(50)	NOT NULL,
	`discount`	INT	NOT NULL,
	`isRatio`	TINYINT(1)	NOT NULL,
	`order_id`	INT	NULL
);

CREATE TABLE `Review` (
	`user_id`	INT	NOT NULL,
	`store_id`	INT	NOT NULL,
	`rating`	INT	NOT NULL,
	`review`	TEXT	NULL,
	`review_picture_url`	TEXT	NULL,
	`review_datetime`	TIMESTAMP	NOT NULL,
	`isLocked`	TINYINT(1)	NOT NULL,
	`order_id`	INT	NOT NULL
);

CREATE TABLE `Delivery` (
	`delivery_id`	INT	NOT NULL,
	`delivery_start_time`	TIMESTAMP	NOT NULL,
	`delivery_end_time`	TIMESTAMP	NULL,
	`user_id`	INT	NOT NULL,
	`order_id`	INT	NOT NULL,
	`delivery_expect_time`	INT	NOT NULL,
	`delievery_tip`	INT	NOT NULL,
	`store_id`	INT	NOT NULL
);

CREATE TABLE `StoreCategory` (
	`store_id`	INT	NOT NULL,
	`category_id`	INT	NOT NULL
);

ALTER TABLE `User` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
	`user_id`
);

ALTER TABLE `Address` ADD CONSTRAINT `PK_ADDRESS` PRIMARY KEY (
	`address_id`
);

ALTER TABLE `Order` ADD CONSTRAINT `PK_ORDER` PRIMARY KEY (
	`order_id`
);

ALTER TABLE `Menu` ADD CONSTRAINT `PK_MENU` PRIMARY KEY (
	`menu_id`
);

ALTER TABLE `OrderMenu` ADD CONSTRAINT `PK_ORDERMENU` PRIMARY KEY (
	`order_id`,
	`menu_id`
);

ALTER TABLE `Store` ADD CONSTRAINT `PK_STORE` PRIMARY KEY (
	`store_id`
);

ALTER TABLE `Category` ADD CONSTRAINT `PK_CATEGORY` PRIMARY KEY (
	`category_id`
);

ALTER TABLE `Like` ADD CONSTRAINT `PK_LIKE` PRIMARY KEY (
	`user_id`,
	`store_id`
);

ALTER TABLE `DeliveryTip` ADD CONSTRAINT `PK_DELIVERYTIP` PRIMARY KEY (
	`delivery_tip`,
	`store_id`
);

ALTER TABLE `Coupon` ADD CONSTRAINT `PK_COUPON` PRIMARY KEY (
	`coupon_id`,
	`user_id`,
	`store_id`
);

ALTER TABLE `Review` ADD CONSTRAINT `PK_REVIEW` PRIMARY KEY (
	`user_id`,
	`store_id`
);

ALTER TABLE `Delivery` ADD CONSTRAINT `PK_DELIVERY` PRIMARY KEY (
	`delivery_id`
);

ALTER TABLE `StoreCategory` ADD CONSTRAINT `PK_STORECATEGORY` PRIMARY KEY (
	`store_id`,
	`category_id`
);

ALTER TABLE `OrderMenu` ADD CONSTRAINT `FK_Order_TO_OrderMenu_1` FOREIGN KEY (
	`order_id`
)
REFERENCES `Order` (
	`order_id`
);

ALTER TABLE `OrderMenu` ADD CONSTRAINT `FK_Menu_TO_OrderMenu_1` FOREIGN KEY (
	`menu_id`
)
REFERENCES `Menu` (
	`menu_id`
);

ALTER TABLE `Like` ADD CONSTRAINT `FK_User_TO_Like_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`user_id`
);

ALTER TABLE `Like` ADD CONSTRAINT `FK_Store_TO_Like_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`store_id`
);

ALTER TABLE `DeliveryTip` ADD CONSTRAINT `FK_Store_TO_DeliveryTip_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`store_id`
);

ALTER TABLE `Coupon` ADD CONSTRAINT `FK_User_TO_Coupon_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`user_id`
);

ALTER TABLE `Coupon` ADD CONSTRAINT `FK_Store_TO_Coupon_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`store_id`
);

ALTER TABLE `Review` ADD CONSTRAINT `FK_User_TO_Review_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`user_id`
);

ALTER TABLE `Review` ADD CONSTRAINT `FK_Store_TO_Review_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`store_id`
);

ALTER TABLE `StoreCategory` ADD CONSTRAINT `FK_Store_TO_StoreCategory_1` FOREIGN KEY (
	`store_id`
)
REFERENCES `Store` (
	`store_id`
);

ALTER TABLE `StoreCategory` ADD CONSTRAINT `FK_Category_TO_StoreCategory_1` FOREIGN KEY (
	`category_id`
)
REFERENCES `Category` (
	`category_id`
);

