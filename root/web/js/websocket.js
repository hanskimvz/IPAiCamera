var j = 0 ;
var SendBuffer = 19200 ;  // 4400 , 8800 , 9600
var uint8View ;
var AduioBuffer;
var blob_count = 0 ;
var blobsize ;
var timeA , timeB  ;
var calcountflag = 0;

function captureUserMedia(mediaConstraints, successCallback, errorCallback) {
	navigator.mediaDevices.getUserMedia(mediaConstraints).then(successCallback).catch(errorCallback);
}

var mediaConstraints = {
    audio: true
};
function init(){	
	console.log( "init():"+ (Date.now() - timeB ));	
	timeB = Date.now();
	uint8View = new Uint8Array(AduioBuffer);
	blob_count = 0 ;
	j= 0 ;
	SendtoIpnc();
}
function SendtoIpnc(){			
	console.log( "sysc:"+blob_count+" time:" +(Date.now() - timeA) );	
	timeA = Date.now();

	var buffer = new ArrayBuffer(SendBuffer);			
	var Txbuffer = new Uint8Array(buffer);	
	
	var interval = 5 ;
	if(  blob_count < interval ){
		for(i=0 ; i < SendBuffer ; i++){
				Txbuffer[i] = uint8View[j+i];
		}
		websocketMic.send(Txbuffer);		
		console.log( Txbuffer );
	}
	j = j+SendBuffer;
	blob_count++ ;

	if( calcountflag == 5){
		clearTimeout(audio_timeout);	
		calcountflag = 0 ;
	}
	calcountflag++ ;
	audio_timeout = setTimeout( "SendtoIpnc();", 1000/6 ) ;		
}
function SendMic() {
	uint8View = new Uint8Array(SendBuffer);
	SendtoIpnc();
}
var mediaRecorder;

function onMdieaStop(){
//	mediaRecorder.stream.stop();
	mediaRecorder.stop();
	clearTimeout(audio_timeout);	
	mediaRecorder = undefined ;
}
var audio ;
var localmidea ;
function onMediaSuccess(stream) {
    audio = document.createElement('audio');
  
    audio = mergeProps(audio, {
        controls: true,
        muted: true,
        src: URL.createObjectURL(stream)
    });
    audio.play();

    audiosContainer.appendChild(audio);
    audiosContainer.appendChild(document.createElement('hr'));

    mediaRecorder = new MediaStreamRecorder(stream);
    mediaRecorder.stream = stream;
    
    mediaRecorder.mimeType = 'audio/pcm';

    // don't force any mimeType; use above "recorderType" instead.
    // mediaRecorder.mimeType = 'audio/webm'; // audio/ogg or audio/wav or audio/webm

    // mediaRecorder.audioChannels = !!document.getElementById('left-channel').checked ? 1 : 2;
    
    mediaRecorder.audioChannels  = 1 ;
  
//  var fileReader = new FileReaderSync();
    mediaRecorder.ondataavailable = function(blob) {		
		var fileReader = new FileReader();
		fileReader.onload = function() {
			AduioBuffer = this.result ;
			init() ;
		};
		fileReader.readAsArrayBuffer(blob);		
		blobsize = blob.size ;
		return 0;
		console.log("size:"+ bytesToSize(blob.size));
    };
    timeInterval  = 1000;  // 500 , 1000
    mediaRecorder.start(timeInterval);

//  get blob after specific time interval
}

function onMediaError(e) {
    console.error('media error', e);
}

var audiosContainer = document.getElementById('audios-container');
var index = 1;

// below function via: http://goo.gl/B3ae8c
function bytesToSize(bytes) {
    var k = 1000;
    var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Bytes';
    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(k)), 10);
    return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i];
}

// below function via: http://goo.gl/6QNDcI
function getTimeLength(milliseconds) {
    var data = new Date(milliseconds);
    return data.getUTCHours() + " hours, " + data.getUTCMinutes() + " minutes and " + data.getUTCSeconds() + " second(s)";
}

window.onbeforeunload = function() {
 //   document.querySelector('#start-recording').disabled = false;
};