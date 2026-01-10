# pip install eclipse-zenoh

import zenoh
import ctypes
import time


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



# C++의 구조체와 동일한 데이터 구조 정의
class SensorData(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int32),
        ("msg", ctypes.c_char * 8)  # char msg[8]
    ]

def on_received_callbck(data: SensorData):
    # byte 데이터를 문자열로 변환 (C의 NULL 문자를 자동으로 처리하기 위해 .split(b'\x00')[0] 사용 권장)
    try:
        clean_msg = data.msg.split(b'\x00')[0].decode('utf-8')
    except UnicodeDecodeError:
        clean_msg = str(data.msg)

    print(f">> [수신] ID: {data.id} | msg: {clean_msg}")


if __name__ == "__main__":

    sub = ZenohSubscriber("example", SensorData)
    sub.on_received = on_received_callbck

    print(f"(종료: Ctrl+C)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sub.close()