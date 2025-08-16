// local includes
#include "myworker.h"

MyWorker::MyWorker(QObject* parent)
{
    Initialize();
}

void MyWorker::Initialize()
{
    startTimeThread();
}

void MyWorker::startTimeThread(uint8_t update_period)
{
    printf("STARTING TIME THREAD");
}

void MyWorker::updateTimeLabelSig(QString time_str)
{
    (void)time_str;
}

void MyWorker::updateAnswerLabelSig(QString ans_str)
{
    (void)ans_str;
}

