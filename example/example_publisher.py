# pip install eclipse-zenoh
import zenoh
import ctypes
import time


class ZenohPublisher:
    def __init__(self, topic_name):
        """
        :param topic_name: 토픽명
        """
        # Zenoh 세션 및 퍼블리셔 설정
        self._conf = zenoh.Config()
        self._session = zenoh.open(self._conf)
        self._publisher = self._session.declare_publisher(topic_name)

        self._backlog(f"Declared Publisher on Topic: {topic_name}")

    def publish(self, data: ctypes.Structure):
        """
        ctypes 구조체 데이터를 바이너리로 변환하여 전송합니다.
        :param data: 전송할 ctypes 구조체 인스턴스
        """
        try:
            # 구조체 데이터를 바이트(바이너리)로 변환 (C++의 메모리 레이아웃 그대로)
            binary_data = bytes(data)

            # Zenoh 토픽으로 데이터 발행
            self._publisher.put(binary_data)

        except Exception as e:
            print(f"[Error] 데이터 전송 중 오류 발생: {e}")

    def _backlog(self, log):
        print(f"[BackLog] [Publisher] {log}")

    def close(self):
        """세션 종료"""
        self._session.close()


class SensorData(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int32),
        ("msg", ctypes.c_char * 8)  # char msg[8]
    ]

if __name__ == "__main__":
    # 1. 퍼블리셔 객체 생성
    pub = ZenohPublisher("example")

    # 2. 전송할 데이터 객체 생성
    sensor_msg = SensorData()
    sensor_msg.id = 1
    sensor_msg.msg = b"hello"

    print(f"(중료: Ctrl+C)")

    try:
        count = 1
        while True:
            # 데이터 값 업데이트
            sensor_msg.id = count
            sensor_msg.msg = b"hello"

            # 3. 데이터 전송
            pub.publish(sensor_msg)

            print(f">> [발행] ID: {sensor_msg.id} | msg: {sensor_msg.msg.decode('utf-8')}")

            count += 1
            time.sleep(1)  # 1초 간격으로 전송
    except KeyboardInterrupt:
        pass
    finally:
        pub.close()