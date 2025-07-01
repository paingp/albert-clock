#ifndef WORKER_H
#define WORKER_H

// os includes
#include <QObject>
#include <QString>

// local includes

class Worker : public QObject {
    Q_OBJECT

    public:

        Worker(QObject* parent=nullptr);

        std::string GetMode();
        void updateMode();

    private:

        std::string mode;
        

    signals:

        void updateTimeLablSig(QString time_str);
        void updateAnswerLablSig(QString time_str);

};

#endif
