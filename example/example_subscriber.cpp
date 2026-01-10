#include "zenoh_subscriber.hpp"
#include <iostream>

struct Data {
    int cnt;
    char msg[8];
};

void recived_callback(Data data)
{
    size_t actual_len = strnlen(data.msg, sizeof(data.msg));
    std::string final_msg(data.msg, actual_len);

    std::cout << "[Subscriber] 데이터 받음: "
              << "cnt: " << data.cnt
              << ", msg: " << final_msg << std::endl;
}

int main()
{
    std::string topic_name = "example";
    Subscriber<Data> sub(topic_name);
    sub.on_received = recived_callback;

    std::cout << "(Enter 입력시 종료)\n";
    std::cin.get();


    return 0;

}
