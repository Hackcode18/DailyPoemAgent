# DailyPoemAgent
# Daily Poem Agent 🌙

An always-on autonomous agent that writes a fresh poem every morning and publishes it to a live webpage — fully automated, no human input needed.

**Live App:** http://daily-poem-agent-12345.s3-website-us-east-1.amazonaws.com/

---

## What It Does

Every day at 6 AM UTC, this agent:
1. Wakes up automatically via a scheduled trigger
2. Calls an AI model to write a poem about today's date
3. Publishes it as a beautiful webpage
4. Goes back to sleep — ready for tomorrow

No app to open. No prompt to type. The poem is already there when you wake up.

---

## Architecture

| Service | Role |
|---|---|
| Amazon EventBridge | Triggers the agent every day at 6 AM UTC |
| AWS Lambda (Python 3.12) | Runs the core logic |
| Amazon Bedrock (Nova Lite) | Generates the poem using AI |
| Amazon S3 | Hosts the poem as a public webpage |

All services run on the **AWS Free Tier**.

---

## How It Works

```python
# Simplified flow
1. EventBridge fires cron(0 6 * * ? *)
2. Lambda calls Bedrock Nova Lite with today's date
3. Bedrock returns a fresh poem
4. Lambda wraps it in HTML
5. Lambda uploads index.html to S3
6. Public URL serves the poem
```

---

## Setup

### Prerequisites
- AWS account
- Bedrock Nova Lite model access enabled (us-east-1)

### Deploy

1. **Create S3 bucket**
   - Enable static website hosting
   - Set index document to `index.html`
   - Make bucket public

2. **Create Lambda function**
   - Runtime: Python 3.12
   - Upload `lambda_function.py`
   - Timeout: 30 seconds
   - Attach permissions: `AmazonBedrockFullAccess` + `AmazonS3FullAccess`

3. **Update bucket name in code**
```python
   BUCKET_NAME = 'your-bucket-name-here'
```

4. **Add EventBridge trigger**
   - Schedule: `cron(0 6 * * ? *)`

5. **Test**
   - Run Lambda test with empty `{}`
   - Check S3 for `index.html`
   - Visit your S3 website URL

---

## Project Structure
daily-poem-agent/
│
└── lambda_function.py # Core Lambda function

---

## Built With

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) — Nova Lite model
- [AWS Lambda](https://aws.amazon.com/lambda/) — Serverless compute
- [Amazon EventBridge](https://aws.amazon.com/eventbridge/) — Scheduling
- [Amazon S3](https://aws.amazon.com/s3/) — Static website hosting

---

## Article

Full write-up on AWS Builder Center:
https://builder.aws.com/content/3ICisQD6a947eC4WKIU9sfSxEJ5/weekend-creative-agent-challenge-daily-poem-agent

---

## License

MIT
