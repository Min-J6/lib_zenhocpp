#pragma once
#include <chrono>
#include <iostream>
#include <string>
#include <functional>
#include <type_traits>
#include <cstring>
#include <thread>

#include "zenoh.hxx"


namespace Zenoh
{
template <typename T>
class Subscriber {
    static_assert(std::is_standard_layout_v<T> && std::is_trivial_v<T>,
                  "데이터 타입은 반드시 POD(Plain Old Data)여야 합니다.");

public:
    std::function<void(const T&)> on_received;

    // 생성자: 토픽명만 받아서 구독을 시작함
    Subscriber(const std::string& topic_name)
        : session_(zenoh::Session::open(zenoh::Config::create_default())),
          subscriber_(session_.declare_subscriber(
              zenoh::KeyExpr(topic_name),
              [this](const zenoh::Sample& sample) { this->_receved_callback(sample); },
              []() {} // on_drop
          ))
    {
        backlog(std::string("Subscribed Topic: " + topic_name));
    }

    ~Subscriber() = default;

    // 복사 및 대입 방지
    Subscriber(const Subscriber&) = delete;
    Subscriber& operator=(const Subscriber&) = delete;


private:
    void _receved_callback(const zenoh::Sample& sample) const
    {
        // 1. 페이로드 획득
        const auto& payload = sample.get_payload();

        if (payload.size() != sizeof(T)) {
            return;
        }

        // 2. 페이로드 데이터를 구조체로 복사
        T received_data;
        std::memcpy(&received_data, payload.as_string().data(), sizeof(T));

        // 3. 콜백 호출
        if (on_received) {
            on_received(received_data);
        }
    }

    void backlog(const std::string& log)
    {
        std::cout << "[BackLog] [Subscriber] " << log << std::endl;
    }

private:
    zenoh::Session session_;
    zenoh::Subscriber<void> subscriber_;
};
} // namespace Zenoh
