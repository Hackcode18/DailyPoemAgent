import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    s3 = boto3.client('s3')
    
    BUCKET_NAME = 'your-bucket-name-here'  # ← CHANGE THIS before uploading
    today = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")
    
    # Call Bedrock Nova Lite
    response = bedrock.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        body=json.dumps({
            "messages": [{
                "role": "user",
                "content": f"Write a short, beautiful and original poem about {day_of_week}, {today}. Make it 4-6 lines. Be vivid, emotional and creative. Do not add any title or explanation, just the poem."
            }],
            "inferenceConfig": {"max_new_tokens": 300}
        })
    )
    
    result = json.loads(response['body'].read())
    poem = result['output']['message']['content'][0]['text']
    
    # Create a clean HTML page
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Poem - {today}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Georgia', serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }}
        .card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 60px 50px;
            max-width: 580px;
            width: 100%;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .label {{
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: rgba(255,255,255,0.4);
            margin-bottom: 12px;
        }}
        .date {{
            font-size: 1rem;
            color: rgba(255,255,255,0.6);
            margin-bottom: 48px;
        }}
        .poem {{
            font-size: 1.25rem;
            line-height: 2;
            color: rgba(255,255,255,0.92);
            white-space: pre-wrap;
            font-style: italic;
        }}
        .footer {{
            margin-top: 48px;
            font-size: 0.72rem;
            color: rgba(255,255,255,0.25);
            letter-spacing: 0.1em;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="label">Daily Poem</div>
        <div class="date">{day_of_week}, {today}</div>
        <div class="poem">{poem}</div>
        <div class="footer">Generated daily by Amazon Bedrock Nova Lite</div>
    </div>
</body>
</html>"""
    
    # Upload to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='index.html',
        Body=html,
        ContentType='text/html'
    )
    
    print(f"Poem generated and uploaded for {today}")
    return {
        'statusCode': 200,
        'body': json.dumps({'date': today, 'poem': poem})
    }
