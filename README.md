# zenohcpp

## Dependencies
This project uses the following open-source libraries:
* Zenoh-C - Eclipse Zenoh C API (Apache-2.0 License)
* Zenoh-CPP - Eclipse Zenoh C++ API (Apache-2.0 License)


## 1. 설치
```shell

```



## 2. CMakeLists.txt
* 프로젝트 메인 CMakeLists.txt에 추가하세요.
```cmake
add_subdirectory(3rdparty/zenohcpp)
target_link_libraries(main PRIVATE lib_zenoh)
```

## 예제
pub_example.cpp
```shell
#include <iostream>
#include <string>
#include "zenoh_publisher.hpp"
using namespace Zenoh;

struct SensorData {
    int id;
    float temperature;
    float humidity;
};

int main() {
    // 1. Publisher를 생성
    Publisher<SensorData> sensor_publisher("demo/sensor/data");

    // 2. 데이터 설정
    SensorData sensor = { 101, 25.5f, 60.2f };

    // 3. 데이터 Publish
    sensor_publisher.publish(sensor);

    return 0;
}
```
```c++
#include <chrono>
#include <iostream>
#include <string>
#include <thread>

#include "zenoh_subscriber.hpp"
using namespace Zenoh;


struct SensorData {
    int id;
    float temperature;
    float humidity;
};

void on_received_callback(const SensorData& sensor_data) {
    std::cout << "[Subscriber] SensorData: id=" << sensor_data.id << ", temperature=" << sensor_data.temperature
              << ", humidity=" << sensor_data.humidity << std::endl;
}

int main() {
    // 1. Subscriber 객체 생성 (토픽명과 데이터 처리 콜백 전달)
    Subscriber<SensorData> sensor_subscriber("demo/sensor/data");
    sensor_subscriber.on_received = on_received_callback;


    // 2. 프로그램 유지 (이벤트 루프)
    std::cout << "종료하려면 CTRL-C를 누르세요..." << std::endl;
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
```
