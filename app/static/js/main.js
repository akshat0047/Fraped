$(document).ready(function() {
  if (!($("#Depth").val() == "dh") || !($("#Depth").val() == "lopd")) {
    $("#Depth").prop("disabled", true);
  }

  $("#Extract").change(function() {
    let val = $(this).val();
    console.log(val);
    if (val == "dh" || val == "lopd") {
      $("#Depth").prop("disabled", false);
    } else {
      $("#Depth").prop("disabled", true);
    }
  });

  $("#scrapef").on("submit", function(e) {
    console.log("running ajax");
    $("#loader").css("display", "block");
    $("#scrape").css("display", "none");
    $.ajax({
      type: $(this).attr("method"),
      url: $(this).attr("action"),
      data: $("#scrapef").serialize(),
      success: function(res) {
        if (res.statusajax == "scraping") {
          console.log(res);
          console.log("ajax 2 fired");
            var results = setInterval(function() {
            $.ajax({
              type: "POST",
              url: "http://165.22.216.65:5000/extract/results",
              cache:false,
              success: function(response) {
                console.log(response);
                if (response.res == "finished") {
                  $("#show_results").submit();
                  clearInterval(results);
                }
              },
              error: function(err) {
                console.log(err);
              }
            });
          }, 4000);
        }
      },
      error: function(err) {
        console.log(err);
      }
    });
    e.preventDefault();
  });
});
