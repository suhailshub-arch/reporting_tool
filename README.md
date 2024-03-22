# Docker

## Prerequisites

Docker, Docker compose

## Deployment

### 1. Clone repository

``` 
git clone https://github.com/suhailshub-arch/reporting_tool
cd reporting_tool
```

### 2. Customize configurations in reporting_tool/congig/configs.py

### 3. Create .env fiie in reporting_tool/

### 4. Copy contents of .env.template to .env and fill in the required fields. Delete any fields not filled

### 5. Build environment

```
docker compose build --build-arg TARGETARCH=amd64
docker compose up
```

### 6. Go to http://127.0.0.1

### 7. Login with default credentials or the user credentials configured in the configuration file

```
default = admin/adminpassword
```

### 8. Create a customer

### 9. Create a report