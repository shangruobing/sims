//
// var lineNum=["å—ç¤¼å£«è·¯ï¼ˆåŒ—æ®µï¼‰","ä¸‰ä¸è€èƒ¡åŒ","æˆæ–¹è¡—","å‰å¸½èƒ¡åŒ","åŒ—å¸½èƒ¡åŒ","ä¸­å¸½èƒ¡åŒ","å®£æ­¦é—¨ä¸œæ²³æ²¿è¡—",
//            "è™ŽåŠè·¯ç¤¾åŒºåŒ—ä¾§è·¯","é‡‘äº•èƒ¡åŒ","å–„æžœèƒ¡åŒè¥¿æ®µ","ç™½çº¸åŠå°å­¦ï¼ˆä¸œé—¨ï¼‰é—¨å‰è·¯","è£å…‰èƒ¡åŒ","å—èœå›­ä¸€æ”¯"];
// var StartPlace=["æœˆå›å—è¡—-é˜œæˆé—¨å¤–å¤§è¡—","ç½—å„¿èƒ¡åŒâ€”å¾·èƒœé—¨å†…å¤§è¡—","å¤å…´é—¨åŒ—é¡ºåŸŽ-å¤ªå¹³æ¡¥å¤§è¡—","èµµç™»ç¦¹è·¯-åŒ—å¸½èƒ¡åŒ",
//                   "å¤§å¸½èƒ¡åŒâ€”å‰å…¬ç”¨èƒ¡åŒ","å‰å…¬ç”¨èƒ¡åŒâ€”å‰å¸½èƒ¡åŒ","é¦™ç‚‰è¥å¤´æ¡â€”â€”é¦™ç‚‰è¥å¤´æ¡",
//            "è™ŽåŠè·¯â€”â€”å¾æ‚²é¸¿ä¸­å­¦","ä¸Šæ–œè¡—â€”â€”è¾¾æ™ºæ¡¥èƒ¡åŒ","æŠ¥å›½å¯ºè¥¿å¤¹é“â€”â€”å¹¿ä¹‰è¡—","ç™½çº¸åŠå°å­¦â€”â€”ç™½å¹¿è·¯",
//            "èµµé”¥å­èƒ¡åŒâ€”â€”å‚¨å­è¥èƒ¡åŒ","å—èœå›­è¡—â€”â€”å¹¿å®‰é—¨å—è¡—"];
// var LongRoad=["1126","260","459.5","186","226.5","145.8","235.5",
//            "255.8","134.5","106.4","98.5","144.7","270"];
//
//         // $.getJSON("busdata.json",function(data){
//         // 		stationNames = data;
//         // 	});//getæœ¬åœ°çš„busdata.jsonæ–‡ä»¶,å¹¶å°†å…¶å€¼èµ‹ç»™å˜é‡stationNames
//         var collect=document.getElementById("type")  //èŽ·å–é“è·¯åç§°çš„å±žæ€§
//         // var old=collect.innerHTML
//         var start=document.getElementById("first")  //èŽ·å–é“è·¯åç§°çš„å±žæ€§
//         // var place=start.innerHTML
//          var Long =document.getElementById("long")  //èŽ·å–é“è·¯åç§°çš„å±žæ€§
//         // var road=Long.innerHTML
//
//         window.onload=function(){
//             var lineNu=" "  //è®¾ç½®æ•°ç»„ä¸ºç©º
//             for(var j=0;j<lineNum.length;j++){
//                 lineNu+='<option>'+lineNum[j]+'</option>';
//             }
//                 collect.innerHTML=old+lineNu;
//                  var StartPla=" "  //è®¾ç½®æ•°ç»„ä¸ºç©º
//             for(var j=0;j<StartPlace.length;j++){
//                 StartPla+='<option>'+StartPlace[j]+'</option>';
//             }
//                 start.innerHTML=place+StartPla;
//                  var LongRo=" "  //è®¾ç½®æ•°ç»„ä¸ºç©º
//             for(var j=0;j<StartPlace.length;j++){
//                LongRo+='<option>'+LongRoad[j]+'</option>';
//             }
//                Long.innerHTML=road+LongRo;
//         }
//
//
//         // $.getJSON("busdata.json",function(data){
//         //      stationNames = data;
//         //  });//getæœ¬åœ°çš„busdata.jsonæ–‡ä»¶,å¹¶å°†å…¶å€¼èµ‹ç»™å˜é‡stationNames
//
//
//