#ifndef MYWINDOW_H
#define MYWINDOW_H

#pragma once

// os inclues
#include <QWidget>
#include <QLabel>
#include <QString>
#include <QPushButton>
#include <QVBoxLayout>
#include <QFont>

// library includes

class MyWindow : public QWidget {
    Q_OBJECT

   public:

        explicit MyWindow(QWidget* parent = nullptr);

        void updateTimeLabel(QString time_str);
        void updateAnswerLabel(QString time_str);

    private:

        QLabel* time_label;
        QLabel* answer_label;
        QPushButton* toggle_mode_button;
        QPushButton* toggle_answer_button;

        QVBoxLayout* layout;

        void Initialize();
};

#endif
