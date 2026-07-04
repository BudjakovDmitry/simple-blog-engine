# Simple blog engine

## Setup clean Debian 13 server

### Install pre-requirements

Login as root:

```bash
su -
```

Update packages:

```bash
apt update && apt upgrade
```

Install utils:

```bash
apt install wget curl unzip tree vim
```

Install building tools:

```bash
apt install build-essential gcc make
```

Install pre-requirements:

```bash
apt install \
    ca-certificates \
    debian-archive-keyring \
    zlib1g-dev \
    gdb \
    gnupg2 \
    lzma \
    lcov \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    libreadline-dev \
    libncurses5-dev \
    lsb-release \
    uuid-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    tk-dev \
    libzstd-dev \
    inetutils-inetd
```

### Install Nginx (for production only)

Import an official nginx signing key

```bash
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
```

Set up the apt repository for stable nginx packages:

```bash
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
https://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Set up repository pinning to prefer nginx packages over distribution-provided ones:

```bash
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx
```

Install Nginx:

```bash
apt update && apt install nginx
```

Run Nginx:

```bash
systemctl start nginx
```

### Install and prepare PostgreSQL

Install PostgreSQL

```bash
apt install postgresql
```

Login as a `postgres` user an use `psql` tool to connect to Postgres.

```bash
su - postgres
psql
```

Create role (don't forget to change password):

```sql
CREATE ROLE dmitbud WITH LOGIN PASSWORD 'MyStrongPassword';
```

Create database:

```sql
CREATE DATABASE knowledge_base
WITH
ENCODING='UTF8'
owner dmitbud;
```

Now quit from `psql`: `\q` and logout from `postgres` user: `exit`.

### Build Python from source

Download Python:

```bash
wget https://www.python.org/ftp/python/3.14.3/Python-3.14.3.tar.xz
```

Unpack:

```bash
tar xvf Python-3.14.3.tar.xz
cd Python-3.14.3
```

Build:

```bash
mkdir -p /opt/python/3.14.3
./configure --enable-optimizations --prefix=/opt/python/3.14.3
make -j$(nproc)
make altinstall
cd ..
rm -r Python-3.14.3
rm Python-3.14.3.tar.xz
```

Make symlink to PATH dir

```bash
ln -s /opt/python/3.14.3/bin/python3.14 /usr/local/bin/python
```

Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Run project

Login as a regular user. Create `code` direcotory

```bash
mkdir $HOME/code
```

Download the project

```bash
wget https://github.com/BudjakovDmitry/simple-blog/archive/refs/heads/main.zip
```

Unzip project to `code`

```bash
unzip main.zip -d $HOME/code
mv $HOME/code/simple-blog-engine-main/ $HOME/code/blog
rm main.zip
cd $HOME/code/blog
```

Create and activate virtual environment

```bash
python -m venv env
source env/bin/activate
```

Install project requirements

```bash
pip install --upgrade pip
python -m pip install -r requirements.txt
```

### For production

Login as a regular user.

Creaate environment variable DMITBUD_SECRET_KEY (don't forget to set your secret key):

```bash
export DMITBUD_SECRET_KEY=YourSecretKey
```

Create shared directories:

```bash
# static files
sudo mkdir -p /var/dmitbud/static
sudo chown -R $USER: /var/dmitbud
# secrets
sudo mkdir -p /etc/dmitbud/postgres
sudo chown -R $USER: /etc/dmitbud
```

Update secrets:

```bash
cp secrets/pgpass.example /etc/dmitbud/postgres/.pgpass
chmod 600 /etc/dmitbud/postgres/.pgpass
cp secrets/pg_service.conf /etc/dmitbud/postgres/
```

Set your own credentials to `pg_service.conf` and `.pgpass`.

```bash
make collectstatic
sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.factory
sudo cp ./deploy/nginx/dmitbud.conf /etc/nginx/conf.d/
sudo nginx -t
sudo nginx -s reload
```

