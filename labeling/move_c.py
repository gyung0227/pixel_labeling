import cv2
import os

# 디렉토리 경로 설정
input_dir = "/home/gu/code/labeling/copy"
output_dir = "/home/gu/code/labeling/c_result"

# 결과 디렉토리가 없다면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# (0, 0, 255) 픽셀을 오른쪽으로 (1080 - 840)만큼 이동하는 함수
def move_pixels(image, shift):
    height, width, channels = image.shape
    new_image = image.copy()
    new_image[:, shift:] = image[:, :width - shift]
    new_image[:, :shift] = (0, 0, 0)  # 오른쪽으로 이동된 부분을 (0, 0, 255)로 채움
    #new_image[:, :width - shift] = image[:, shift:]
    #new_image[:, width - shift:] = (0, 0, 0)  # 오른쪽으로 이동된 부분을 (0, 0, 255)로 채움
    return new_image

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)
    image = cv2.imread(image_path)
    
    if image is not None:
        # (0, 0, 255) 픽셀을 오른쪽으로 (1080 - 840)만큼 이동
        shifted_image = move_pixels(image, 293)
         # 원본 이미지와 새로 생성된 이미지를 합치기
        combined_image = image+shifted_image
        # 결과 이미지 저장
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, combined_image)
        print(f"Processed and saved: {output_path}")
    else:
        print(f"Failed to load image: {image_path}")

