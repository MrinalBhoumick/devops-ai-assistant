def build_prompt(user_question, topic="General"):
    """
    Builds a prompt using filtered content based on the selected topic.
    """
    knowledge_base_by_topic = {
        "Kubernetes": """
🔹 Kubernetes Ecosystem & Core Concepts
✅ Core Concepts
Pods: Smallest deployable unit; share network/storage. Init Containers run before app containers. Lifecycle phases: Pending, Running, Succeeded, Failed, Unknown.
Deployments: Declaratively manage ReplicaSets. Enable rolling updates & rollbacks.
ReplicaSets: Maintain a stable set of replica Pods.
StatefulSets: For apps needing persistent ID & storage; stable network IDs.
DaemonSets: Run one pod per node (e.g., monitoring agents).
Jobs/CronJobs: For one-off and scheduled tasks.

✅ Configuration & Networking
Services: Stable endpoint for accessing Pods. Types: ClusterIP, NodePort, LoadBalancer.
Namespaces: Isolate workloads and resources logically.
ConfigMaps & Secrets: Manage configuration (non-sensitive & sensitive). Secrets are base64-encoded, not encrypted by default.
Volumes: Ephemeral or Persistent. PVCs bind to PVs.

✅ Networking
CNI Plugins: Calico, Flannel, Cilium for pod networking.
CoreDNS: Provides service discovery.
Network Policies: Control pod-to-pod communication.

✅ Resource Management
Requests/Limits: CPU & memory bounds.
QoS Classes: Guaranteed, Burstable, BestEffort.
""",

        "Helm": """
🔹 Helm Charts & Packaging
✅ Basics
Helm: Package manager for Kubernetes.
Chart: Bundle of templates + values used to deploy K8s resources.
Templates: Go templating syntax for reusable manifests.

✅ Key Files
Chart.yaml: Metadata (name, version, dependencies).
values.yaml: Default configuration values.
_helpers.tpl: Define reusable template snippets.

✅ Commands
helm install/upgrade/uninstall.
helm repo add/update/list.
helm template (render locally), helm lint (validate chart).
helm package (create .tgz from chart).

✅ Best Practices
Use defaults in values.yaml.
Avoid hardcoding.
Use `.Values`, `.Release`, `.Chart`, `.Capabilities`.
""",

        "Ingress": """
🔹 Ingress Controllers & Load Balancing
✅ Concepts
Ingress: Expose HTTP/HTTPS routes to services inside the cluster.
Ingress Controller: Software that implements Ingress (e.g., NGINX, Traefik).
Annotations: Control rewrites, TLS redirects, rate-limiting, etc.

✅ TLS & Routing
TLS Termination: Offload SSL to the Ingress controller.
Path-based Routing: Direct traffic by path (e.g., /api, /web).
Host-based Routing: Route by domain.

✅ Alternatives
LoadBalancer: Exposes service externally via cloud provider.
NodePort: Expose on static port across all nodes.
""",

        "Autoscaling": """
🔹 Cluster Autoscaler & Pod Autoscaling
✅ Autoscalers
Horizontal Pod Autoscaler (HPA): Scales pods based on CPU/memory/custom metrics.
Vertical Pod Autoscaler (VPA): Adjusts pod resource requests/limits.
Cluster Autoscaler: Adds/removes nodes based on scheduling failures.

✅ Scheduling Control
Node Affinity: Prefer or require pods to be on specific nodes (via labels).
Taints & Tolerations: Prevent unwanted pods from being scheduled on certain nodes.
PodDisruptionBudget (PDB): Define voluntary disruption limits.
""",

        "RBAC": """
🔹 Role-Based Access Control (RBAC)
✅ Components
Roles: Namespace-scoped permissions (verbs, resources).
ClusterRoles: Cluster-wide permissions.
RoleBindings: Assign Role to subjects within a namespace.
ClusterRoleBindings: Assign ClusterRole to subjects cluster-wide.
ServiceAccounts: Used by Pods to authenticate to API server.

✅ Best Practices
Follow principle of least privilege.
Audit RBAC with tools like rbac-lookup, rakkess.
""",

        "Security": """
🔹 Kubernetes Security Best Practices
✅ Container Security
Run containers as non-root.
Use read-only root file systems.
Drop unnecessary Linux capabilities via `securityContext.capDrop`.

✅ Network Security
Use Network Policies to isolate workloads.
Use mTLS via Service Mesh (e.g., Istio) for service-to-service encryption.

✅ Secrets Management
Rotate Secrets & TLS Certs regularly.
Use SealedSecrets or External Secrets Operator.
Restrict etcd access (stores all cluster data).

✅ API Server Hardening
Use RBAC.
Audit Logs enabled.
Use Admission Controllers for validation.

✅ Tools
Trivy: Image/IaC scanning.
kube-bench: CIS compliance testing.
""",

        "CI/CD": """
🔹 CI/CD & GitOps Tools
✅ Traditional CI/CD
Jenkins: Scripted or declarative pipelines.
GitLab CI: Defined via `.gitlab-ci.yml`.
GitHub Actions: GitHub-native CI/CD with YAML workflows.

✅ GitOps
ArgoCD: Declarative CD tool. Syncs with Git repositories.
FluxCD: Lightweight GitOps tool with source and kustomize controllers.
Supports Canary/Blue-Green deployments via Argo Rollouts.

✅ Tools Integration
Helm & Kustomize supported in both ArgoCD and Flux.
""",

        "Monitoring": """
🔹 Observability & Alerting
✅ Monitoring Stack
Prometheus: Metrics collection. Uses PromQL for querying.
kube-state-metrics: Exposes K8s object states as metrics.
Node Exporter: Host-level metrics.

✅ Visualization & Alerts
Grafana: Dashboard visualization; alerting support.
Alertmanager: Group, throttle, and route alerts (email, Slack, etc).

✅ Service Mesh Monitoring
Integrate metrics from Istio/Linkerd sidecars.
""",

        "Logging": """
🔹 Centralized Logging & Tracing
✅ Logging
EFK Stack: Elasticsearch, Fluentd, Kibana.
Loki: Prometheus-style logging backend.
Fluent Bit: Lightweight logging agent for edge.

✅ Tracing
Jaeger: OpenTracing compatible distributed tracing.
OpenTelemetry: Unified observability (metrics, logs, traces).
""",

        "Secrets": """
🔹 Secrets Management
✅ Kubernetes Secrets: Base64-encoded; use RBAC & encryption at rest.
✅ HashiCorp Vault: Dynamic secrets, policy-based access, secret leasing.
✅ SealedSecrets: Encrypt secrets using public key—safe to store in Git.
✅ External Secrets Operator: Sync secrets from cloud providers or Vault.

✅ Best Practices
Don’t commit secrets to Git.
Use short TTL and rotate regularly.
Audit secret usage and access logs.
""",

        "ServiceMesh": """
🔹 Service Mesh & Service-to-Service Communication
✅ Core Tools
Istio: Rich features (traffic shaping, telemetry, mTLS).
Linkerd: Simpler and lightweight alternative.
Consul Connect: Integrated with HashiCorp ecosystem.

✅ Components
Sidecars (Envoy): Injected proxies per pod.
mTLS: Encrypted service communication.
Traffic Shifting: Canary, A/B testing, retries, timeouts.

✅ Observability
Built-in metrics, tracing, and dashboards.
Integrate with Grafana/Prometheus.
""",

        "Containers": """
🔹 Container Tooling & Runtimes
✅ Docker: Build, run, and manage containers.
✅ Podman: Docker alternative; daemonless & rootless support.
✅ BuildKit: Improved build performance, caching, concurrency.
✅ Docker Compose: Define multi-container apps in YAML.

✅ Runtimes
Containerd: Core runtime used in Kubernetes.
CRI-O: Lightweight Kubernetes container runtime.
""",

        "IaC": """
🔹 Infrastructure as Code (IaC)
✅ Terraform: Declarative IaC for cloud infrastructure; supports modules and state.
✅ Pulumi: IaC using familiar languages like Python, TS, Go.
✅ Ansible: Procedural config management; great for server provisioning.
✅ AWS CloudFormation: AWS-native declarative tool.

✅ Best Practices
Use version control for all IaC.
Separate dev/stage/prod using workspaces or environments.
Use linters (tflint), scanners (checkov).
""",

        "Compliance": """
🔹 Policy & Compliance in Kubernetes
✅ OPA/Gatekeeper: Define and enforce policies using Rego language.
✅ Kyverno: Kubernetes-native policy engine; easier syntax than OPA.
✅ kube-bench: Scan K8s clusters against CIS Benchmarks.
✅ Trivy: Scan images, SBOMs, IaC for vulnerabilities.

✅ Use Cases
Deny root containers, enforce labels/annotations, image registry restrictions.
""",

        "Artifacts": """
🔹 Artifact Repositories
✅ JFrog Artifactory: Enterprise-grade artifact manager.
✅ Nexus Repository: Supports Docker, Maven, NuGet, etc.
✅ Harbor: OCI-compliant container registry with vulnerability scanning.

✅ Features
Role-based access, retention policies, proxying public registries.
Integrates with CI tools for build pipelines.
""",

        "General": """🔹 Full DevOps Study Material Summary
Includes Kubernetes concepts, Helm, CI/CD, Observability, Secrets Management, Container Runtimes, IaC tools, GitOps tools, and policy/compliance practices. Use this for an all-in-one review session.
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
