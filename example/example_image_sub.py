import zenoh
import ctypes
import cv2
import numpy as np
import time

WIDTH = 1920
HEIGHT = 1080
CHANNELS = 3
IMG_SIZE = WIDTH * HEIGHT * CHANNELS

class ImagePacket(ctypes.Structure):
    _fields_ = [
        ("frame_id", ctypes.c_int32),
        ("timestamp", ctypes.c_double), # 보낸 시간
        ("data", ctypes.c_ubyte * IMG_SIZE)
    ]

class ZenohLatencyVisualizer:
    def __init__(self, topic_name):
        self._conf = zenoh.Config()
        self._session = zenoh.open(self._conf)
        self._subscriber = self._session.declare_subscriber(topic_name, self._listener)

        # 지연시간 통계용 변수
        self.latency_sum = 0
        self.count = 0

    def _listener(self, sample):
        try:
            # 1. 수신 시간 기록
            recv_time = time.time()

            # 2. 데이터 복원
            packet = ImagePacket.from_buffer_copy(sample.payload.to_bytes())

            # 3. 지연시간 계산 (단위: ms)
            latency = (recv_time - packet.timestamp) * 1000

            # 통계 업데이트
            self.count += 1
            self.latency_sum += latency
            avg_latency = self.latency_sum / self.count

            # 4. 시각화용 이미지 변환
            img_flat = np.frombuffer(packet.data, dtype=np.uint8)
            frame = img_flat.reshape((HEIGHT, WIDTH, CHANNELS))

            # 이미지 위에 지연시간 표시
            cv2.putText(frame, f"Latency: {latency:.2f} ms", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.putText(frame, f"Avg Latency: {avg_latency:.2f} ms", (50, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

            cv2.imshow("Zenoh Latency Test", frame)

            # 터미널 출력
            if self.count % 10 == 0: # 10프레임마다 한 번씩 출력
                print(f"[Stats] ID: {packet.frame_id} | Current Latency: {latency:.2f}ms | Avg: {avg_latency:.2f}ms")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

        except Exception as e:
            print(f"[Error] {e}")

    def run(self):
        print("Subscribing... Press Ctrl+C to stop.")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            self.close()

    def close(self):
        cv2.destroyAllWindows()
        self._session.close()

if __name__ == "__main__":
    vis = ZenohLatencyVisualizer("rt/camera/raw")
    vis.run()