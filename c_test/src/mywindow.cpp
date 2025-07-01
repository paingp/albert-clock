// os includes
#include <iostream>
#include <ctime>

// local includes
#include "mywindow.h"

MyWindow::MyWindow(QWidget* parent):
    QWidget(parent)
{
    Initialize();
}

void MyWindow::updateTimeLabel(QString time_str) {
    time_label->setText(time_str);
}

void MyWindow::updateAnswerLabel(QString time_str) {
    answer_label->setText(time_str);
}

void MyWindow::Initialize() {
    // set up window
    this->setWindowTitle("Albert Clock");
    this->setGeometry(200, 200, 800, 400);

    // WIDGETS
    // time label
    time_label = new QLabel("time_label", this);
    time_label->setFont(QFont("Arial", 40));
    time_label->setGeometry(0,0,500,100);

    // answer label
    answer_label = new QLabel("answer_label", this);
    answer_label->setFont(QFont("Arial", 40));
    answer_label->setGeometry(0,0,500,100);

    // toggle mode (am/pm vs military)
    toggle_mode_button = new QPushButton("Change Mode", this);
    toggle_mode_button->setCheckable(true);

    // toggle answer string
    toggle_answer_button = new QPushButton("Show Answer", this);
    toggle_answer_button->setCheckable(true);

    // add all widgets to layout
    layout = new QVBoxLayout();
    layout->addWidget(time_label);
    layout->addWidget(answer_label);
    layout->addWidget(toggle_mode_button);
    layout->addWidget(toggle_answer_button);

    // set layout
    this->setLayout(layout);
}
