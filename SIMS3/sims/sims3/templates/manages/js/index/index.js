/*$(".leftsidebar_box dt").css({"background-color":"#3992d0"});*/
$(".leftsidebar_box dt").css({"background-color":"#AAAAAA"});
$(".leftsidebar_box dt").css({"font-family":"幼圆"});
$(".leftsidebar_box dt img").attr("src","../../image/index/select_xl01.png");
$(function(){
	$(".leftsidebar_box dd").hide();
	$(".leftsidebar_box dt").click(function(){
		$(".leftsidebar_box dt").css({"background-color":"#3992d0"})
		$(this).css({"background-color": "#317eb4"});
		$(this).parent().find('dd').removeClass("menu_chioce");
		$(".leftsidebar_box dt img").attr("src","../../image/index/select_xl01.png");
		$(this).parent().find('img').attr("src","../../image/index/select_xl.png");
		$(".menu_chioce").slideUp(); 
		$(this).parent().find('dd').slideToggle();
		$(this).parent().find('dd').addClass("menu_chioce");
	});
});
$(function(){
	//菜单点击
	$(".J_menuItem").on('click',function(){
		var url = $(this).attr('href');
		$("#J_iframe").attr('src',url);
		return false;
	});
});