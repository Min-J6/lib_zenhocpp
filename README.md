# Zenohcpp
* Ubuntu 환경에서 사용할 수 있게 프리빌드된 라이브러리를 사용합니다.
* 사용하기 쉬운 Publisher와 Subscriber 클래스를 지원합니다.

## Dependencies
This project uses the following open-source libraries:
* Zenoh-C - Eclipse Zenoh C API (Apache-2.0 License)
* Zenoh-CPP - Eclipse Zenoh C++ API (Apache-2.0 License)

## 프로젝트 구조
```text
workspace/
├── 3rdparty/
│   └── lib_zenohcpp/
├── main.cpp
└── CMakeLists.txt
```

## 1. 설치
* 예시에서는 3rdparty 디렉토리에서 git clone을 실행합니다
```shell
git clone https://github.com/code2j/lib_zenhocpp.git
```

## 2. CMakeLists.txt
* 프로젝트 메인 CMakeLists.txt에 추가하세요.
```cmake
add_subdirectory(3rdparty/lib_zenohcpp)
target_link_libraries(main PRIVATE libzenoh)
```

## 3. 빌드
```c++
mkfir build && cd build
cmake ..
make
```
