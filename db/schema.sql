CREATE TABLE IF NOT EXISTS users (
	user_id     	VARCHAR(12)	UNIQUE	NOT NULL,
	user_pw			VARCHAR(25)			NOT NULL,
	fname       	TEXT				NOT NULL,
	lname       	TEXT				NOT NULL,
	lv1_correct		INT					DEFAULT 0,
	lv1_total   	INT					DEFAULT 0,
	lv2_correct 	INT 				DEFAULT 0,
	lv2_total   	INT 				DEFAULT 0,
	lv3_correct		INT 				DEFAULT 0,
	lv3_total		INT 				DEFAULT 0
);
