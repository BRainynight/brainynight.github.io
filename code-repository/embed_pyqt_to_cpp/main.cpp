#include <QApplication>
#include <QPushButton>
#include <PythonQt.h>


int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // Initialize PythonQt
    PythonQt::init();

    // Create a button
    QPushButton button("Hello, PythonQt!");
    button.show();

    // Run a simple Python script
    PythonQtObjectPtr mainContext = PythonQt::self()->getMainModule();
    mainContext.evalScript("print('Hello from Python!')");

    return app.exec();
}
