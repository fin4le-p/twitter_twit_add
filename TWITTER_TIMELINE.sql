create table TWITTER_TIMELINE(
id varchar(20) character set utf8mb4,
user varchar(20) character set utf8mb4,
created_at datetime,
text varchar(600) character set utf8mb4,
fav int,
rt int,
twit_frg int
)CHARSET=utf8mb4;

alter table TWITTER_TIMELINE add primary key (id,user);