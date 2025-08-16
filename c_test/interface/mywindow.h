#ifndef MYWINDOW_H
#define MYWINDOW_H

// os inclues
#include <QWidget>
#include <QLabel>
#include <QString>
#include <QPushButton>
#include <QVBoxLayout>
#include <QFont>

// library includes

class MyWindow : public QWidget 
{
    Q_OBJECT

    public:

        explicit MyWindow(QWidget* parent = nullptr);

    private:

        QLabel* time_label;
        QPushButton* toggle_time_mode_button;
        QPushButton* toggle_diff_mode_button;
        QLabel* answer_label;
        QPushButton* toggle_answer_button;

        QVBoxLayout* layout;

        void Initialize();

    private Q_SLOTS: 

        void updateTimeLabel(QString time_str);
        void updateAnswerLabel(QString ans_str);
};

#endif
