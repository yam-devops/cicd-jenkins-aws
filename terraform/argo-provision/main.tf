resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = kubernetes_namespace.argocd.metadata[0].name
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "5.51.6" # Use latest stable
  timeout    = 600
  create_namespace = false

  values = [
    file("${path.module}/values/argocd-values.yaml")
  ]
}

