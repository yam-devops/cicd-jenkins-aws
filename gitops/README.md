# GitOps Infrastructure Deployment with Terraform, Argo CD, and Helm

## Overview

This repository documents how I built a GitOps-based CI/CD system for deploying a weather application to staging and production environments across separate EKS clusters. The architecture uses:

- **Terraform** to provision the Kubernetes clusters and deploy Argo CD
- **Argo CD** (bootstrapped via Terraform) to manage all deployments using the **App of Apps** pattern
- **Helm** to package and manage Kubernetes manifests with environment-specific values
- **GitLab** (hosted within the cluster) to manage my staging and production application repositories

## Why I Use Argo CD for Weather App Deployments

It provides me to handle deployments using a single source of truth approach, and helps me to use a pull-based deployments.
All desired state for the weather app — including Kubernetes manifests, Helm charts, and environment-specific configuration — lives in Git. This provides:

- **Version control**: every change is tracked.
- **Auditability**: I know exactly what was deployed and when.
- **Rollbacks**: I can revert to a previous state with a simple Git revert, Or using Argo rollouts.
---

## Architecture Summary

- I use **three EKS clusters**:

  - One for **management** where Argo CD, GitLab, and Jenkins are deployed
  - One for **staging**
  - One for **production**

- Argo CD is deployed in the management cluster via Terraform and then bootstrapped using an **App of Apps** pattern that:

  - Deploys GitLab (self-hosted)
  - Deploys Jenkins

- Initially, my application manifests and Helm charts are stored in **GitLab.com** until GitLab is running on my infrastructure.\
  After that, I use the **self-hosted GitLab** to manage the weather app charts and environments.

---

## Repository Structure

### GitLab.com Repo (Bootstrap GitOps)

This is where I keep the manifests for the initial Argo CD applications (GitLab, Jenkins, etc.) before I have a self-hosted GitLab.

```
gitops/
├── app-of-apps.yaml                    # Argo CD Application that installs all base apps
├── dev-apps/
│   ├── gitlab-app.yaml
│   └── jenkins-app.yaml
├── helm-charts/
│   ├── gitlab/                         # My own GitLab chart that wraps the official one
│   └── jenkins/
```

### Self-Hosted GitLab Repo (Weather App)

Once GitLab is deployed in the cluster, I push this GitOps repo into it:

```
weather-app-gitops/
├── chart/                              # Helm chart for weather app
│   ├── Chart.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── prod-values.yaml
├── staging-values.yaml
├── argocd-apps/
│   ├── weather-app-prod.yaml
│   └── weather-app-staging.yaml
```
[weather app helm charts](../k8s/weather-app/)

Using a **single Helm chart** with different `values.yaml` files, Argo CD lets me:

- Reuse the same chart for both **staging** and **production**
- Apply different configurations (e.g., replicas, domains, resources) via separate `prod-values.yaml` and `staging-values.yaml` files
- Avoid drift between environments
---

## Deployment Steps

### Step 1: Provision EKS and Argo CD with Terraform

I use Terraform to:

- Create all three EKS clusters (management, staging, prod)
- Deploy Argo CD into the management cluster using the Helm provider

[argocd-provision-terraform](../terraform/argo-provision/main.tf)

---

### Step 2: Register External Clusters with Argo CD

After Argo CD is installed in the management cluster, I register the **staging** and **production** EKS clusters so Argo CD can deploy apps to them.

```bash
# Set context to Argo CD management cluster
kubectl config use-context <management-cluster-context>

# Register staging cluster
argocd cluster add <staging-cluster-context>

# Register prod cluster
argocd cluster add <prod-cluster-context>
```

This adds the external clusters to Argo CD, and I can now target them in my `Application` manifests using their API server URLs or context names.

---

### Step 3: Bootstrap Argo CD with App of Apps

To get started, I apply the `app-of-apps.yaml` stored in my GitLab.com repo. This instructs Argo CD to create applications for GitLab and Jenkins.

```bash
kubectl apply -n argocd -f app-of-apps.yaml
```

---

### Step 4: GitLab and Jenkins Are Deployed via Argo CD

Once this is synced:

- GitLab is deployed inside the cluster using my own wrapper Helm chart
- Jenkins is also deployed and ready to integrate with GitLab if needed

---

### Step 5: Push Application Repos to Self-Hosted GitLab

Now that GitLab is running inside my infrastructure, I push the weather app gitops repo (`weather-app-gitops/`) to a project inside my self-hosted GitLab.

This repo includes:

- The `chart/` directory for the app's Helm chart
- `prod-values.yaml` and `staging-values.yaml`
- The `Application` manifests Argo CD will use for staging and prod deployments

---

### Step 6: Create Argo CD Applications for Prod and Staging

Each environment has its own Argo CD `Application`, pointing to the same chart but with a different values file and destination cluster.

Argo CD watches the repo and deploys the staging and production apps to their respective clusters\
Argo CD tracks changes independently for each environment based on the chart and the specified values file

---

## Conclusion

This setup provides a full GitOps workflow with:

- **Terraform** for infrastructure provisioning and Argo CD installation
- **Argo CD** to deploy and manage all infrastructure and app components
- **Helm charts with separate values files** to deploy the same app to different environments
- A clean migration from GitLab.com to **self-hosted GitLab** as the source of truth

It allows me to scale deployments, track changes via Git, and have a fully automated and declarative CI/CD pipeline across environments.



---

## Argo Rollouts

There is also an option to deploy the application using Argo rollouts for different deployment strategies,
The advantages and usage discussed in the main README 


- install Argo Rollouts controller

```bash
kubectl create namespace argo-rollouts
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm install argo-rollouts argo/argo-rollouts   -n argo-rollouts   --set installCRDs=true
```

- install Argo Rollouts CLI

```bash
 curl -sLO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x kubectl-argo-rollouts-linux-amd64
sudo mv kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
```

then you can use commands to inspect rollouts

```bash
kubectl-argo-rollouts get rollout weather-app
kubectl-argo-rollouts abort weather-app
```

you can see something like this when a rollout fails
```bash

kubectl-argo-rollouts get rollout weather-app
Name:            weather-app
Namespace:       default
Status:          ◌ Progressing
Message:         more replicas need to be updated
Strategy:        Canary
  Step:          0/3
  SetWeight:     50
  ActualWeight:  0
Images:          nginx:1.21 (canary, stable)
Replicas:
  Desired:       2
  Current:       3
  Updated:       1
  Ready:         2
  Available:     2

NAME                                     KIND        STATUS         AGE    INFO
⟳ weather-app                            Rollout     ◌ Progressing  6m40s
├──# revision:2
│  └──⧉ weather-app-5679855949           ReplicaSet  ◌ Progressing  54s    canary
│     └──□ weather-app-5679855949-xwqgl  Pod         ✔ Running      54s    ready:0/1
└──# revision:1
   └──⧉ weather-app-785c7bbcd7           ReplicaSet  ✔ Healthy      6m40s  stable
      ├──□ weather-app-785c7bbcd7-2vjzv  Pod         ✔ Running      6m40s  ready:1/1
      └──□ weather-app-785c7bbcd7-rnmhd  Pod         ✔ Running      6m40s  ready:1/1

```

- To use a UI for the rollouts you can
```bash
kubectl-argo-rollouts dashboard
```
and access through localhost:3100


P.S: when i first tried and used rollouts, i noticed the rollback function through the UI creates a new revision with the previous image version, so it does it through helm. Abort is useful as it just stops the current rollout and it does not create a new revision, so if the helm chart changed and not just an image version, abort will fix it.

