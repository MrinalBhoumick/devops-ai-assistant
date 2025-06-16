def build_prompt(user_question, topic="General"):
    """
    Builds a prompt using filtered content based on the selected topic with extended knowledge base.
    """
    knowledge_base_by_topic = {
        "Kubernetes": """
🔹 **Kubernetes Core Components**
✅ **Pods**: Smallest deployable unit. Can have multiple containers sharing storage/network. Lifecycle: Pending, Running, Succeeded, Failed, Unknown.
✅ **Deployments**: Declaratively manage updates and scale ReplicaSets. Enable rolling updates and rollbacks.
✅ **ReplicaSets**: Maintain a stable set of replica Pods. Automatically replaced if pods die.
✅ **StatefulSets**: Provide stable identities and persistent storage for pods. Ideal for stateful apps (e.g., databases).
✅ **DaemonSets**: Ensure a copy of a pod runs on all (or selected) nodes. Used for logs/metrics agents.
✅ **Jobs/CronJobs**: One-time (Jobs) or scheduled tasks (CronJobs). Ensure completion of a batch process.

🔹 **Configuration & Networking**
✅ **Services**: Abstractions to expose pods. Types:
   - ClusterIP: Internal access only.
   - NodePort: Access via `<NodeIP>:<Port>`.
   - LoadBalancer: Expose via external load balancer.
✅ **Namespaces**: Logical isolation within a cluster.
✅ **ConfigMaps & Secrets**: Store config data (non-sensitive vs sensitive). Secrets base64-encoded by default.
✅ **Volumes**: Handle persistent data. PVC binds to PV.

🔹 **Networking & Discovery**
✅ **CNI Plugins**: Implement pod networking (e.g., Calico, Flannel).
✅ **CoreDNS**: Handles service discovery via DNS.
✅ **Network Policies**: Restrict traffic between pods.

🔹 **Resource Management**
✅ **Requests & Limits**: Define min/max resource allocation.
✅ **QoS Classes**: 
   - Guaranteed: Requests == Limits.
   - Burstable: Requests < Limits.
   - BestEffort: No requests/limits.
""",

        "Helm": """
🔹 **Helm – Kubernetes Package Manager**
✅ **Concepts**
- Chart: Package of Kubernetes manifests (YAML + templates).
- Templates: Go-based templates (`{{ .Values }}`).
- Values.yaml: Default user configuration.
✅ **File Structure**
- Chart.yaml: Metadata.
- values.yaml: User config.
- templates/: YAML with templating.
- _helpers.tpl: Helper templates for reuse.

✅ **Helm Commands**
- `helm install <release> <chart>`: Install.
- `helm upgrade --install`: Upgrade or install.
- `helm template`: Render manifests.
- `helm lint`: Validate charts.
- `helm package`: Create `.tgz`.

✅ **Best Practices**
- Version charts.
- Keep values configurable.
- Use `.Values`, `.Chart`, `.Release` smartly.
""",

        "Ingress": """
🔹 **Ingress & External Traffic**
✅ **Ingress Concepts**
- Ingress: Manages external HTTP(S) access to Services.
- Ingress Controller: Handles Ingress resources (e.g., NGINX, Traefik).
✅ **Routing**
- Host-based (example.com).
- Path-based (/api, /admin).
✅ **TLS**
- TLS termination at Ingress level.
- Cert-manager for automation.

✅ **Annotations**
- Rewrite targets.
- Enable rate-limiting.
- TLS redirection and sticky sessions.

✅ **Alternatives**
- LoadBalancer: Expose via external cloud LB.
- NodePort: Static port on each node.
""",

        "Autoscaling": """
🔹 **Kubernetes Autoscaling**
✅ **Types of Autoscalers**
- **HPA** (Horizontal Pod Autoscaler): Scales pods based on CPU/memory/custom metrics.
- **VPA** (Vertical Pod Autoscaler): Adjusts resource requests/limits dynamically.
- **Cluster Autoscaler**: Scales nodes based on pod scheduling needs.

✅ **Advanced Scheduling**
- **Node Affinity**: Prefer/require pods on certain nodes.
- **Taints & Tolerations**: Prevent scheduling unless tolerated.
- **PodDisruptionBudget (PDB)**: Limit voluntary disruptions during maintenance.
""",

        "RBAC": """
🔹 **Kubernetes RBAC (Role-Based Access Control)**
✅ **Key Concepts**
- **Role**: Permissions in a namespace (verbs, resources).
- **ClusterRole**: Cluster-wide permissions.
- **RoleBinding**: Bind Role to user/group/service account in a namespace.
- **ClusterRoleBinding**: Bind ClusterRole cluster-wide.
- **ServiceAccount**: Used by pods for API access.

✅ **Best Practices**
- Least privilege.
- Use separate accounts per app.
- Audit with `kubectl auth can-i`, `rbac-lookup`, `rakkess`.
""",

        "Security": """
🔹 **Kubernetes Security**
✅ **Container Security**
- Run as non-root.
- Use read-only filesystem.
- Set `securityContext` appropriately.
- Drop unnecessary Linux capabilities.

✅ **Network Security**
- Use Network Policies.
- Enable mTLS with Service Mesh (Istio/Linkerd).
- Use isolated namespaces.

✅ **Secrets Management**
- Use SealedSecrets or External Secrets.
- Enable encryption at rest.
- Rotate secrets and TLS certificates regularly.

✅ **API Server Hardening**
- Enable audit logs.
- Limit API exposure.
- Use admission controllers (e.g., OPA).
""",

        "CI/CD": """
🔹 **CI/CD & GitOps**
✅ **CI/CD Tools**
- Jenkins: Groovy pipelines, plugins.
- GitHub Actions: Native GitHub integration.
- GitLab CI: `.gitlab-ci.yml` driven.

✅ **GitOps Tools**
- ArgoCD: Declarative Git-based deployment; auto-sync support.
- FluxCD: Lightweight GitOps; built-in image automation.

✅ **Patterns**
- Canary and Blue/Green deployments.
- Helm/Kustomize support.
- Integrate Secrets/Infra as Code with pipelines.
""",

        "Monitoring": """
🔹 **Monitoring in Kubernetes**
✅ **Metrics Collection**
- Prometheus: Core metrics + PromQL.
- kube-state-metrics: K8s object states as metrics.
- Node Exporter: Host-level metrics.

✅ **Dashboards & Alerts**
- Grafana: Visualize Prometheus data.
- Alertmanager: Deduplicate and route alerts.

✅ **Service Mesh Observability**
- Istio/Linkerd expose per-service metrics.
- Jaeger/Zipkin used for tracing.
""",

        "Logging": """
🔹 **Centralized Logging**
✅ **Stacks**
- **EFK**: Elasticsearch, Fluentd, Kibana.
- **Loki**: Prometheus-style logging.
- **Fluent Bit**: Lightweight log forwarder.

✅ **Distributed Tracing**
- Jaeger: Trace request flows across services.
- OpenTelemetry: Unified API for metrics, logs, traces.
""",

        "Secrets": """
🔹 **Secrets Handling**
✅ **Kubernetes Secrets**
- Base64-encoded.
- Use RBAC & encryption at rest.

✅ **Tools**
- SealedSecrets: Public-key encryption, Git-safe.
- External Secrets Operator: Pull from AWS/GCP/Vault.
- Vault: Dynamic secrets, policy-based access.

✅ **Best Practices**
- Don’t expose secrets in YAML or Git.
- Rotate regularly.
- Use short TTL.
""",

        "ServiceMesh": """
🔹 **Service Mesh**
✅ **Core Mesh Tools**
- **Istio**: mTLS, traffic shifting, observability.
- **Linkerd**: Simpler, lightweight.
- **Consul Connect**: Works well with HashiCorp tools.

✅ **Features**
- Sidecar proxies (Envoy).
- mTLS encryption.
- Canary/A-B testing with traffic shifting.

✅ **Observability**
- Integrated metrics, tracing.
- Native dashboards in Prometheus/Grafana.
""",

        "Containers": """
🔹 **Containers & Runtimes**
✅ **Container Tools**
- Docker: Core tool for container lifecycle.
- Podman: Rootless Docker alternative.
- BuildKit: Parallelized, cache-optimized builds.
- Docker Compose: Multi-container setups.

✅ **Runtimes**
- Containerd: Runtime used by Kubernetes.
- CRI-O: Lightweight OCI-compliant runtime.
""",

        "IaC": """
🔹 **Infrastructure as Code**
✅ **Popular Tools**
- Terraform: Modular, stateful infra management.
- Pulumi: Code-based IaC with typed languages.
- Ansible: Agentless config management.
- AWS CloudFormation: AWS-native IaC.

✅ **Best Practices**
- Version control all infra.
- Use `checkov`, `tflint` for scanning/linting.
- Use workspaces for stage separation.
""",

        "Compliance": """
🔹 **Compliance & Policy**
✅ **Tools**
- **OPA/Gatekeeper**: Write policies in Rego.
- **Kyverno**: Easier syntax, native to K8s.
- **kube-bench**: CIS benchmark checker.
- **Trivy**: Scan containers, IaC, SBOMs.

✅ **Use Cases**
- Enforce labeling, prohibit root, restrict registries.
- Gatekeeper for runtime policy enforcement.
""",

        "Artifacts": """
🔹 **Artifact Repositories**
✅ **Tools**
- **JFrog Artifactory**: Enterprise-grade repo.
- **Nexus**: Supports Docker, Maven, etc.
- **Harbor**: Container registry with scanning.

✅ **Features**
- RBAC, retention, proxy public registries.
- Integrates with CI/CD for secure artifact flow.
""",

        "General": """
🔹 **Full DevOps & Kubernetes Study Guide**
✅ Kubernetes: Core concepts, deployments, services, scaling, networking.
✅ Helm: Charts, templating, best practices.
✅ CI/CD: GitHub Actions, ArgoCD, GitOps strategies.
✅ Monitoring & Logging: Prometheus, Grafana, EFK, Loki.
✅ Secrets Management: Vault, SealedSecrets, External Secrets.
✅ Security: RBAC, Network Policies, API server hardening.
✅ IaC: Terraform, CloudFormation, Pulumi.
✅ Compliance: Kyverno, Gatekeeper, CIS Benchmarks.
✅ Service Mesh: Istio, Linkerd, observability and security.
✅ Containerization: Docker, CRI-O, Podman.
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
