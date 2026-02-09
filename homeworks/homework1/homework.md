
Understanding Docker images:
```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.13
```
```bash
root@7e9d83abb9bf:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

Understanding Docker networking and docker-compose:
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
```bash
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```
hostname: db
port: 5432 (Postgres listens on 5432 inside the db container; 5433 is only the host-side mapping.)


Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?
```bash
(.venv) katwre@katwre-XPS-13-9350:~/projects/data-engineering-zoomcamp/homeworks/homework1$ /home/katwre/projects/data-engineering-zoomcamp/homeworks/homework1/.venv/bin/python -c "import pandas as pd; df=pd.read_parquet('green_tripdata_2025-11.parquet'); df=df[(df['lpep_pickup_datetime']>='2025-11-01') & (df['lpep_pickup_datetime']<'2025-12-01') & (df['trip_distance']<=1)]; print(len(df))"
8007
```

Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).
Use the pick up time for your calculations.
```bash
/home/katwre/projects/data-engineering-zoomcamp/homeworks/homework1/.venv/bin/python -c "import pandas as pd; df=pd.read_parquet('green_tripdata_2025-11.parquet'); df=df[df['trip_distance']<100]; df['pickup_day']=df['lpep_pickup_datetime'].dt.date; day=df.loc[df['trip_distance'].idxmax(),'pickup_day']; print(day)"
2025-11-14
```


Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
```bash
/home/katwre/projects/data-engineering-zoomcamp/homeworks/homework1/.venv/bin/python -c "import pandas as pd; df=pd.read_parquet('green_tripdata_2025-11.parquet'); zones=pd.read_csv('taxi_zone_lookup.csv'); df=df[(df['lpep_pickup_datetime']>='2025-11-18') & (df['lpep_pickup_datetime']<'2025-11-19')]; df=df.merge(zones, left_on='PULocationID', right_on='LocationID', how='left'); top=df.groupby('Zone', dropna=False)['total_amount'].sum().sort_values(ascending=False).head(1); print(top.index[0])"
East Harlem North
```

Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
Note: it's tip , not trip. We need the name of the zone, not the ID.
```bash
/home/katwre/projects/data-engineering-zoomcamp/homeworks/homework1/.venv/bin/python -c "import pandas as pd; df=pd.read_parquet('green_tripdata_2025-11.parquet'); zones=pd.read_csv('taxi_zone_lookup.csv'); df=df[(df['lpep_pickup_datetime']>='2025-11-01') & (df['lpep_pickup_datetime']<'2025-12-01')]; df=df.merge(zones, left_on='PULocationID', right_on='LocationID', how='left'); df=df[df['Zone']=='East Harlem North']; df=df.merge(zones, left_on='DOLocationID', right_on='LocationID', how='left', suffixes=('','_do')); top=df.groupby('Zone_do')['tip_amount'].max().sort_values(ascending=False).head(5); print(top)"
Zone_do
Yorkville West                   81.89
LaGuardia Airport                50.00
East Harlem North                45.00
Long Island City/Queens Plaza    34.25
JFK Airport                      23.53
Name: tip_amount, dtype: float64
```

or I could Ingest Data into Postgres and Insert data into PostgreSQL using SQLAlchemy
```bash
/home/katwre/projects/data-engineering-zoomcamp/homeworks/homework1/.venv/bin/pip install sqlalchemy psycopg2-binary
```
1. Run Postgres (docker-compose or docker run) so the database is reachable. Use host localhost and port 5433 from your compose setup.
2. 3. Create an ingest script that loads green_tripdata_2025-11.parquet into a table (e.g., green_tripdata) and taxi_zone_lookup.csv into a zones table.
Run your SQL queries against those tables.

[why I can run postgres only via docker-compose or docker run? -> Because you don’t have a local Postgres server running on your host. Docker is the simplest way to start one for the homework. You could also install Postgres directly on Linux and run it as a service, but that’s optional and more setup.]


```bash
mkdir ny_taxi_postgres_data

sudo docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

```bash
# Install pgcli:
uv add --dev pgcli
# Now use it to connect to Postgres:
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
# First, install SQLAlchemy:
uv add sqlalchemy psycopg2-binary
```

The script reads data in chunks (100,000 rows at a time) to handle large files efficiently without running out of memory.
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

  Run pgAdmin Container
```bash 
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

docker-compose allows us to launch multiple containers using a single configuration file, so that we don't have to run multiple complex docker run commands separately.
```bash 
docker-compose up -d
```


Running the Ingestion Script with Docker Compose
```bash
docker network ls 

docker build -t taxi_ingest:v001 .

docker run -it --rm\
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
``` 

Stop and remove volumes
```bash
docker-compose down -v
``` 


# creating terraform

Created `main.tf` to provision Google Cloud Storage bucket for the project:

```terraform
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file("/home/katwre/.config/gcloud/terraform/projectd-devops-91b5143ef1a3.json")
  project = "projectd-devops"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "projectd-devops-terraform-demo-bucket"
  location      = "US"
  force_destroy = true
  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "AbortIncompleteMultipartUpload"
    }
    condition {
      age = 3  // days
    }
  }
}
```

Initialize and apply Terraform configuration:
```bash
terraform init
terraform plan
terraform apply
```

**Note:** Initially had credentials configuration issues:
- Fixed by using `file()` function to read JSON credentials file
- Alternatively, can use `GOOGLE_APPLICATION_CREDENTIALS` environment variable instead of hardcoding credentials path in main.tf

To destroy/remove the created resources:
```bash
terraform destroy
```
This will remove all resources defined in the Terraform configuration (the GCS bucket in this case).

Created `.gitignore` file to exclude Terraform and project files from version control:
- `.terraform/` directory (plugins and modules)
- `*.tfstate` and `*.tfstate.*` files (contain sensitive state information)
- `*.tfvars` files (may contain sensitive variables)
- Python virtual environments (`.venv/`)
- Data files (`*.parquet`, `*.csv`, `*.json`)
- Docker volumes (`ny_taxi_postgres_data/`)

**Important:** Never commit `.tfstate` files to git as they may contain sensitive information like credentials and resource IDs. 


