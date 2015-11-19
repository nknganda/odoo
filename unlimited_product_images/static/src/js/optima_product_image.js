  function productImage(){
    var image = $('.optima_product_image');
    var settings = $('#optima_elevateZoom');
    image.elevateZoom({gallery:"optima_thumb",galleryActiveClass:"active",
        cursor: settings.attr("cursor"),
        zoomType: settings.attr("zoomType"),
        lensShape: settings.attr("lensShape"),
        lensSize: parseInt(settings.attr("lensSize")),
        zoomWindowWidth: parseInt(settings.attr("zoomWindowWidth")),
        zoomWindowHeight: parseInt(settings.attr("zoomWindowHeight")),
        zoomWindowFadeIn: parseInt(settings.attr("zoomWindowFadeIn")),
        zoomWindowFadeOut: parseInt(settings.attr("zoomWindowFadeOut")),
        lensFadeIn: parseInt(settings.attr("lensFadeIn")),
        lensFadeOut: parseInt(settings.attr("lensFadeOut")),
        easing: settings.attr("easing"),
        scrollZoom: settings.attr("scrollZoom"),
        tint: settings.attr("tint"),
        tintColour: settings.attr("tintColour"),
        tintOpacity: parseFloat(settings.attr("tintOpacity")),
        zoomWindowPosition: parseInt(settings.attr("zoomWindowPosition")),
        zoomWindowFadeIn:500,zoomWindowFadeOut:750});
  }
  $(document).ready(function() {
        productImage();
        //pass the images to box
        $(".optima_thumb_small").bind("mouseenter", function(e) {
            $(".optima_thumb_small").removeClass('active');
            $(this).addClass('active');
            $('.optima_product_image').attr("src", $(".active img").attr("src"));
            productImage();
            return false;
        });
  });

