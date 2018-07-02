(function($) {
    "use strict";
  
    /*--------------------
    Header Dropdown
    --------------------*/ 
    $('.nav>li>a>i, .dropdown-submenu>a>i').click(function() {
        $(this).closest('.dropdown').siblings().removeClass('open');
        $(this).closest('.dropdown').toggleClass('open');  
        return false; 
    });     

    /* -------------------
    Scroll functions
    ---------------------*/
    $(window).scroll(function(){
        parallax();
        /* -------------------
        Header Animation
        ---------------------*/
        if ($(this).scrollTop() > 30){   
            $('nav').addClass("small");
            $('.secondary-header').addClass("fixed");
        }
        else { 
            $('nav').removeClass("small");
            $('.secondary-header').removeClass("fixed");
        }
        /* -------------------
        Back to top button popup
        ---------------------*/
        if ($(window).scrollTop() > 400){
            $("#back-to-top").stop().animate({ bottom:'16px' },300,'easeInOutCubic')
        } 
        else {
            $("#back-to-top").stop().animate({ bottom:'-50px' },300,'easeInOutCubic')
        }
    });
    /* -------------------
    Home Parallax
    ---------------------*/ 
    function parallax(){
        var scrolled = $(window).scrollTop();
        if ($(window).width() > 992) {
            $('.hero-parallax-fullscreen,.hero-parallax-fullwidth,.page-hero-parallax').css('top',-(scrolled*0.4)+'px'); 
            $('.hero-container').css('top',-(scrolled*0.2)+'px'); 
            $('.scroll-opacity').css('opacity',1-(scrolled*.00105)); 
        };
    }; 
 
    /* -------------------
    Lightbox
    ---------------------*/ 
    $(".gallery-item").magnificPopup({
        type: 'image',
        gallery: { enabled: true },
        mainClass: 'my-mfp-slide-bottom'
    }); 
    // Video Popup
    $('.popup-youtube,.popup-vimeo,.popup-gmaps').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false, 
        fixedContentPos: false
    }); 

    /* -------------------
    Search Modal
    ---------------------*/   
    $('.popup-with-zoom-anim').magnificPopup({
        type: 'inline',
        fixedContentPos: false,
        fixedBgPos: true,
        overflowY: 'auto',
        closeBtnInside: true,
        preloader: false,
        midClick: true,
        removalDelay: 300,
        mainClass: 'my-mfp-slide-bottom'
    });  
    
    $('.search').click(function(){ 
        setTimeout ( function timeoutFunction () { 
            $('#search-modal-input').focus();
        }, 100);
    });
     
    /* -------------------
    Smooth scrolling to anchor
    ---------------------*/
    $('.scroll-btn,.btn-scroll').bind('click', function(event) {
        var $anchor = $(this);
        
        if ($(window).width() > 992) {
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 53
            }, 1000, 'easeInOutExpo');
            event.preventDefault();
        } else {
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top + 5
            }, 1000, 'easeInOutExpo');
            event.preventDefault();
        }
    }); 

    /* -------------------
    Owl Slider callings
    ---------------------*/ 
    $(".hero-slider").owlCarousel({
        autoPlay : true,
        navigation : true,
        navigationText: [
          "<img src='img/assets/slider-left-thin-arrow.png'>",
          "<img src='img/assets/slider-right-thin-arrow.png'>"
        ],
        slideSpeed : 300,
        paginationSpeed : 400,
        singleItem: true,
        items:1,
        autoHeight: true,  
        addClassActive: true, 
        beforeMove: function(){
            // BEFORE going to the next slide (hide captions) 
        }, 
        afterMove: function(){
            // AFTER going to next slide (show captions)   
        }
    }); 
 
    $(".image-slider1,.image-slider2,.image-slider5,.image-slider6,.image-slider7").owlCarousel({
        navigation : true,
        navigationText: [
          "<img src='img/assets/slider-left-thin-arrow.png'>",
          "<img src='img/assets/slider-right-thin-arrow.png'>"
        ],
        slideSpeed : 300,
        pagination: true,
        paginationSpeed : 400,
        singleItem: true,
        items:1,
        autoHeight: true,  
        addClassActive: true
    });
 
    $(".image-slider3,.image-slider4").owlCarousel({
        navigation : false,  
        pagination: true,
        paginationSpeed : 400,
        singleItem: true,
        items:1,
        autoHeight: true,  
        addClassActive: true
    });
      


    $("#owl-music").owlCarousel({
        autoPlay : true,
        items: 3, 
        pagination: false,
        navigation: false
    });

    $("#clients-slider").owlCarousel({
        autoPlay : true,
        items: 3, 
        pagination: true,
        navigation: false
    });
    
    $("#clients-slider-2").owlCarousel({
        autoPlay : true,
        items: 6, 
        pagination: false,
        navigation: false
    });
     
    $("#quote-slider").owlCarousel({
        autoPlay : false,
        singleItem : true,
        pagination: false,
        navigation: false
    });

    $("#owl-testimonials").owlCarousel({
        autoPlay : true,
        singleItem : true,
        pagination: true,
        navigation: false
    });

    $("#project-slider").owlCarousel({
        autoPlay : true,
        singleItem : true,
        pagination: false,
        navigation:true,
        navigationText: [
          "<i class='ion-ios-arrow-left size-2x'></i>",
          "<i class='ion-ios-arrow-right size-2x'></i>"
          ],
    }); 

    $("#blog-slider").owlCarousel({ 
        autoPlay : true,
        singleItem : true,
        pagination: false,
        navigation: false,
    });   
    
    $("#owl-slider1").owlCarousel({
        autoPlay : false,
        singleItem : true,
        pagination: false,
        navigation: false
    });
    
    $("#slider-features-1,#slider-features-2").owlCarousel({
        autoPlay : false,
        items: 3,
        pagination: false,
        navigation: false
    });
     
    /* -------------------
    Contact form
    ---------------------*/
    $('#contactform').submit(function(){
		var action = $(this).attr('action');
		$("#message").slideUp(250,function() {
            $('#message').hide();
            $('#submit')
                .after('<img src="img/assets/contact-form-loader.gif" class="loader" />')
                .attr('disabled','disabled');
            $.post(action, {
                name: $('#name').val(),
                email: $('#email').val(), 
                comments: $('#comments').val(),
            },
                function(data){
                    document.getElementById('message').innerHTML = data;
                    $('#message').slideDown(250);
                    $('#contactform img.loader').fadeOut('slow',function(){$(this).remove()});
                    $('#submit').removeAttr('disabled');
                    if(data.match('success') != null) $('#contactform').slideUp(850, 'easeInOutExpo');
                }
            );
		});
		return false;
	});
    
    /* -------------------
    Subscribe form
    ---------------------*/ 
    $('#subscribe-form,#subscribe-form2').on( 'submit', function( e ) {
        e.preventDefault();
        var $el = $( this ),
            $alert = $el.find( '.form-validation' ),
            $submit = $el.find( 'button' ),
            action = $el.attr( 'action' );
        $submit.button( 'loading' );
        $alert.removeClass( 'alert-danger alert-success' );
        $alert.html( '' );
        $.ajax({
            type     : 'POST',
            url      : action,
            data     : $el.serialize() + '&ajax=1',
            dataType : 'JSON',
            success  : function( response ) {
                if ( response.status == 'error' ) {
                    $alert.html( response.message );
                    $alert.addClass( 'alert-danger' ).fadeIn( 500 );
                } 
                else {
                    $el.trigger( 'reset' );
                    $alert.html( response.message );
                    $alert.addClass( 'alert-success' ).fadeIn( 500 );
                }
                $submit.button( 'reset' );
            },
        })
    });
    
    /* --------------------
    Google Maps
    --------------------- */ 

    /*-Google Map 1-*/
    $(".map1").gmap3({
        marker:{     
        address:"38.740527, -79.443050", 
        options:{ icon: "img/assets/marker.png"}},
        map:{
        options:{
        styles: [{ stylers: [{ "saturation": -20 }, { "gamma": 1.2 }, { "lightness": 10 }] }],
        zoom:11,
        scrollwheel:!1,
        draggable:!0
        }}
    });
            
    /*-Google Map 2-*/
    $(".map2").gmap3({
        marker:{     
        address:"44 W 66th St, New York, NY", 
        options:{ icon: "img/assets/marker.png"}},
        map:{
        options:{
        styles:[{featureType:"all",elementType:"labels.text.fill",stylers:[{saturation:36},{color:"#000000"},{lightness:40}]},{featureType:"all",elementType:"labels.text.stroke",stylers:[{visibility:"on"},{color:"#000000"},{lightness:16}]},{featureType:"all",elementType:"labels.icon",stylers:[{visibility:"off"}]},{featureType:"administrative",elementType:"geometry.fill",stylers:[{color:"#000000"},{lightness:20}]},{featureType:"administrative",elementType:"geometry.stroke",stylers:[{color:"#000000"},{lightness:17},{weight:1.2}]},{featureType:"landscape",elementType:"geometry",stylers:[{color:"#000000"},{lightness:20}]},{featureType:"poi",elementType:"geometry",stylers:[{color:"#000000"},{lightness:21}]},{featureType:"road.highway",elementType:"geometry.fill",stylers:[{color:"#000000"},{lightness:17}]},{featureType:"road.highway",elementType:"geometry.stroke",stylers:[{color:"#000000"},{lightness:29},{weight:.2}]},{featureType:"road.arterial",elementType:"geometry",stylers:[{color:"#000000"},{lightness:18}]},{featureType:"road.local",elementType:"geometry",stylers:[{color:"#000000"},{lightness:16}]},{featureType:"transit",elementType:"geometry",stylers:[{color:"#000000"},{lightness:19}]},{featureType:"water",elementType:"geometry",stylers:[{color:"#000000"},{lightness:17}]}],
        zoom:13,
        scrollwheel:!1,
        draggable:!0
        }}
    });
            
    /*-Google Map 3-*/
    $(".map3").gmap3({
        marker:{     
        address:"44 W 66th St, New York, NY", 
        options:{ icon: "img/assets/marker.png"}},
        map:{
        options:{
        styles: [{ stylers: [{ "saturation": -100 }, { "gamma": 2 }, { "lightness": 14 }] }],
        zoom: 15,
        scrollwheel:false,
        draggable: true }
        }
    });

    /* -------------------
    Animated progress bars
    ---------------------*/
    $('.progress-bars,.progress-bars-2,.progress-bars-3,.progress-bars-4').waypoint(function() {
       $('.progress').each(function(){
            $(this).find('.progress-bar').animate({
                width:$(this).attr('data-percent')
            },800);
        });
        }, { offset: '100%',
             triggerOnce: true 
    });

    /* -------------------
    Fun facts counter
    ---------------------*/
    $('.counter').counterUp({
        delay: 8,
        time: 1400
    });

    /* -------------------
    Portfolio
    ---------------------*/ 
    $(window).load(function(){
        var $container = $('.portfolioContainer,.blog-masonry');
        $container.isotope({
            filter: '*',
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false,
                resizesContainer: true
            }
        });
        // reveal all items after init
        var iso = $container.data('isotope');
        if (iso){
            $container.isotope( 'reveal', iso.items ).css({opacity: 1});
        }
        $('.portfolioFilter a').click(function(){
            $('.portfolioFilter .current').removeClass('current');
            $(this).addClass('current');
            var selector = $(this).attr('data-filter');
            $container.isotope({
                filter: selector,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
             });
             return false; 
        });    
        $container.isotope() 
    });    

    /* ------------------------------
    Accordion, Toggle, Tooltips, Tabs
    --------------------------------*/  
    $('#accordion,#accordion2').on('show.bs.collapse', function () {
        if (true) $('#accordion .in').collapse('hide');
    }); 
    $("[data-toggle='tooltip']").tooltip();  
    $(".alert").alert();
    $('#buttonTabs a,#iconTabs a').click(function (e) {
      e.preventDefault()
      $(this).tab('show')
    }); 
    
    /*--------------------
    Countdown Timers
    --------------------*/ 
    $('.countdown-timer').each(function() {
        var date = $(this).attr('data-date');
        $(this).countdown(date, function(event) {
            $(this).text(
                event.strftime('%D days %H:%M:%S')
            );
        });
    });   

    /* -------------------
    Back to top buttons
    ---------------------*/
    $('#back-to-top,.to-top').click(function() {
        $('html, body').animate({ scrollTop: 0}, 1000, 'easeInOutExpo');
        return false;
    });

    /*--------------------
    Hero Video
    --------------------*/
    $(function () { 
        var vid = document.getElementById("bgvid");
        var pauseButton = document.querySelector(".hero-video .play-pause-btn");
        function vidFade() {
            vid.classList.add("stopfade");
        } 
        if (pauseButton){
            pauseButton.addEventListener("click", function() {
                vid.classList.toggle("stopfade");
                if (vid.paused) {
                    vid.play();
                    pauseButton.innerHTML = "<i class='ion-pause'></i>";
                } else {
                    vid.pause();
                    pauseButton.innerHTML = "<i class='ion-play'></i>";
                }
            });
        }
    });  
    
})(jQuery);