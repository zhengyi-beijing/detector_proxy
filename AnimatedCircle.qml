import QtQuick 1.0
 
Rectangle {
    id: waitNote
    color:"blue"
    width: 400
    height: 400
    Image {
        anchors.centerIn: parent
        width:400   
        height:400
        
        source: "waitNote.png"
        NumberAnimation on rotation {
            loops: Animation.Infinite
            from: 0
            to: 360
            duration: 1500 // Define the desired rotation speed.
        }
    }
}
