# GitOps CI/CD Project with Argo CD, Terraform, Jenkins, and GitLab

## Overview

This project demonstrates how I built a full GitOps-driven CI/CD pipeline to deploy a Python-based weather app across **staging** and **production** environments, using:

- **Terraform** for provisioning infrastructure (EKS and VPC and Argo CD)
- **Argo CD** for continuous deployment using the **App of Apps** pattern
- **Helm** for packaging and managing Kubernetes applications
- **Jenkins** for continuous integration and pipeline execution
- **GitLab** (self-hosted) for source control and GitOps manifests
- **Docker** for containerization
- **EKS (3 clusters)**: one for CI/CD tools (GitLab, Jenkins, Argo CD) and two for apps (staging and prod)

---

## Architecture

- **Management Cluster**:
  - Hosts Argo CD, GitLab (self-hosted), and Jenkins.
  - Argo CD is bootstrapped with an App of Apps that deploys GitLab and Jenkins.
  
- **Staging & Production Clusters**:
  - Each runs a separate instance of the weather app using the same Helm chart with different values.

- **Repository Flow**:
  - Initial bootstrap App of Apps and Helm charts are stored in `gitlab.com` (external).
  - After self-hosted GitLab is deployed, the weather app and environment-specific Application manifests are moved to internal GitLab repos.

---

## Tools Used

| Tool       | Purpose                                 |
|------------|------------------------------------------|
| Terraform  | Infrastructure provisioning (EKS, Argo) |
| Argo CD    | GitOps deployment controller             |
| Helm       | Package Kubernetes manifests             |
| Jenkins    | Build & test pipelines                   |
| GitLab     | SCM and GitOps repos                     |
| Docker     | Image building and app packaging         |
| EKS        | Hosting all workloads                    |

---

## CI/CD Flow

1. **Provision Infrastructure**:
   - I use Terraform to provision:
     - EKS clusters (management, staging, prod)
     - Argo CD via Helm chart

2. **Bootstrap Argo CD**:
   - Using Terraform, I deploy Argo CD into the management cluster.
   - I apply the `app-of-apps.yaml` that points to a GitLab.com repo with definitions for GitLab and Jenkins applications.

3. **Deploy GitLab and Jenkins**:
   - Argo CD deploys GitLab and Jenkins via custom Helm charts I created.
   - GitLab is exposed using an Ingress and hosts the source code repo and the GitOps repo for the weather app.

4. **Weather App Deployment**:
   - Argo CD is configured to sync two Application manifests:
     - One for **staging** (using `staging-values.yaml`)
     - One for **production** (using `prod-values.yaml`)
   - Both apps use the same Helm chart but point to different clusters and namespaces.

5. **Jenkins Pipelines**:
   - Jenkins is used for testing, static analysis, and Docker image building.
   - Successful builds push images to Docker Hub, which are then picked up by Argo CD for deployment.

## Jenkins Pipeline

I used Jenkins as it has an extensive plug-in support and it can be used for flexible and customizable pipelines using Groovy.
But the most important thing i considered for choosing Jenkins is because of how practical, hands-on and learning journey i had with Jenkins- all the configuration proccess which can be challenging, the pipeline that needs to be written imperatively and detailed. I have used GitHub Actions later and i experienced how much abstractions i have in GitHub so learning Jenskins challenged me with a big learning curve.

### Jenkinsfile Stages:

**Checkout Code**: Jenkins uses GitLab webhook triggers based on MR to fetch the latest code

**Static Code Analysis**: Trivy for dependency scanning and pylint for code standard and maintainability

**Unit and Integration Testing**: Runs tests with pytest on source code

**Build Docker Image**: Tags the image using build number, commit hash and environment (staging/prod)

**Scan Image**: Trivy to scan for vulnerabilities and CVE's in the app image

**Reachability and E2E Testing**: Running selenuim on a running instance of the app using the built image to check the app is performing

**Push to Registry**: Docker Hub

**Update Argo CD helm values**: Updating the {environment}-values.yaml in the helm chart ARGO CD follow's with the new image version.

**Notify pipeline success/fail**: Sending a message to a slack chaneel if the pipeline successed or failed with the developer name, commit & build number, and failed stage if it failed

**ARGO CD Takes control**: ARGO CD reconciles every 3 minutes to compare desired state in the Git repo and the current state in the cluster and sync's the new version - and send notification if sync was successful


---



## Future Improvements

 - Add secret management

 - Documenting Argo rollouts for rolling out in a canary deployment strategy and roll back a failed deployment

 - Add monitoring (Prometheus + Grafana) (I have implemented it in another project, i want to make it on this project, working on making it possible on tracking 3 clusters)

 - Working on documenting better the jenkins configuration and to use a dynamic agent pod

 - Implementing and Documenting saving logs using Loki
