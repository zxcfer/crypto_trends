

select * from feed_item;
select * from feed;

select * from crypto_price order by created_at desc limit 200;
select count(*) from crypto_price;
select * from crypto_price order by id desc;
select * from crypto;

select * from alembic_version;

show tables;
show create table alembic_version;

select coin, sum(price)/6 as price1
from crypto_price
where 
   created_at between '2020-10-17 00:20:00' and '2020-10-17 01:20:00' 
group by coin;

select cp.coin, cp.price, cp2.price
from crypto_price cp
join crypto_price cp2 on cp.coin = cp2.coin and cp2.created_at between '2020-10-17 01:10:01' and '2020-10-17 01:20:00' 
where cp.created_at between '2020-10-17 01:00:00' and '2020-10-17 01:10:00';


select cp.coin, cp.price_btc, cp2.price_btc, cp3.price_btc, cp4.price_btc, cp5.price_btc, cp6.price_btc, cp7.price_btc
from crypto_price cp
join crypto_price cp7 on cp.coin = cp7.coin and cp7.created_at between DATE_SUB(NOW(), INTERVAL 70 MINUTE) and DATE_SUB(NOW(), INTERVAL 60 MINUTE)
join crypto_price cp6 on cp.coin = cp6.coin and cp6.created_at between DATE_SUB(NOW(), INTERVAL 60 MINUTE) and DATE_SUB(NOW(), INTERVAL 50 MINUTE)
join crypto_price cp5 on cp.coin = cp5.coin and cp5.created_at between DATE_SUB(NOW(), INTERVAL 50 MINUTE) and DATE_SUB(NOW(), INTERVAL 40 MINUTE)
join crypto_price cp4 on cp.coin = cp4.coin and cp4.created_at between DATE_SUB(NOW(), INTERVAL 40 MINUTE) and DATE_SUB(NOW(), INTERVAL 30 MINUTE)
join crypto_price cp3 on cp.coin = cp3.coin and cp3.created_at between DATE_SUB(NOW(), INTERVAL 30 MINUTE) and DATE_SUB(NOW(), INTERVAL 20 MINUTE)
join crypto_price cp2 on cp.coin = cp2.coin and cp2.created_at between DATE_SUB(NOW(), INTERVAL 20 MINUTE) and DATE_SUB(NOW(), INTERVAL 10 MINUTE)
where cp.created_at between DATE_SUB(NOW(), INTERVAL 10 MINUTE) and NOW();


select cp.coin, cp.price_btc
from crypto_price cp
where cp.created_at between DATE_SUB(NOW(), INTERVAL 10 MINUTE) and NOW();

select NOW(), DATE_SUB(NOW(), INTERVAL 10 MINUTE);

ALTER TABLE crypto_price ADD COLUMN price_btc NUMERIC(20, 8);
ALTER TABLE crypto_price ADD COLUMN price_usd NUMERIC(20, 8);
ALTER TABLE crypto_price ADD COLUMN market_cap NUMERIC(20, 8);

