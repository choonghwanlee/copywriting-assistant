# Copywriting Assistant

Demo app of enterprise copywriting assistant, built using Amazon Bedrock & FastAPI.

## Week 10 submission:

Deliverables:

- Security implementation (Security, Privacy)
- Audit documentation
- Compliance report
- Final Presentation

### Getting Started

Clone the repository and install the dependencies:

```bash
git clone https://github.com/choonghwanlee/copywriting-assistant.git
cd copywriting-assistant
pip install -r requirements.txt
```

To start the FastAPI server in development mode:

```bash
fastapi dev main.py
```

This will launch the app at http://localhost:8000. You can access the interactive API docs at http://localhost:8000/docs.

Make sure your AWS credentials are properly configured before running the app.

Once the app is launched, go to http://localhost:8000/docs for a friendly UI to experiment with the app and see the AWS Bedrock Guardrail in action.

### Security Implementation

To secure our app, we use:

1. JWT token authentication to disable API access to unauthenticated users.
2. AWS Bedrock Guardrail to prevent:
   - Prompt attacks (i.e. SQL injection, jailbreak prompts)
   - Harmful categories (i.e. hate, sexually explicit content, etc.)
   - Custom denied topics (i.e. political or election related content, medical or health claims)
   - Profanity
   - PII masking

PII masking allows us to redact sensitive information from the Bedrock model, enabling privacy in our AI system.

In addition, we want our copywriting assistant to not generate marketing copies that represent the brand in unfavorable ways. This not only includes hateful speech, profanity, etc., but also 1. misleading advertisement about the clinical effectiveness of a product 2. direct partisan support for specific candidates. Marketing copies that fall under these categories can tarnish the reputation of the brand, and we block these prompts with a custom message, "Sorry, the model cannot answer this question."

### Audit Documentation

We enable AWS CloudWatch logging/monitoring via the Watchtower package. This allows us to track successful/unsuccessful login attempts, and any prompts/responses that our AWS Bedrock Guardrail blocks. Monitoring allows us to easily aggregate safety/security data during audits. It also allows us to automatically trigger alerts/notifications when flags are raised repeatedly in a short time-span (which can indicate the presence of a malicious actor).

Thus, we configure AWS CloudWatch Alerts to automatically send me an email if the logger raises a warning more than 5 times within a minute.

### Compliance Documentation

Our copywriting assistant is designed with compliance in mind, particularly with respect to key data protection regulations such as the General Data Protection Regulation (GDPR). We ensure that no personally identifiable information (PII) is stored or exposed during the generation process. All interactions with the model are stateless and ephemeral—PII is masked before being sent to the Bedrock model, and we do not log any raw input or output that contains user-submitted data unless it has been fully redacted.

In addition to privacy regulations, our app aligns with the NIST AI Risk Management Framework (AI RMF) to ensure responsible AI use. This includes proactively managing risks related to safety, fairness, transparency, and accountability. Through the use of Amazon Bedrock Guardrails, we block harmful or inappropriate content as well as any prompt attack methods. We also maintain audit logs, human oversight in critical workflows, and mechanisms for flagging and reviewing questionable prompts. These practices support a trustworthy AI system that is not only technically secure but also aligned with emerging ethical standards.

### Final Presentation

[You can find the final presentation in the slides here](https://docs.google.com/presentation/d/1mo47NkAUcDz96n7Wwa3m395Mxicn8qAT2PPNHjpnxgc/edit?usp=sharing)
