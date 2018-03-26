CREATE TABLE IF NOT EXISTS users (
  user_id       VARCHAR(12)	UNIQUE	NOT NULL,
  user_pw		VARCHAR(25)			NOT NULL,
  fname         TEXT				NOT NULL,
  lname         TEXT				NOT NULL,
  lv1_correct   INT,
  lv1_total     INT,
  lv2_correct   INT,
  lv2_total     INT,
  lv3_correct 	INT,
  lv3_total		INT
);
