module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.1"

  name = "eks-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-north-1a", "eu-north-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24"]

  enable_dns_support   = true
  enable_dns_hostnames = true
  enable_nat_gateway   = true
  single_nat_gateway   = true


  public_subnet_tags = {
    "kubernetes.io/role/elb"                    = "1"
    "kubernetes.io/cluster/eks_deploy" = "shared"
    "kubernetes.io/cluster/eks_dev" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/eks_deploy" = "shared"
    "kubernetes.io/cluster/eks_dev" = "shared"
  }

  tags = {
    "kubernetes.io/cluster/eks_deploy" = "shared"
    "kubernetes.io/cluster/eks_dev" = "shared"
  }
}

module "eks_dev" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name    = "dev-eks"
  cluster_version = "1.32"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_cluster_creator_admin_permissions = true
  cluster_endpoint_public_access           = true

  eks_managed_node_groups = {
    gitlab = {
      desired_capacity = 1
      max_capacity     = 2
      min_capacity     = 1

      instance_types = ["t3.medium"]
	  
	  labels = {
        role = "gitlab"
	  }
    }

    jenkins = {
      desired_capacity = 1
      instance_types   = ["t3.medium"]

	  labels = {
        role = "jenkins"
	  }

    }

	jenkins_agent = {
      desired_capacity = 1
      instance_types   = ["t3.medium"]

	  labels = {
        role = "jenkins-agent"
	  }

    }


    monitoring = {
      desired_capacity = 1
      instance_types   = ["t3.medium"]

	  labels = {
        role = "monitoring"
	  }

    }

    argocd = {
      desired_capacity = 1
      instance_types   = ["t3.medium"]

	  labels = {
        role = "argocd"
	  }

    }
  }
  tags = {
    environment = "dev-eks-terraform"
    Terraform   = "true"
  }

}



module "eks_deploy" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name    = "weather-app-deploy"
  cluster_version = "1.32"

  subnet_ids = module.vpc.private_subnets
  vpc_id     = module.vpc.vpc_id

  enable_cluster_creator_admin_permissions = true
  cluster_endpoint_public_access           = true



  eks_managed_node_groups = {
    staging = {
      desired_size = 2
      min_size     = 1
      max_size     = 2

      instance_types = ["t3.micro"]

      labels = {
        environment = "staging"
      }

    }

    prod = {
      desired_size = 2
      min_size     = 1
      max_size     = 2

      instance_types = ["t3.micro"]

      labels = {
        environment = "prod"
      }

    }
  }
  tags = {
    environment = "deploy-eks-terraform"
    Terraform   = "true"
  }
}

