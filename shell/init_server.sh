#!/usr/bin/env bash
echo 'STARTING SERVER INSTALLATION ...'
echo 'current filesystem data....'
df -h
echo 'current filesystem data.... DONE'

## install dependencies (nginx, uwsgi, flask, python, pip, emacs)
echo 'install init ubuntu server dependencies ...'
sudo apt -y update
sudo apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt -y update
sudo apt install -y emacs
sudo apt install -y nginx

## install python3.9 from source code (required on ubuntu16 & ubuntu18)
sudo apt install wget build-essential checkinstall
sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
cd /opt
sudo wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
tar xzf Python-3.9.6.tgz
cd Python-3.9.6
sudo ./configure --enable-optimizations
sudo make altinstall
python3.9 -V
sudo rm -f /opt/Python-3.9.6.tgz

## install python3.9 using apt-get (doesn't work on ubuntu16; python3.9-dev seems required on ubuntu20)
#sudo apt install -y python3.9-dev
#sudo apt install -y python3.9 python3.9-distutils # might come in handy when installing packages with pip
    # *IMPORTANT* NOTE: apparently includes uwsgi plugin fro python3.9
    #ref: https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html

## bind python3.9 to 'python3'
sudo rm /usr/bin/python3
sudo ln -sf /usr/bin/python3.9 /usr/bin/python3
sudo rm /usr/local/bin/python3
sudo ln -sf /usr/local/bin/python3.9 /usr/local/bin/python3

## install remaining python dependencies
sudo apt install -y python3-pip
python3 -m pip install --upgrade pip
python3 -m pip uninstall uwsgi                # handles python3.8 bind issue
python3 -m pip install --no-cache-dir uwsgi   # handles python3.8 bind issue
python3 -m pip install flask
    ## NOT USED YET (may not be needed anymore with ubuntu20.04.3
    #sudo apt-get install uwsgi
    #sudo apt-get install uwsgi-plugins-all
    #sudo apt-get install uwsgi-extra
echo 'install init ubuntu server dependencies ... DONE'

## clone project git repo and set up environmentals
echo 'clone project git repo and set up environmentals ...'
sudo mkdir /srv/www
cd /srv/www
git clone https://{username}:{key}@github.com/{username}/{project}.git
cd /srv/www/{project}/
#git checkout www
mkdir /srv/www/{project}/logs
cd /srv/www/{project}/src
git clone https://github.com/{username}/house_tools.git
cd /srv/www/{project}/src/sites
touch .env  # create file with vars below
    #DB_HOST=localhost
    #DB_DATABASE={project}
    #DB_USERNAME=scrape
    #DB_PASSWORD=password
    #ACCESS_KEY=xxxxxxxxxxxxxxxxxxxx
    #SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
echo 'clone project git repo and set up environmentals ... DONE (note: .env manual setup req)'

## install python dependencies (read_env, boto3, mysql)
echo 'install python dependencies ...'
python3 -m pip install read_env
python3 -m pip install boto3
sudo apt install -y mysql-server
python3 -m pip install PyMySQL
python3 -m pip install cryptography
python3 -m pip install PyMuPDF
python3 -m pip install cffi       # apparent requirement on ubuntu
python3 -m pip install pytz
python3 -m pip install lxml
python3 -m pip install selenium
python3 -m pip install webdriver_manager
python3 -m pip install pandas
python3 -m pip install python-barcode
python3 -m pip install fpdf # installation
python3 -m pip install pdf2image
python3 -m pip install pillow
python3 -m pip install poppler-utils
sudo apt-get install poppler-utils
echo 'install python dependencies ... DONE'

## set up nginx config & restart nginx
echo 'set up nginx config & restart nginx ...'
cp /srv/www/{project}/src/_backups/nginx/gmsservgasp_102321_0146 /etc/nginx/sites-available/gmsservgasp
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/gmsservgasp
sudo nginx -s stop
sudo nginx
echo 'set up nginx config & restart nginx ... DONE'

## deploy server for inital endpoint testing
##   "http://3.16.26.237:50040/{project}/api/request"
#echo 'deploy server for inital endpoint testing'
#cd /srv/www/{project}/src
#sudo uwsgi --enable-threads --ini deploy.ini

#=====================================#
# google drive asset support
#=====================================#
## get equibase pdf assets from google drive
#ref: https://github.com/wkentaro/gdown/issues/148#issuecomment-1042976792
echo 'get equibase pdf assets from google drive ... DISABLED'
#python3 -m pip install gdown
#python3 -m pip install --upgrade --no-cache-dir gdown
#sudo apt install -y unzip
#sudo mkdir /srv/assets
#cd /srv/assets
#cp /srv/www/{project}/get_assets.sh .
#chmod +x get_assets.sh
#./get_assets.sh
echo 'get equibase pdf assets from google drive ... DONE'

## in seperate terminal provides filesystem data
echo 'current filesystem data....'
df -h
echo 'current filesystem data.... DONE'

## set mysql accounts & create database with .sql schema
echo 'set mysql accounts & create database with .sql schema manually.... '
each "cd /srv/www/{project}/design/database/schemas\
mysql -uroot\
    mysql> CREATE USER 'house'@'%' IDENTIFIED BY 'password';\
    mysql> CREATE USER 'dev'@'127.0.0.1' IDENTIFIED BY 'password';\
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'house'@'%' with grant option;\
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'dev'@'127.0.0.1';\
    mysql> FLUSH PRIVILEGES;\
    mysql> exit\
cd /srv/www/{project}/design/database/schemas   # *IMPORTANT*\
mysql -u house -p\
    mysql> create database {project};\
    mysql> use {project};\
    mysql> source ./gtires_db_part2_schema.sql\
    mysql> source ./gtires_func_part2_schema.sql\
    mysql> source ./gtires_proc_part2_schema.sql\
    mysql> exit"
echo 'set mysql accounts & create database with .sql schema manually.... DONE'

echo 'COMPLETED SERVER INSTALLATION ... DONE'
