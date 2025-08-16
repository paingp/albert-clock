#ifndef MY_WORKER_H
#define MY_WORKER_H

// os includes
#include <QObject>
#include <QString>

// local includes

class MyWorker : public QObject
{
    Q_OBJECT

    public:

        MyWorker(QObject* parent=nullptr);

        std::string GetMode();
        void updateMode();

    private:

        std::string mode;

        void Initialize();
        
    signals:

        void updateTimeLablSig(QString time_str);
        void updateAnswerLablSig(QString time_str);
};

#endif
