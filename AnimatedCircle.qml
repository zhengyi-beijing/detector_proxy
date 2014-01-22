import QtQuick 1.0
 
Rectangle {
    id: waitNote
    color:"blue"
    width: 400
    height: 400
    property alias running: rotation.running
    Image {
        id: animation
        anchors.centerIn: parent
        width:300   
        height:300
        
        source: "res\\X-ray.svg"
        NumberAnimation on rotation {
            id : rotation
            loops:  Animation.Infinite
            from: 0
            to: 360
            duration: 3000 // Define the desired rotation speed.
            running:false
        }
    }
}
