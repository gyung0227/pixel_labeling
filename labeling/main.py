import cv2
import numpy as np
import glob
import os

# 변수 초기화
image = None
drawing = False  # 마우스 드래깅 여부
mode = True  # 그림을 그릴지 지우기 모드 여부 (True: 그리기, False: 지우기)
ix, iy = -1, -1  # 클릭한 좌표
points = []  # 마우스로 찍은 점을 저장할 리스트
backup_image = None  # 이미지 백업

pixel_width = 20
pixel_color = (0, 0, 255)
pixel_range_l = (0, 0, 200)
pixel_range_h = (100, 100, 255)
# 그리드 생성 함수
def draw_grid(image, grid_size):
    # 수직 라인 그리기
    for x in range(0, image.shape[1], grid_size):
        cv2.line(image, (x, 0), (x, image.shape[0]), (0, 255, 0), 1)
    
    # 수평 라인 그리기
    for y in range(0, image.shape[0], grid_size):
        cv2.line(image, (0, y), (image.shape[1], y), (0, 255, 0), 1)

# 마우스 이벤트 콜백 함수
def draw_line(event, x, y, flags, param):
    global ix, iy, drawing, mode, image, backup_image

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) > 0:
            # 이전 점과 현재 점을 선으로 연결
            cv2.line(image, points[-1], (x, y), pixel_color, pixel_width)
        points.append((x, y))
        backup_image = image.copy()
# 이미지 초기화 함수
def reset_image():
    global image, points, backup_image
    if backup_image is not None:
        image = backup_image.copy()
        points = []

# 이미지 파일 경로 리스트 가져오기 및 이름 순으로 정렬
img_files = sorted(glob.glob('/home/gu/code/labeling/input/*.jpg'))

current_image_index = 0

# 현재 실행 파일의 경로를 가져오고, 결과 이미지를 저장할 디렉토리 경로 생성
current_dir = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(current_dir, "result")

# 결과 디렉토리가 없다면 생성
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# OpenCV 윈도우 생성 및 마우스 콜백 함수 연결
cv2.namedWindow("Labeling Tool")
cv2.setMouseCallback("Labeling Tool", draw_line)

while True:
    if image is None:
        if current_image_index >= len(img_files):
            break  # 모든 이미지가 처리되면 종료
        image_path = img_files[current_image_index]
        image = cv2.imread(image_path)
        if image is not None:
            print(f"Processing image: {image_path}")
            # 그리드 그리기
            draw_grid(image, 40)  # 40픽셀 간격의 그리드 생성
            backup_image = image.copy()
        else:
            print(f"Failed to load image: {image_path}")
            current_image_index += 1
            continue

    cv2.imshow("Labeling Tool", image)
    key = cv2.waitKey(1)

    if key == ord('m'):
        mode = not mode  # 모드 전환 (그리기 또는 지우기)

    if key == ord('s'):
        # save image
        # 결과 디렉토리에 현재 이미지와 같은 이름으로 저장
        image_name = os.path.basename(img_files[current_image_index])
        
        # 빨간색 부분만 추출하여 저장
        red_mask = cv2.inRange(image, (pixel_range_l, pixel_range_h))  # 빨간색 범위 설정
        red_region = cv2.bitwise_and(image, image, mask=red_mask)
        output_image_path = os.path.join(result_dir, image_name)
        cv2.imwrite(output_image_path, red_region)
        print(f"Saved labelled image as {output_image_path}")

    if key == ord(' '):
        # next image
        image = None
        points = []  # 다음 이미지로 이동할 때 이전 점 초기화
        current_image_index += 1

    if key == ord('c'):
        # "c" back to the previous image
        current_image_index -= 1
        if current_image_index < 0:
            current_image_index = 0
        image = None
        points = []  # 이전 이미지로 이동할 때 이전 점 초기화

    if key == ord('z'):
        # "z" point initialize
        if backup_image is not None:
            image = backup_image
            points = []  # 복원 시 이전 점 초기화

    if key == 27:
        break

cv2.destroyAllWindows()


