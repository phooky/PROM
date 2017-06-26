import QtQuick 2.2
import QtQuick.Controls 1.1

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("ROM Explorer 2")

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    Rectangle {
        id: rectangle1
        color: "#ffffff"
        anchors.fill: parent

        Image {
            id: image1
            smooth: false
            anchors.bottom: byte_width.top
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: parent.top
            source: "qrc:/qtquickplugin/images/template_image.png"
        }

        SpinBox {
            id: byte_width
            y: 433
            prefix: ""
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.bottom: parent.bottom
        }
    }
}
