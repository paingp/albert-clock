// os includes
#include <iostream>
#include <chrono>

// local includes
#include "myapp.h"

int main(int argc, char* argv[]) {
    MyApp* app = new MyApp(argc, argv);

    // auto now = std::chrono::system_clock::now();
    // std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    // app->gui_obj->updateTimeLabel(std::ctime(&now_c));

    return app->exec();
}
