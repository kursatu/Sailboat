<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RaspberryPi Remote Control</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="assets/bootstrap.min.css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="assets/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="assets/bootstrap.min.js"></script>
	<script src="assets/jquery.nouislider.min.js"></script>
	<link href="assets/jquery.nouislider.css" rel="stylesheet">  	

  	<style type="text/css">
		.panel-body {height:700px; align="middle" }
		.slider 	{height:100%; width: 70%; margin-left: auto; margin-right: auto}
		.noUi-vertical .noUi-handle {
			width: 110%;
			height: 60px;
			top: -34px
		}
		.col-sm-1 { width: 15%}
		.col-sm-8 { width: 70%}
	</style>	

	
	</head>
  <body>

	<script>
	function onSlide ()
	{
		var jq = $("#"+this.id);
		var pos = Math.round(jq.val())
		var servopos = {position: pos };
		var servostr = JSON.stringify(servopos);
		var areq = {
				type: 'put',
				url: '/servos/'+this.id,
				contentType: 'application/json',
				dataType: "json",
				data: servostr,
				async: false,
				success: function(data){
					}
				}
		$.ajax(areq)			


	}
        function getIntervalFromFPS(fps)
        {
            var nReturns = 500/fps; // double the scan freq
            return(nReturns);
        }
        function fps_slider_onSlide ()
        {
            var jq = $("#fps_slider");
            var pos = jq.val();

            clearInterval(window.timer_id);
            if (pos != 0)
                window.timer_id = setInterval(updateImage, getIntervalFromFPS(pos));
            
        }
	</script>
	<script>
	$(function(){
		var start = [ 0 ];
		var range = { 'min': -90, 	'max': 90 };
		var noUISld = { 	start: start, 
							range: range, 
							orientation: "vertical" ,
							serialization: {lower: [ toolTip ]},
							direction: "rtl",
							step: 1
					   };
		var slider = $('.slider').noUiSlider(noUISld);
		slider.on({slide: onSlide});
                var fps_slider = $("#fps_slider").noUiSlider (
                   { start: [1], range: { 'min': 0, 'max': 10}, orientation: "horizontal",
                     step: 1, serialization: {lower: [ toolTip ]},});
                fps_slider.on({slide: fps_slider_onSlide});
	});
	var toolTip = $.Link({	target: '-tooltip-'	});
	
	window.onload = function() {
            timer_id = setInterval(updateImage, getIntervalFromFPS(1));
        }



	function updateImage() {
                
		var image = document.getElementById("camera_img");
                if (image.complete)
                    image.src = image.src.split("?")[0] + "?" + new Date().getTime();
	}
	
	</script>

      <div class="row" >
        <div class="col-sm-1" >
          <div class="panel panel-default">

            <div class="panel-body servo-panel-body">
              	<div class="slider" id="1" ></div>
            </div>
          </div>

        </div>

        <div class="col-sm-8" >
          <div class="panel panel-default">
            <div class="panel-body">
			<img src="/camera/capture.jpg" style="display: block; margin-left: auto; margin-right: auto; height: 100%" id="camera_img" >
              <div class="fps_slider" id="fps_slider" ></div>                          
             </div>
          </div>
 
        </div>

        <div class="col-sm-1">
          <div class="panel panel-default">
            <div class="panel-body servo-panel-body">
			   <div class="slider" id="2" ></div>
            </div>
          </div>

        </div>
      </div>

	  
  </body>
</html>
