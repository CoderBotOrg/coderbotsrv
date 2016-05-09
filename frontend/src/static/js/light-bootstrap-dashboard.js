var searchVisible = 0;
var transparent = true;

var transparentDemo = true;
var fixedTop = false;

var navbar_initialized = false;

$(document).ready(function(){
    window_width = $(window).width();

    // check if there is an image set for the sidebar's background
    lbd.checkSidebarImage();

    // Init navigation toggle for small screens
    if(window_width <= 991){
        lbd.initLeftMenu();
    }

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

// activate collapse right menu when the windows is resized
$(window).resize(function(){
    if($(window).width() <= 991){
        lbd.initLeftMenu();
    }
});

lbd = {
    misc:{
        navbar_menu_visible: 0
    },

    checkSidebarImage: function(){
        $sidebar = $('.sidebar');
        image_src = $sidebar.data('image');

        if(image_src !== undefined){
            sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
            $sidebar.append(sidebar_container);
        }
    },
    initLeftMenu: function(){
         if(!navbar_initialized){

             $toggle = $('.navbar-toggle');

             $toggle.click(function (){
                console.log("click");
                $('#sidebar').css('display', 'visible');
                if(lbd.misc.navbar_menu_visible == 1) {
                    //$('html').removeClass('nav-open');
                    lbd.misc.navbar_menu_visible = 0;
                    //$('#bodyClick').remove();
                    // setTimeout(function(){
                    //    $toggle.removeClass('toggled');
                    // }, 400);

                } else {
                    //setTimeout(function(){
                    //    $toggle.addClass('toggled');
                    //}, 430);

                    //div = '<div id="bodyClick"></div>';
                    //$(div).appendTo("body").click(function() {
                    //    $('html').removeClass('nav-open');
                    //    lbd.misc.navbar_menu_visible = 0;
                    //    $('#bodyClick').remove();
                    //     setTimeout(function(){
                    //        $toggle.removeClass('toggled');
                    //     }, 400);
                    //});

                    //$('html').addClass('nav-open');
                    lbd.misc.navbar_menu_visible = 1;

                }
            });
            navbar_initialized = true;
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
