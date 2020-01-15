import json
import boto3
import urllib.request, urllib.parse

bucket_name = 'visualization-app-camera'
file_name = "capture_20200115121007.jpg"
rekognition_client = boto3.client('rekognition')

def main():
    
    # Rekognitionに画像を渡して結果を取得
    response = rekognition_client.detect_labels(
        Image= {
            'S3Object':
            {
                'Bucket':bucket_name,
                'Name':file_name
            }
        },
    )

    print("## Rekognition Response")
    print(response)

    # Rrekognitionの結果をJSONファイルで保存
    with open('./JSON/json_labels01.json', 'w') as f:
        json.dump(response, f, indent=2)
    
    return {
        'statusCode': 200,
    }

if __name__ == "__main__":
    main()