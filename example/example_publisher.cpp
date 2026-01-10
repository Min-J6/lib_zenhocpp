#include "zenoh_publisher.hpp"
#include <iostream>
#include <atomic>
#include <thread>


class Timer {
    std::atomic<bool> active{false};
    std::thread worker;
    int interval_ms;

public:
    Timer(int interval_ms) : interval_ms(interval_ms) {}
    ~Timer() { stop(); }

    std::function<void()> on_callback;

    void start()
    {
        if (active)
            return; // 이미 실행 중이면 무시

        active = true;

        worker = std::thread([this]()
        {
            while (active) {
                std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
                if (active && on_callback) on_callback();
            }
        });
    }

    void stop()
    {
        active = false;
        if (worker.joinable()) worker.join();
    }
};

struct Data {
    int cnt;
    char msg[8];
};

int main()
{
    // 퍼블리셔 생성
    std::string topic_name = "example";
    Publisher<Data> pub(topic_name);

    Timer pub_timer(1000); // 1000ms

    pub_timer.on_callback = [&]()
    {
        static int cnt = 0;
        static Data data;
        data.cnt = ++cnt;
        snprintf(data.msg, sizeof(data.msg), "hello");
        pub.publish(data);
        std::cout << "[Publisher] 메세지 발행: "
                  << "cnt: " << data.cnt
                  << ", msg: " << data.msg << std::endl;
    };

    pub_timer.start(); // 타이머 시작

    std::cout << "(Enter 입력시 종료)\n";
    std::cin.get();

    pub_timer.stop(); // 타이머 중지

    return 0;
}