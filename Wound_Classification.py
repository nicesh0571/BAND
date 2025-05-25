import cv2
from ultralytics import YOLO

# 모델 로드 (자신이 학습한 yolov8 모델 경로로 바꾸세요)
model = YOLO('best.pt')  # 예: 'runs/detect/train/weights/best.pt'

# 카메라 열기 (0: 기본 웹캠)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 모델에 프레임 전달 후 예측
    results = model(frame)

    # 결과 시각화 (bounding box가 적용된 이미지)
    annotated_frame = results[0].plot()

    # 프레임 출력
    cv2.imshow('Wound Detection', annotated_frame)

    # q 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
