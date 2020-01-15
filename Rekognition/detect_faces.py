import json
import io
import boto3
from PIL import Image, ImageDraw, ExifTags, ImageColor

bucket_name = 'visualization-app-camera'
client = boto3.client('rekognition')


def show_faces(photo, bucket):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_bucket = s3_connection.Bucket('visualization-app-camera')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()    

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    #Call DetectFaces 
    response = client.detect_faces(
        Image=
        {
            'S3Object': 
                {
                    'Bucket': bucket, 
                    'Name': photo
                }
        },
        Attributes=['ALL']
    )
    
    with open('./JSON/json_faces01.json', 'w') as f:
        json.dump(response, f, indent=2)

    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)                      

    # calculate and display bounding boxes for each detected face       
    print('Detected faces for ' + photo)    
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']

        print('Left: ' + '{0:.0f}'.format(left))
        print('Top: ' + '{0:.0f}'.format(top))
        print('Face Width: ' + "{0:.0f}".format(width))
        print('Face Height: ' + "{0:.0f}".format(height))

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)

        )
        draw.line(points, fill='#d40000', width=2)

    # プレビューを表示
    image.show()

    # 画像を保存
    image.save('./reko/image.jpg', quality=95)

    print("## image")
    print(image)
    s3_bucket.upload_file("./reko/image.jpg", "image.jpg")

    return len(response['FaceDetails'])

def main():
    bucket="visualization-app-camera"
    photo="reko_test2.jpeg"

    faces_count=show_faces(photo,bucket)
    print("faces detected: " + str(faces_count))


if __name__ == "__main__":
    main()