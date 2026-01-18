import zenoh
import ctypes
import time
import cv2
import numpy as np

# --- 설정 ---
WIDTH = 1920
HEIGHT = 1080
CHANNELS = 3
IMG_SIZE = WIDTH * HEIGHT * CHANNELS
TOPIC_NAME = "rt/camera/raw"
FPS = 30
# ------------

class ImagePacket(ctypes.Structure):
    _fields_ = [
        ("frame_id", ctypes.c_int32),
        ("timestamp", ctypes.c_double),
        ("data", ctypes.c_ubyte * IMG_SIZE)
    ]

class ZenohImagePublisher:
    def __init__(self, topic_name):
        self._conf = zenoh.Config()
        # 로컬 네트워크 대역폭 문제 시 아래 주석 해제하여 공유 메모리 사용 시도
        # self._conf.insert_json5("transport/shared_memory/enabled", "true")
        self._session = zenoh.open(self._conf)
        self._publisher = self._session.declare_publisher(topic_name)
        print(f"[Log] Publisher started on: {topic_name}")

    def publish(self, packet: ImagePacket):
        try:
            self._publisher.put(bytes(packet))
        except Exception as e:
            print(f"[Error] Publish failed: {e}")

    def close(self):
        self._session.close()

if __name__ == "__main__":
    pub = ZenohImagePublisher(TOPIC_NAME)

    # 카메라 연결 시도 (실패 시 랜덤 모드)
    cap = cv2.VideoCapture(0)
    use_random = not cap.isOpened()

    if use_random:
        print(f"[Warn] 카메라를 찾을 수 없습니다. {WIDTH}x{HEIGHT} 랜덤 노이즈 이미지를 생성합니다.")
    else:
        print("[Log] 카메라 연결 성공.")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    packet = ImagePacket()
    count = 0

    print("스트리밍 시작... (중지: Ctrl+C)")

    try:
        while True:
            start_time = time.time()

            if not use_random:
                # 카메라에서 읽기
                ret, frame = cap.read()
                if not ret: break
                if frame.shape != (HEIGHT, WIDTH, CHANNELS):
                    frame = cv2.resize(frame, (WIDTH, HEIGHT))
            else:
                # ========================================================
                # [핵심 변경] 랜덤 노이즈 이미지 생성
                # 0~255 사이의 랜덤한 정수로 채워진 (H, W, C) 배열 생성
                # ========================================================
                frame = np.random.randint(0, 256, (HEIGHT, WIDTH, CHANNELS), dtype=np.uint8)

                # 프레임이 실제로 바뀌는지 확인하기 위해 텍스트 추가
                cv2.putText(frame, f"Random Noise Mode - Frame: {count}", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
                cv2.putText(frame, f"Resolution: {WIDTH}x{HEIGHT}", (50, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # 데이터 패킷 채우기
            packet.frame_id = count
            packet.timestamp = time.time()
            # 고속 메모리 복사
            ctypes.memmove(packet.data, frame.ctypes.data, IMG_SIZE)

            # 전송
            pub.publish(packet)
            print(f">> [Sent] Frame: {count}")

            count += 1

            # FPS 유지 로직
            elapsed = time.time() - start_time
            wait_time = max(0.0, (1.0 / FPS) - elapsed)
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n종료 요청됨.")
    finally:
        if not use_random: cap.release()
        pub.close()
        print("Publisher 종료됨.")