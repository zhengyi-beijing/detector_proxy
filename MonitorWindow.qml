
import QtQuick 1.0
Rectangle {
    id: window
    width: 800
    height: 600
    //anchors.fill: parent
    color: "lightblue"
    /*
    gradient: Gradient {
         GradientStop { position: 0.0; color: "lightblue" }
         GradientStop { position: 1.0; color: "blue" }
        }*/
    function set_scanner_battery_level (level){
        
    }
    
    function set_xray_battery_level(level) {
    }
    
    function set_detector_running (running) {
            runing_status.running = running
    }
    
    function set_detector_connected(connected) {
        if (connected) {
            detector_connection.source = "res\\CONNECTED.png"
        } else {
            detector_connection.source = "res\\UNCONNECTED.png"
        }
    }
    
    function set_xray_connected(connected) {
        if (connected) {
            xray_connection.source = "res\\CONNECTED.png"
        } else {
            xray_connection.source = "res\\UNCONNECTED.png"
        }
    }
    
    function set_speaker_status (on) {
        if(on) {
            speaker.source = "res\\PCS-EN.png"
        } else {
            speaker.source = "res\\PCS-DI.png"
        }
    }

    function set_stop_status (stopped) {
        if (stopped) {
            stopped.source = "res\\ES-EN.png"
        } else {
            stopped.source = "res\\ES-LK.png"
        }
    }

    function set_trace_info(msg) {
        log.text = msg
    }
    

    
    Column {
        spacing: 2
        anchors.fill: parent
        Rectangle {
            id: title_area
            height: parent.height/6
            width : parent.width
            color:"transparent"
            
            Image {
                anchors.fill:parent
                anchors.margins : 20
                anchors.horizontalCenter : title_area.horizontalCenter
                anchors.baseline : title_area.verticalCenter

                id: appons
                source:"res\\Appons-With_R1.png"
            }
        }
        Row {
                width: window.width
                height:window.height - title_area.height
                
                Column {
                    id: side_info
                    width:160
                    height:parent.height
                    Rectangle {
                        height: parent.height //- test.height
                        width:parent.width
                        color: "transparent"
                    }
                    /*
                    Button {
                        id:test
                        height: 100
                        width:parent.width
                        text:"Test"
                        onClicked: {runing_status.running = !runing_status.running }
                    }*/
                }
                
                Item {
                    width:100
                    height:parent.height
                    //color:"yellow"
                    BatteryBar {
                        id: xray_battery
                        width:parent.width
                        height:300
                        anchors.horizontalCenter : parent.horizontalCenter
                        y:parent.y+50
                    }
                    
                    Image { 
                        id: xray_connection
                        height :80
                        width : 80
                        fillMode: Image.PreserveAspectFit
                        source: "res\\CONNECTED.png"
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.bottom:parent.bottom
                    }
                }
                
                Column {
                    width: parent.width-2*xray_battery.width-2*side_info.width
                    height: parent.height
                    AnimatedCircle {
                        id: runing_status
                        color:"transparent"
                        //height:window.height - title_area.height
                        height: parent.height - log.height
                        width: parent.width
                    }
                    
                    Text {
                        id: log
                        height: 40
                        width: parent.width
                        text: "Waiting"
                        font.pointSize:24
                    }
                }
                
                Item {
                    width:100
                    height:parent.height
                    //color:"red"
                    BatteryBar {
                        id: detector_battery
                        width:parent.width
                        height:300
                        anchors.horizontalCenter : parent.horizontalCenter
                    
                        y:parent.y+50
                    }
                    
                    Image { 
                        id: detector_connection
                        height :80
                        width : 80
                        fillMode: Image.PreserveAspectFit
                        source: "res\\CONNECTED.png"
                        anchors.horizontalCenter : parent.horizontalCenter
                        anchors.bottom:parent.bottom
                    }
                }
                
                Item {
                    width:side_info.width
                    height:parent.height
                    //color:"transparent"
                    Row {
                        id: status_system
                        anchors.bottom:parent.bottom
                        width:parent.width
                        
                        height:80
                        Image { 
                            id: stopped
                            height : 80
                            width : 80
                            fillMode: Image.PreserveAspectFit
                            source: "res\\ES-EN.png"
                            //source: "res\\CONNECTED.png"
                            //anchors.bottom: parent.bottom
                            //anchors.left: parent.anchors.left
                        }

                        Image { 
                            id: speaker
                            height : 80
                            width : 80
                            fillMode: Image.PreserveAspectFit
                            source: "res\\PCS-DI.png"
                            //anchors.bottom: parent.bottom
                            //anchors.left: stopped.anchors.right
                        }
                    }
                }
        }
    }
}
