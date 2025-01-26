provider "mongodbatlas" {
  public_key  = var.atlas_api_username
  private_key = var.atlas_api_key
}

provider "databricks" {
  host = var.databricks_host
  token = var.databricks_token
}

# Create a MongoDB Atlas Project
resource "mongodbatlas_project" "atlas-project" {
  org_id = var.atlas_org_id
  name   = var.atlas_project_name
}

# Create Databricks Cluster for LlamaIndex
resource "databricks_cluster" "llamaindex_cluster" {
  cluster_name            = "llamaindex-cluster"
  spark_version           = var.databricks_spark_version
  node_type_id            = var.databricks_node_type
  autotermination_minutes = var.databricks_autotermination_minutes

  libraries {
    pypi {
      package = "llama-index"  # This installs LlamaIndex from PyPI to your cluster
    }
  }

  spark_conf = {
    "spark.databricks.library.installTimeout" = "600s"
  }
}

# IP Whitelist for MongoDB Atlas
resource "mongodbatlas_project_ip_access_list" "ip" {
  project_id = mongodbatlas_project.atlas-project.id
  ip_address = var.ip_address
}

# MongoDB Atlas Advanced Cluster
resource "mongodbatlas_advanced_cluster" "atlas-cluster" {
  project_id        = mongodbatlas_project.atlas-project.id
  name              = "${var.atlas_project_name}-${var.environment}-cluster"
  cluster_type      = "REPLICASET"
  backup_enabled    = true
  mongo_db_major_version = var.mongodb_version
  replication_specs {
    region_configs {
      electable_specs {
        instance_size = var.cluster_instance_size_name
        node_count    = 1
      }
      analytics_specs {
        instance_size = var.cluster_instance_size_name
        node_count    = 1
      }
      priority      = 7
      provider_name = var.cloud_provider
      region_name   = var.atlas_region
    }
  }
}