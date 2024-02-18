import json
import boto3

bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):

    # This lambda only takes the prompt as input. If you want
    # to include all llm parameters into the input, call
    # event_body = json.loads(event["body"]) and use this
    # into the invoke_model_with_response_stream body.

    body = {
        "prompt": event["body"],
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.1
    }

    response_stream = bedrock.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId="meta.llama2-13b-chat-v1",
        accept="application/json",
        contentType="application/json",
    )
    status_code = response_stream["ResponseMetadata"]["HTTPStatusCode"]
    if status_code != 200:
        raise ValueError(f"Error invoking Bedrock API: {status_code}")
    for response in response_stream["body"]:
        json_response = json.loads(response["chunk"]["bytes"])
        print(json_response["generation"])
        yield json_response["generation"].encode()
