docker run --name mysql -v mysql:/var/lib/mysql -p 3307:3306 -e MYSQL_ROOT_PASSWORD=ztesoft -d mysql
docker run --name postgres -v postgres:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=ztesoft -d postgres

alter user 'root'@'%' identified with mysql_native_password by 'ztesoft';