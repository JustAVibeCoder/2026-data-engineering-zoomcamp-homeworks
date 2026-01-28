terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = "./my-creds.json"
  project     = "dtc-de-course-485005"
  region      = "uk-west"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "demo-bucket03211"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}