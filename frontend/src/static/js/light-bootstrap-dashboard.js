"use strict";
var searchVisible = 0;
var transparent = true;

var transparentDemo = true;
var fixedTop = false;

var navbar_initialized = false;

$(document).ready(function(){
    var window_width = $(window).width();

    // check if there is an image set for the sidebar's background
    lbd.checkSidebarImage();

    //  Activate the tooltips
    $('[rel="tooltip"]').tooltip();

    //      Activate the switches with icons
    if($('.switch').length != 0){
        $('.switch')['bootstrapSwitch']();
    }
    //      Activate regular switches
    if($("[data-toggle='switch']").length != 0){
         $("[data-toggle='switch']").wrap('<div class="switch" />').parent().bootstrapSwitch();
    }

    $('.form-control').on("focus", function(){
        $(this).parent('.input-group').addClass("input-group-focus");
    }).on("blur", function(){
        $(this).parent(".input-group").removeClass("input-group-focus");
    });

});

var lbd = {
    misc:{
        navbar_menu_visible: 0
    },

    checkSidebarImage: function(){
        var $sidebar = $('.sidebar');
        var image_src = $sidebar.data('image');
        console.log(image_src);
        if(image_src !== undefined){
            var sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
            $sidebar.append(sidebar_container);
        }
    }
}


// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		clearTimeout(timeout);
		timeout = setTimeout(function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		}, wait);
		if (immediate && !timeout) func.apply(context, args);
	};
};
