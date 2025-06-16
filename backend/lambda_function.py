import json
import boto3
import time
import logging
import re
from prompt import build_prompt

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_runtime = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Constants
MODEL_ID = "arn:aws:bedrock:Region:1234XXX:inference-profile/apac.anthropic.claude-sonnet-4-20250514-v1:0"
MAX_RETRIES = 7
RETRY_DELAY_SECONDS = 3
MAX_TOKENS = 25000


def format_markdown_to_text(markdown: str) -> str:
    """Convert markdown to simplified plain text for better readability."""
    logger.info("Formatting markdown content to plain text")

    markdown = re.sub(r'#{1,6}\s*', '', markdown)
    markdown = re.sub(r'\*\*(.*?)\*\*', r'\1', markdown)
    markdown = re.sub(r'\*(.*?)\*', r'\1', markdown)
    markdown = re.sub(r'__(.*?)__', r'\1', markdown)
    markdown = re.sub(r'_(.*?)_', r'\1', markdown)
    markdown = re.sub(r'\n\s*[-*+]\s*', '\n- ', markdown)
    markdown = re.sub(r'[`>]', '', markdown)
    markdown = re.sub(r'\n{2,}', '\n\n', markdown)

    formatted = markdown.strip()
    logger.info("Formatted content: %s", formatted)
    return formatted


def lambda_handler(event, context):
    logger.info("Lambda function triggered.")
    logger.info("Received event: %s", json.dumps(event))

    try:
        body = json.loads(event['body'])
        user_input = body.get("question", "").strip()
        topic = body.get("topic", "General").strip()

        logger.info("Parsed input - Question: '%s', Topic: '%s'", user_input, topic)

        if not user_input:
            logger.warning("Request missing 'question' key or it's empty.")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'question' in request"})
            }

        logger.info("Constructing prompt for topic '%s'", topic)
        combined_prompt = build_prompt(user_input, topic)
        logger.info("Prompt constructed successfully.")

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "messages": [{"role": "user", "content": combined_prompt}]
        }
        logger.info("Payload ready for model: %s", json.dumps(payload))

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info("Attempt %d: Invoking Bedrock model...", attempt)

                response = bedrock_runtime.invoke_model(
                    modelId=MODEL_ID,
                    contentType="application/json",
                    accept="application/json",
                    body=json.dumps(payload).encode("utf-8")
                )

                logger.info("Model response received successfully on attempt %d", attempt)
                raw_response = response["body"].read().decode("utf-8")
                logger.info("Raw response from model: %s", raw_response)

                result = json.loads(raw_response)
                model_output = result.get("content", [])[0].get("text", "").strip()

                logger.info("Extracted text from model output.")
                logger.debug("Model raw text: %s", model_output)

                formatted_answer = format_markdown_to_text(model_output)

                logger.info("Returning formatted answer to client.")
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"answer": formatted_answer}, ensure_ascii=False, indent=2)
                }

            except Exception as retry_exception:
                logger.warning("Attempt %d failed: %s", attempt, str(retry_exception))
                if attempt == MAX_RETRIES:
                    logger.error("Max retries reached. Failing Lambda.")
                    raise
                logger.info("Retrying after %d seconds...", RETRY_DELAY_SECONDS)
                time.sleep(RETRY_DELAY_SECONDS)

    except Exception as e:
        logger.error("Unhandled exception occurred: %s", str(e), exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
