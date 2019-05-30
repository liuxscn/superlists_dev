配置新网站
===========================


## 需要的包
	nginx
	Python3.6
	virtualenv
	pip
	git


以Ubuntu为例：
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt-get install nginx git python3.6 python3.6-venv


## Nginx虚拟主机

* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如dev.lxacn.com

## Systemd服务

* 参考gunicorn-systemd.template.service
* 把SITENAME替换成所需的域名，例如dev.lxacn.com


## 目录结构
假设有用户账户，家目录为/home/ubuntu

/home/ubuntu
	sites
		SITENAME
			database
			source
			static
			virtualenv




## 使用sed命令将NGINX配置文件中的测试环境地址替换为生产环境地址

sed "s/SITENAME/www.lxacn.com/g" sites/www.lxacn.com/source/deploy_tools/nginx.template.conf \
	| sudo tee /etc/nginx/sites-available/www.lxacn.com

sudo ln -s /etc/nginx/sites-available/www.lxacn.com /etc/nginx/sites-enabled/www.lxacn.com


## 

sed "s/SITENAME/www.lxacn.com/g" sites/www.lxacn.com/source/deploy_tools/gunicorn-systemd.template.service \
	| sudo tee /etc/systems/system/gunicorn-www.lxacn.com.service