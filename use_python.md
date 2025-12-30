# Python Zenho

## 1. 설치
```shell
pip install eclipse-zenoh
```

## 예제
sub_example.py
```python
import zenoh
import ctypes
import time

# C++의 구조체와 동일한 데이터 구조 정의
class SensorData(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int32),             # 4byte
        ("temperature", ctypes.c_float),    # 4byte
        ("humidity", ctypes.c_float)        # 4byte
    ]

class ZenohSubscriber:
    def __init__(self, topic_name, data_struct):
        """
        :param topic_name: 구독할 토픽명
        :param data_struct: 데이터를 매핑할 ctypes 구조체 클래스
        """
        self.data_struct = data_struct

        # 콜백 함수를 저장할 변수 (기본값은 None)
        self.on_received = None

        # Zenoh 세션 및 구독 설정
        self._conf = zenoh.Config()
        self._session = zenoh.open(self._conf)
        self._subscriber = self._session.declare_subscriber(
            topic_name,
            self._internal_callback
        )

        self._backlog(f"Subscribed Topic: {topic_name}")

    def _internal_callback(self, sample):
        """Zenoh 데이터 수신 콜백 함수"""
        try:
            # 1. 페이로드 획득
            payload = sample.payload.to_bytes()

            # 2. 크기 검사
            if len(payload) != ctypes.sizeof(self.data_struct):
                return

            # 3. 바이트 데이터를 구조체 객체로 변환
            received_data = self.data_struct.from_buffer_copy(payload)

            # 4. on_received에 호출
            if self.on_received is not None:
                self.on_received(received_data)

        except Exception as e:
            print(f"[Error] 수신 데이터 처리 중 오류: {e}")

    def _backlog(self, log):
        """Back Log"""
        print(f"[BackLog] [Subscriber] {log}")

    def close(self):
        """세션 종료"""
        self._session.close()


def on_received_callbck(data: SensorData):
    print(f">> [수신] ID: {data.id} | "
          f"온도: {data.temperature:.2f}°C | "
          f"습도: {data.humidity:.2f}%")


if __name__ == "__main__":
    
    sub = ZenohSubscriber("demo/sensor/data", SensorData)
    sub.on_received = on_received_callbck

    print(f"[{key_expr}] (종료: Ctrl+C)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sub.close()
```


pub_example.py
```python
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
        ("temperature", ctypes.c_float),
        ("humidity", ctypes.c_float)
    ]
    
    
if __name__ == "__main__":
    # 1. 퍼블리셔 객체 생성
    pub = ZenohPublisher("demo/sensor/data")

    # 2. 전송할 데이터 객체 생성
    sensor_msg = SensorData()
    sensor_msg.id = 1
    sensor_msg.temperature = 25.5
    sensor_msg.humidity = 60.2

    print(f"[{topic}] (중료: Ctrl+C)")

    try:
        count = 1
        while True:
            # 데이터 값 업데이트
            sensor_msg.id = count
            sensor_msg.temperature += 0.1 

            # 3. 데이터 전송
            pub.publish(sensor_msg)

            print(f">> [발행] ID: {sensor_msg.id} | 온도: {sensor_msg.temperature:.2f}°C")

            count += 1
            time.sleep(1)  # 1초 간격으로 전송

    except KeyboardInterrupt:
        pass
    finally:
        pub.close()
```