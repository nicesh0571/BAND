from django.shortcuts import render
from django.http import StreamingHttpResponse
from ultralytics import YOLO
import cv2
from django.templatetags.static import static

model = YOLO("yolov8/best.pt")
# 핸드폰 카메라 스트림 URL
#cap = cv2.VideoCapture("http://192.168.0.100:8554/video")
cap = cv2.VideoCapture(0)


image_paths = {
    "Abrasions": "images/Abrasions.png",
    "Bruises": "images/Bruises.png",
    "Burns": "images/Burns.png",
    "Cut": "images/Cut.png",
    "Laseration": "images/Laseration.png",
    "Unknown": "images/Unknown.png",
}
# 상처별 응급처치 텍스트 사전 정의
treatment_info = {
    "Abrasions": """
🩹 <b>Abrasions (찰과상)</b><br>
- 흐르는 물로 이물질 제거, 생리식염수로 세척<br>
- 출혈 시 압박 지혈, 상처 보호 드레싱<br>
- <b>약품:</b> 포비돈, 후시딘, 마데카솔, 습윤밴드<br>
- <b>대체물품:</b> 깨끗한 생수, 식염수 대용으로 생수 + 소금(0.9%), 멸균된 천 대신 깨끗한 면 티셔츠, 위생 티슈
""",

"Bruises": """
🟣 <b>Bruises (타박상)</b><br>
- 24시간 내 냉찜질, 이후 온찜질<br>
- 통증 심할 땐 휴식 및 고정<br>
- <b>약품:</b> 디클로페낙 겔, 이부프로펜<br>
- <b>대체물품:</b> 얼음팩 대신 냉동채소, 물병에 찬물 담아 수건으로 감싸 사용, 탄력붕대 대신 머플러나 천 조각으로 고정
""",

"Burns": """
🔥 <b>Burns (화상)</b><br>
- 찬물 10~15분 냉각, 물집은 손대지 않기<br>
- 2도 이상 병원 방문<br>
- <b>약품:</b> 실버설파다이아진, 후시딘<br>
- <b>대체물품:</b> 흐르는 찬 수돗물, 차가운 젖은 수건으로 감싸기, 알로에겔 대신 생알로에 잎 즙, 랩(비닐)으로 일시적 보호
""",

"Cut": """
✂️ <b>Cut (베임)</b><br>
- 깨끗한 물로 세척 후 압박 지혈<br>
- 깊은 상처는 병원 봉합<br>
- <b>약품:</b> 포비돈, 후시딘, 박트로반<br>
- <b>대체물품:</b> 깨끗한 생수 + 면 티셔츠로 압박, 수건이나 휴지로 지혈, 테이프 + 거즈 대신 키친타월 + 랩
""",

"Laseration": """
⚡ <b>Laceration (열상)</b><br>
- 이물질 제거, 압박 지혈<br>
- 봉합 필요 시 병원 이동<br>
- <b>약품:</b> 항생제 연고, 습윤 드레싱<br>
- <b>대체물품:</b> 물티슈로 이물 제거, 깨끗한 손수건/마스크로 지혈, 비닐봉지나 랩으로 상처 보호
""",

"Unknown": """
❓ <b>Unknown (불명확)</b><br>
- 정확한 상처 형태 파악 어려움<br>
- 병원 또는 응급실 방문 권장<br>
- 감염/통증/고름 시 즉시 진료<br>
- <b>대체물품:</b> 손 대지 않고 랩, 깨끗한 비닐, 수건 등으로 덮어 보호 후 빠른 병원 방문
"""
}



# 전역 label → 처리 텍스트 공유 변수
current_info = {"label": "Unknown", "text": treatment_info["Unknown"], "image": "images/Unknown.png"}


import time  # 맨 위에 추가

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)[0]
        probs = results.probs.data.cpu().numpy()
        class_names = results.names
        name_prob_pairs = [(class_names[i], prob) for i, prob in enumerate(probs)]
        name_prob_pairs.sort(key=lambda x: x[1], reverse=True)

        top_name, top_prob = name_prob_pairs[0]
        second_name = name_prob_pairs[1][0] if len(name_prob_pairs) > 1 else "Unknown"
        label = second_name if top_name == "Unknown" and top_prob < 0.7 else top_name

        # ✅ 텍스트 + 이미지 갱신
        current_info["label"] = label
        current_info["text"] = treatment_info.get(label, treatment_info["Unknown"])
        current_info["image"] = image_paths.get(label, image_paths["Unknown"])

        # 화면에 표시
        cv2.putText(frame, f'Predicted: {label}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def camera_page(request):
    return render(request, 'Classify/index.html', {  # camera.html → index.html 로 변경
        "label": current_info["label"],
        "treatment_text": current_info["text"],
        "image_url": current_info["image"]   # ✅ 이거 꼭 들어가야 함
    })

from django.http import JsonResponse

def get_label_info(request):
    return JsonResponse({
        "label": current_info["label"],
        "text": current_info["text"],
        "image": current_info["image"]
    })
