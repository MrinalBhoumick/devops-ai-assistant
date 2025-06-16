# 📘 DevOps AI Exam Assistant using Amazon Bedrock (Claude Sonnet)

This AWS Lambda function provides intelligent, exam-friendly responses to DevOps-related questions. It uses the Anthropic Claude model hosted on **Amazon Bedrock** and supports dynamic topics like Kubernetes, Helm, CI/CD, Observability, RBAC, and more.

---

## 🔧 Features

- ✅ Uses **Amazon Bedrock Claude Sonnet** to generate human-like answers
- ✅ Topic-based prompt enrichment via `prompt.py`
- ✅ Markdown output cleaned and returned as plain text
- ✅ Retry logic with exponential backoff on model invocation failures
- ✅ Designed for **internal exam prep** or **knowledge check tools**

---

## 📁 Project Structure

```

.
├── lambda\_function.py        # Main Lambda handler (contains Bedrock integration)
├── prompt.py                 # Dynamic prompt builder with topic-specific study content
├── README.md                 # Project documentation (this file)

````

---

## 🚀 Getting Started

### 1. Prerequisites

- An AWS account with Bedrock access
- IAM permissions to invoke `bedrock-runtime`
- AWS CLI configured or Lambda running in a suitable IAM role
- Region: `ap-south-1`

---

### 2. Environment Setup (Locally or Lambda)

Install required Python libraries:
```bash
pip install boto3
````

---

## 🧠 Topics Supported

You can pass a `topic` to get customized context:

* Kubernetes
* Helm
* Ingress
* Autoscaling
* RBAC
* Security
* CI/CD
* Monitoring
* Logging
* Secrets
* ServiceMesh
* Containers
* IaC
* Compliance
* Artifacts

Default is `General` if no topic is specified.

---

## 📨 API Usage

### Input (`event['body']`)

```json
{
  "question": "Explain the difference between StatefulSet and Deployment in Kubernetes",
  "topic": "Kubernetes"
}
```

### Output

```json
{
  "answer": "StatefulSets are used for stateful applications..."
}
```

---

## 🧪 Testing

You can test locally using:

```python
from lambda_function import lambda_handler

event = {
  "body": json.dumps({
    "question": "How does HPA work in Kubernetes?",
    "topic": "Autoscaling"
  })
}

response = lambda_handler(event, None)
print(json.loads(response["body"]))
```

---

## 🔄 Retry Logic

* Max Attempts: 7
* Delay Between Attempts: 3 seconds
* Automatically retries on transient errors from `bedrock-runtime`

---

## 🔐 Security Notes

* Ensure your Lambda role includes permissions to invoke `bedrock:InvokeModel`.
* Never log sensitive payloads or secrets.
* Use API Gateway to secure this function with authentication if exposing publicly.

---

## 🧹 Markdown Formatter

The output from Claude is cleaned from:

* Headers (`#`, `##`)
* Bold, italic, code formatting
* List item normalization

---

## 🏗️ Future Improvements

* Add streaming support for partial completions
* Add support for multiple languages
* Integrate with a web UI or chatbot
* Store user queries for improvement analytics

---

## 🧑‍💻 Author

**Mrinal Bhoumick**
DevOps Enthusiast | AWS | Kubernetes | GitOps

---

## 📄 License

This project is internal-use and educational. You may adapt for your organization’s exam preparation needs or personal study tools.

```

---

Let me know if you'd like:
- A deployment script via AWS SAM or CDK.
- A `requirements.txt`.
- GitHub Actions CI/CD for automatic deployment.
```
