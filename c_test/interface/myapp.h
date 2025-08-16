#ifndef MYAPP_H
#define MYAPP_H

// os includes
#include <QApplication>

// local includes
#include "mywindow.h"

class MyApp : public QApplication
{

    public:

        MyApp(int& argc, char** argv);
        ~MyApp();

    private:

        MyWindow* window_obj;
        Worker* worker;

        void Initialize();
};

#endif
