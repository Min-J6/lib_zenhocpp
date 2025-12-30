# Zenoh C++ 환경 구축 가이드
* 시스템에 직접 설치할 경우 아래의 명령어를 사용해 설치를 진행하세요.

# 1. 필수 도구 및 Rust 설치
```shell
    sudo apt update && sudo apt install -y build-essential cmake git
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
```

# 2. Zenoh-C 설치 (Back-end)
```shell
    cd ~/workspace/test_zenoh
    git clone https://github.com/eclipse-zenoh/zenoh-c.git
    cd zenoh-c && mkdir build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
    # ★ sudo를 붙여야 /usr/local에 설치됩니다.
    sudo cmake --build . --target install -j$(nproc)
```

# 3. Zenoh-CPP 설치 (Front-end)
```shell
    cd ~/workspace/test_zenoh/zenoh-cpp
    mkdir -p build && cd build
    rm -rf * # CMake 설정 및 설치
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
    sudo cmake --build . --target install
```

# 4. CMakeLists.txt 수정
```cmake
find_package(zenohc REQUIRED)     # /usr/local/lib/cmake/zenohc 에서 찾음
find_package(zenohcxx REQUIRED)  # /usr/local/lib/cmake/zenohcxx 에서 찾음

add_executable(main main.cpp)
target_link_libraries(main PRIVATE zenohcxx::zenohc)
```

