#pragma once

#include <iostream>
#include <string>
#include <string_view>
#include "zenoh.hxx"

namespace Zenoh
{
template <typename T>
class Publisher {
    // 컴파일 타임에 T가 POD 타입인지 검사
    static_assert(std::is_standard_layout_v<T> && std::is_trivial_v<T>,
                  "데이터 타입은 반드시 POD(Plain Old Data)여야 합니다.");

public:
    Publisher(const std::string& topic_name)
        : topic_name_(topic_name),
          session_(zenoh::Session::open(zenoh::Config::create_default()))
    {
        backlog(std::string("Published Topic: " + topic_name_));
    }

    ~Publisher() = default;

    // 발행자
    void publish(const T& data) const
    {
        session_.put(topic_name_,
                     zenoh::Bytes(std::string_view(reinterpret_cast<const char*>(&data), sizeof(T))));
    }

    // 복사 및 대입 방지
    Publisher(const Publisher&) = delete;
    Publisher& operator=(const Publisher&) = delete;

private:
    void backlog(const std::string& log)
    {
        std::cout << "[BackLog] [Publisher] " << log << std::endl;
    }

private:
    std::string topic_name_;
    zenoh::Session session_;
};
} // namespace Zenoh

