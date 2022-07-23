var MJID = 0;
window.MJ =
{
	fi:false, // finish streaming
	sh : 480,
	dx : 0,
	dy : 0,
	dw : 960,
	dh : 540,
	blob : 0 ,
	urlCreator  : 0,
	imageUrl  : 0,
	canvas  : 0,
	context  : 0,
	imageObj  : 0,
	oReq : 0,
	url : 0,
	id : 0,

	//fetches BINARY FILES synchronously using XMLHttpRequest
	drawLine:function(cali_x ,cali_y ){
		MJ.canvas = document.getElementById('fisheye_jpeg');
		MJ.context = MJ.canvas.getContext('2d');

//		console.log( cali_x +" "+cali_y );
		
		MJ.context.beginPath();
		MJ.context.setLineDash([5,2]);
		MJ.context.strokStyle = 4 ;
		MJ.context.strokeStyle = '#353535' ;		
		MJ.context.moveTo(160,0);
		MJ.context.lineTo(160,240);
		MJ.context.stroke();	
		
		MJ.context.beginPath();
		MJ.context.setLineDash([5,2]);
		MJ.context.strokStyle = 4 ;
		MJ.context.strokeStyle = '#353535' ;
		MJ.context.moveTo(0,120);
		MJ.context.lineTo(320,120);
		MJ.context.stroke();		

		MJ.context.beginPath();	
		MJ.context.getLineDash();
		MJ.context.setLineDash([0]);
		MJ.context.strokeStyle = '#ff0000' ;
		MJ.context.moveTo(cali_x,0);
		MJ.context.lineTo(cali_x,240);
		MJ.context.stroke();		
		
		MJ.context.beginPath();
		MJ.context.strokeStyle = '#ff0000' ;		
		MJ.context.moveTo(0,cali_y);
		MJ.context.lineTo(320, cali_y);
		MJ.context.stroke();	
	
	},
	draw:function(blob, mode){	
		if( mode == "cali_center" ) {
            MJ.canvas = document.getElementById('fisheye_jpeg');
        }        
        else if(!document.getElementById('jpeg')){
            var id_name="jpeg"+MJID;
            MJ.canvas = document.getElementById(id_name);
        }
		else {
            MJ.canvas = document.getElementById('jpeg');
        }

		if( MJ.canvas == null){
			MJ.fi = true;
			return 0;
		}
	    var deferred = $.Deferred();
		MJ.context = MJ.canvas.getContext('2d');
		
		MJ.imageObj.onload = function(evt){			
			MJ.context.drawImage(MJ.imageObj,0,0,0,0);
			if( mode == "cali_center" ){
				MJ.context.drawImage(MJ.imageObj, 0,0,320,240);	
			}
			else MJ.context.drawImage(MJ.imageObj,MJ.dx,MJ.dy,MJ.dw,MJ.dh);
			
			MJ.urlCreator.revokeObjectURL(MJ.imageObj.src);
			MJ.imageObj.src = "" ;
			MJ.context = "";
	        deferred.resolve();		   
		};
		try{
			MJ.imageObj.src = MJ.urlCreator.createObjectURL( blob );
		}
		catch(e){
			console.log(e);
		}
		return deferred.promise();
	},
	
	load_url_blob_3:function(){
		setTimeout(function() { // UDP technology
			if(!document.getElementById('jpeg')){
        MJ.url ='/cgi-bin/video?id='+ (MJID+1) + '&_=' + new Date().getTime();
      }else{
    		MJ.url ='/cgi-bin/video?id='+ MJ.id + '&_=' + new Date().getTime();
			}
			if(!MJ.fi)
				MJ.oReq.send(null);
		}, 25); // UDP technology
	}, 
	streaming:function()
	{
    if(document.getElementById('jpeg')){
      MJID = MJ.id;
    }
		var deferred = $.Deferred();
		MJ.imageObj = "" ;
		MJ.imageObj = new Image();
		MJ.oReq = "";
		MJ.oReq = new XMLHttpRequest();
		MJ.url ='/cgi-bin/video.cgi?id='+MJID + '&_=' + new Date().getTime();
		MJ.oReq.open("GET", MJ.url, true);
		MJ.oReq.responseType = "blob";	
		MJ.oReq.onload = function(e) {
      MJ.draw(MJ.oReq.response);
			MJ.oReq.open("GET", MJ.url, true,"","");
        if(!document.getElementById('jpeg')){
          if(capInfo.camera_type == "PREDATOR_CLIENT" || capInfo.camera_type == "PREDATOR_SERVER") {
            MJ.id++;
          }
          MJID++;
          if((capInfo.video_in == 4 && MJID == 4) || (capInfo.video_in == 2 && MJID == 2)) MJID = 0;
          if(MJ.id > (capInfo.video_in-1)){
            MJ.id=0;
            MJID=0;
          }
        }
			requestAnimationFrame(MJ.load_url_blob_3);
			return 0 ;
		};
			
		MJ.urlCreator = window.URL || window.webkitURL;
		MJ.load_url_blob_3();			
	} ,
	ajax:function(){
		var deferred = $.Deferred();
		MJ.imageObj = "" ;
		MJ.imageObj = new Image();
		MJ.oReq = "";
		MJ.oReq = new XMLHttpRequest();
		MJ.url ='/cgi-bin/video.cgi?id='+ MJ.id + '&_=' + new Date().getTime();
		MJ.oReq.open("GET", MJ.url, true,"","");
		MJ.oReq.responseType = "blob";	
		MJ.oReq.onload = function(e) {
			MJ.blob = MJ.oReq.response; 
			deferred.resolve();	
		};
		MJ.urlCreator = window.URL || window.webkitURL;	
		MJ.oReq.send(null);
		return deferred.promise();

	},
	change_video_id : function(id) {
		if(typeof(id) == 'undefined'){
			return false;
		}
		MJ.id = id;
		return true;
	}
};
 
