// os includes
#include <iostream>
#include <ctime>

// local includes
#include "myapp.h"

MyApp::MyApp(int& argc, char** argv):
    QApplication(argc, argv)
{
    Initialize();
}

MyApp::~MyApp() 
{
    delete window_obj;
}

void MyApp::Initialize() 
{
    window_obj = new MyWindow();
    window_obj->show();
}
