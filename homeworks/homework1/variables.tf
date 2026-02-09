variable "credentials" {
  description = "Path to the GCP credentials JSON file"
  default = "/home/katwre/.config/gcloud/terraform/projectd-devops-91b5143ef1a3.json"
}


variable "project"{ 
  description = "Project Location"
  default     = "projectd-devops"
}

variable "region"{ 
  description = "Project Region"
  default     = "us-central1"
}


variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "projectd-devops-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
variable "location" {
  description = "Bucket Location"
  default     = "US"
}