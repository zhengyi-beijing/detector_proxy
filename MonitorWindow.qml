
import QtQuick 1.0
Rectangle {
    id: window
    width: 1024
    height: 768
    //anchors.fill: parent
    color: "green"
    gradient: Gradient {
         GradientStop { position: 0.0; color: "greenyellow" }
         GradientStop { position: 1.0; color: "green" }
        }
    function set_scanner_battery_level (level){
        
    }
    
    function set_xray_battery_level(level) {
    }
    
    function set_detector_running (running) {
    
    }
    
    function set_detector_connected(connected) {
    }
    
    function set_client_connected(connected) {
    }
    
    function set_trace_info(msg) {
    }
    
    function set_bandwidth() {
    }
    
    Column {
        spacing: 2
        anchors.fill: parent
        Rectangle {
            id: title_area
            height: parent.height/6
            width : parent.width
            color:"transparent"
            Text {
                //anchors.centerIn: parent
                anchors.horizontalCenter : title_area.horizontalCenter
                anchors.baseline : title_area.verticalCenter
                height : parent.height
                text: "Appons"
                font.family: "Helvetica"
                color: "white"
                font.pointSize: 48
                style: Text.Outline
            }
        }
        Row {
                width: window.width
                height:window.height - title_area.height-info_area.height
            
                BatteryBar {
                    id:battery1
                    width:parent.width/5
                    height:parent.height
                }
                AnimatedCircle {
                    id: runing_status
                    color:"transparent"
                    //height:window.height - title_area.height
                    height:parent.height
                    width:parent.width-2*battery1.width
                }
                
                BatteryBar {
                    id:battery2
                    width:parent.width/5
                    height:parent.height 
                }
        }
        
        Rectangle {
            id: info_area
            height: parent.height/8
            width : parent.width
            color:"transparent"
            Flow {
                anchors.fill: parent
                anchors.margins:4
                Button {
                    height: parent.height
                    width:200
                    text:"Test"
                    onClicked: {runing_status.running = !runing_status.running }
                }
                Text { text: "Detector"; font.pixelSize: 40 }
                Text { id:detector_status ;text: "Waiting"; font.pixelSize: 40 }
                Text { text: "Client"; font.pixelSize: 40 }
                Text { id: client_status; text: "Waiting"; font.pixelSize: 40 }
                Text { text: "bandwidth"; font.pixelSize: 40 }
                Text { id :bandwidth; text: "0"; font.pixelSize: 40 }
            }
        }
    }
}
