sql='''
create table `match` (
id int auto_increment primary key,
match_id varchar(50),
match_date varchar(50),
match_xuhao varchar(50),
league varchar(50),
home varchar(255),
guest varchar(255),
half_scorce varchar(255),
all_scorce varchar(255)
);

create table  detail (
id int auto_increment primary key,
match_id varchar(50),
rangqiu varchar(50)
);


'''