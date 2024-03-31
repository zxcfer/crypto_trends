select body_text from pages where site_domain = 'zombieharbor.com';
select * from page where site_domain = 'zombieharbor.com';
select * from pages where domain_authority is not null;

select id, name, total, total_parsed, status, in_hist, updated_at from website 
where name in ('ipressmedia.com') order by total_parsed desc;

select * from website;
select total from website;
select count(id), status from website group by status;

select * from stats order by count_date desc;
select * from website where name in ('rechargefoods.com');

insert into stats (count_date, total, type)
select date_sub(curdate(), INTERVAL 1 DAY) as count_date, count(*) as total, 'page' from page where parsed_at between timestamp(DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY)) and timestamp(CURRENT_DATE);
insert into stats (count_date, total, type)
select date_sub(curdate(), INTERVAL 1 DAY) as count_date, count(*) as total, 'website' from website where ended_at between timestamp(DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY)) and timestamp(CURRENT_DATE);

insert into stats (count_date, total, type)
select '2021-02-18', count(*) as total, 'page' from page where parsed_at between '2021-02-18 00:00:00' and '2021-02-19 00:00:00';
insert into stats (count_date, total, type)
select '2021-02-18', count(*) as total, 'website' from website where ended_at between '2021-02-18 00:00:00' and '2021-02-19 00:00:00';

select count(*) from website where ended_at between '2021-02-16 00:00:00' and '2021-02-17 00:00:00';
select website_id, count(*) as total from page group by website_id order by website_id;


-- update website set status = 3 where id in (select site_id from existing_domains);
-- update website set status = 1 where status in (0)4;
-- update website set status = 4 where id >1;
-- update website set status = 1 where id = 36961;

select website_id, count(website_id) as total 
from page where 
  in_hist = 0 and 
  parsed_at > subdate(current_date, 1)
group by website_id 
order by total desc;

select * from website where status = 3;
select subdate(current_date, 1);
update website set total_pages = total where id = website_id

select * from sites where domain_authority > 70 order by domain; 
select * from website where name = 'pollingersocial.co.uk';
select * from page where domain = 'pollingersocial.co.uk';
select * from page where website_id = 61493;

https://pollingersocial.co.uk/social-media-training/

select status, count(id) as total from website group by status;
-- 1, 2 => 0
select * from pages where website_id = 199;
select id, url from page where domain = 'blog.punchao.com' order by url;
select id, url from pages where site_domain = 'blog.punchao.com' order by url;

select count(*) from page where in_hist = 0;
select count(*) from page where in_hist = 1;
delete from page where in_hist = 0;

SHOW INDEX FROM page;
CREATE INDEX page_domain_idx ON page(`domain`);

select count(*) from existing_domains where site_id is not null;
select count(*) from existing_domains;
select * from existing_domains;

-- mysqldump -h $HOST -u $USER -p $DATABASE > ~/tmp/rowedigital_crawlerdb.bkp.sql
update website set status = 1 where id = 999999;
update page set parsed_at = '2035-12-24 00:00:00' where website_id = 999999 and is_home = 0;
select count(*) from page where website_id is null;

insert into website (name, created_at, updated_at, root_url, status, max_urls, nav_extracted_at, main_crawl_id)
(select `domain`, NOW(), NOW(), concat('http://', `domain`), 1, 1000, '2035-12-24 00:00:00', 1 from sites 
 where domain_authority < 70
   and `domain` not in (select `domain` from website));

select count(*) from sites where domain_authority < 70;

--delete from website where name not in (select `domain` from sites);
--DELETE FROM website WHERE name NOT IN (SELECT `domain` from sites where domain_authority < 70);

select `domain`, count(*) as total from website group by `domain`;

select count(*) from sites;
select count(*) from website;

insert into website (name, created_at, updated_at, root_url, status, max_urls, nav_extracted_at, main_crawl_id) 
values ('art-photography-schools.com', now(), now(), 'http://art-photography-schools.com', 1, 1000, '2035-12-24 00:00:00', 1);
INSERT INTO website (id, name, root_url, status, created_at, updated_at, max_urls, domain, 
nav, nav_extracted_at, main_crawl_id) VALUES (999999, 'blog.punchao.com', 'https://blog.punchao.com/', 
2, NOW(), NOW(), 1000, 'blog.punchao.com', NULL, '2035-12-24 00:00:00', 1);

select count(*) from website where status = 2;

--echo "delete from website where name not in (select `domain` from sites);" | mysql -h $HOST -u $USER -p%O7SsIt7-\&C\! $DATABASE
--echo "insert into website (name, created_at, updated_at, root_url, status, max_urls, nav_extracted_at, main_crawl_id) (select `domain`, NOW(), NOW(), concat('http://', `domain`), 1, 1000, '2035-12-24 00:00:00', 1 from sites where domain_authority < 70 and `domain` not in (select distinct `domain` from website));" | mysql -h $HOST -u $USER -p%O7SsIt7-\&C\! $DATABASE

UPDATE page
INNER JOIN website_crawl wc ON page.website_crawl_id = wc.id and wc.website_id >= 1000 and wc.website_id < 1000000
SET page.website_id = wc.website_id;

UPDATE website w
INNER JOIN sites s ON w.name = s.`domain`
SET w.id = s.id;

update pages p INNER JOIN sites s ON p.site_id = s.id and p.site_id is not null
set p.domain_authority=s.domain_authority, 
  p.page_authority=s.page_authority, p.spam_score=s.spam_score, p.trust_flow=s.trust_flow, p.citation_flow=s.citation_flow, p.traffic=s.traffic
where p.domain_authority is null;

select * from sites;
describe sites;
 

select website_id where (
select count(id) as total, website_id from page group by website_id)
total = 1000 and s;

select count(*) from pages where domain_authority is null;
select * from pages where domain_authority is null;
select count(*) from pages where site_id is null;

UPDATE pages p
INNER JOIN sites s ON p.site_domain = s.`domain`
SET p.site_id = s.id
where p.site_id is null;

select * from pages;