def build_prompt(user_question, topic="General"):
    """
    Builds a prompt using filtered content based on the selected topic.
    """
    knowledge_base_by_topic = {
        "Kubernetes": """
🔹 Kubernetes Ecosystem & Core Concepts
✅ Core Concepts
Pods: Smallest deployable unit in K8s; one or more containers sharing network/storage.
Deployments: Manage ReplicaSets; enable rolling updates and rollbacks.
ReplicaSets: Ensure a specified number of pod replicas are running.
Services: Stable endpoints for Pods; types: ClusterIP, NodePort, LoadBalancer.
Namespaces: Virtual clusters within a physical cluster; isolate workloads.
ConfigMaps: Store non-sensitive configuration data (env vars, CLI args).
Secrets: Store sensitive data (tokens, passwords) in base64-encoded form.
Volumes: Persistent or ephemeral storage mounted to Pods.
StatefulSets: For stateful apps needing persistent identity and storage.
DaemonSets: Ensure one pod per node (e.g., for log collection).
Jobs/CronJobs: Run one-time or scheduled batch processes.
""",

        "Helm": """
🔹 Helm Charts & Packaging
Helm: Kubernetes package manager.
Chart: A collection of YAML files to describe a K8s app.
Templates: Use Go templating to make YAML dynamic.
Commands: helm install, helm upgrade, helm repo add, helm lint, helm package.
Values.yaml: Central config file for parameterization.
Dependencies: Charts can depend on other charts; managed via Chart.yaml.
""",

        "Ingress": """
🔹 Ingress Controllers & Load Balancing
Ingress: Manages external HTTP/HTTPS traffic to services.
Ingress Controller: NGINX, Traefik, HAProxy—must be installed separately.
LoadBalancer: Exposes services externally via cloud LB (AWS ELB, etc).
TLS termination and path-based routing done via Ingress.
Annotations: Configure behavior like rewrite-target or rate-limiting.
""",

        "Autoscaling": """
🔹 Cluster Autoscaler, Node Affinity, Taints/Tolerations
Cluster Autoscaler: Adds/removes nodes based on pending pods.
Horizontal Pod Autoscaler (HPA): Scales pods based on CPU/memory or custom metrics.
Vertical Pod Autoscaler (VPA): Adjusts pod resources (CPU/RAM) automatically.
Node Affinity: Assign pods to specific nodes based on labels.
Taints: Prevent scheduling unless toleration is present.
Tolerations: Allow pods to schedule on tainted nodes.
""",

        "RBAC": """
🔹 RBAC (Role-Based Access Control)
Roles/ClusterRoles: Define permissions (verbs, resources).
RoleBindings/ClusterRoleBindings: Bind roles to users/service accounts.
Namespaces: Roles are namespace-scoped; ClusterRoles are cluster-wide.
ServiceAccounts: Used by pods to authenticate to API server.
""",

        "Security": """
🔹 Kubernetes Security Best Practices
Run containers as non-root.
Use read-only file systems where possible.
Limit container capabilities using securityContext.capDrop.
Enable Network Policies to control traffic between pods.
Audit logs: Enable for tracing changes.
Rotate Secrets and TLS certificates regularly.
Use tools like Trivy and kube-bench for scanning.
Restrict API server access and use RBAC.
""",

        "CI/CD": """
🔸 CI/CD Tools
✅ Jenkins: Scripted/Declarative pipelines; agents can run in Kubernetes.
✅ GitHub Actions: Native to GitHub, uses YAML workflows.
✅ GitLab CI: .gitlab-ci.yml, integrates with Kubernetes runners.
✅ ArgoCD (GitOps): Declarative CD, auto-syncs with Git repo.
✅ FluxCD: GitOps tool; uses source-controller and kustomize-controller.
Blue/Green & Canary Deployments supported with Argo Rollouts.
""",

        "Monitoring": """
🔸 Monitoring & Alerting
✅ Prometheus: Pull-based metrics, PromQL query language.
✅ Grafana: Visualizes metrics; alerting with integrations.
✅ Alertmanager: Deduplicates, groups, and routes alerts.
✅ Node Exporter: Collects host-level metrics for Prometheus.
✅ kube-state-metrics: Exposes cluster object states as metrics.
""",

        "Logging": """
🔸 Logging & Tracing
✅ EFK Stack (Elasticsearch, Fluentd, Kibana): Centralized logging.
✅ Loki (Grafana Labs): Lightweight logging with Prometheus-like labels.
✅ Fluent Bit: Lightweight Fluentd alternative for edge logging.
✅ Jaeger: Distributed tracing platform; supports OpenTracing.
✅ OpenTelemetry: Vendor-neutral observability framework (metrics, logs, traces).
""",

        "Secrets": """
🔸 Secrets Management
✅ Kubernetes Secrets: Base64-encoded, not encrypted by default.
✅ HashiCorp Vault: Dynamic secrets, fine-grained access policies.
✅ Sealed Secrets: Encrypt K8s Secrets using a controller’s public key; safe for Git.
✅ External Secrets Operator: Sync secrets from external providers (AWS, GCP, Vault).
""",

        "ServiceMesh": """
🔸 Service Mesh
✅ Istio: Advanced traffic routing, mTLS, telemetry, fault injection.
✅ Linkerd: Lightweight, secure-by-default, high performance.
✅ Consul Connect: Integrates with HashiCorp stack for service discovery and mesh.
✅ Sidecars: Proxies deployed alongside apps (e.g., Envoy).
""",

        "Containers": """
🔸 Container Tools
✅ Docker: CLI and runtime for building, running containers.
✅ BuildKit: Modern builder backend; fast, cache-aware builds.
✅ Docker Compose: Define multi-container apps in docker-compose.yml.
✅ Podman: Docker-compatible but daemonless.
✅ Containerd: Core container runtime used by Kubernetes.
""",

        "IaC": """
🔸 Infrastructure as Code (IaC)
✅ Terraform: Declarative language (.tf); supports state management and modules.
✅ Ansible: Procedural automation via playbooks and inventories.
✅ Pulumi: IaC using general-purpose languages (Python, TypeScript, Go).
✅ CloudFormation: AWS-native declarative IaC service.
""",

        "Compliance": """
🔸 Policy & Compliance
✅ OPA/Gatekeeper: Admission controller to enforce policies via Rego.
✅ Trivy: Scan container images, IaC, SBOMs for vulnerabilities.
✅ kube-bench: Validates against CIS Kubernetes Benchmarks.
✅ Kyverno: Kubernetes-native policy engine (no external controller needed).
""",

        "Artifacts": """
🔸 Artifact Management
✅ Nexus: Supports Docker, Maven, PyPI, NPM, more; can proxy public repos.
✅ JFrog Artifactory: High availability, CI/CD ready artifact management.
✅ Harbor: OCI-compliant container registry with vulnerability scanning.
""",

        "General": """🔹 Full DevOps Study Material Summary
Refer to all topics across Kubernetes, Helm, Ingress, CI/CD, Monitoring, Security, Service Mesh, Secrets Management, and more. Use this when topic-specific material is unavailable.
"""
    }

    study_content = knowledge_base_by_topic.get(topic, knowledge_base_by_topic["General"])

    return f"""Human:
You are a Kubernetes and DevOps expert AI assistant helping someone prepare for their internal exam at work.

Here is the study material to refer to:
{study_content}

Now, using the above information, answer the following question in an exam-friendly format:

{user_question}

Assistant:"""
