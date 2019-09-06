// Add exp parameter to exp URLs - takes the target page and object with key : values pairs object where key is a parameter and value is the value.
function urlRedirect(page, param, value) {

  window.location.href = page + "?" + param + "=" + value;

}

// Hide options based on input
jQuery(function($) {

  // Show different options depending on selections
  // Get determining input
  $("input[name='goal']").change(function() {

    // If selection is cardio, show cardio options and reset the value, else {
    // Show weight options and reset cardio value.
    var $sel = $(this).filter(function() {

      return $(this).prop("checked");
    });

    // Get this value of the selected option, if cardio, show cardio etc.
    if ($sel.val() == "cardio") {

      // Change display of both weight (hide) and cardio (show) options
      $(".cardioOptions").css("display", "block");
      $(".weightOptions").css("display", "none");

      // Change value on weight options
      $("input[type='radio'][name='group'][id*='def']").prop("checked", "checked");
    } else {

      // Change display of both weight and cardio options
      $(".cardioOptions").css("display", "none");
      $(".weightOptions").css("display", "block");

      // Change value on weight options
      $("input[type='radio'][name='cardio'][id*='def']").prop("checked", "checked");
    }

  });


});

// Activate/disable submit button until steps are all valid
jQuery(function($) {

  // Disable submit button function
  var disable = function() {
    // console.log("Disable");

    // Disable button
    $("input[type='submit']").attr("disabled", "disabled");

    // Add disabled styling
    $("input[type='submit']").addClass("disabled");
  };

  // Enable function
  var enable = function() {
    console.log("Enable");

    // Disable button
    $("input[type='submit']").removeAttr("disabled");

    // Remove disabled styling
    $("input[type='submit']").removeClass("disabled");
  };

  // Disable the button initially
  $("input[type='submit']").attr("disabled", "disabled");

  // On click of any radio button, check all buttons. If all needed buttons of
  // both cardio or weights are selected, enable submit button, else disable
  $("input:radio").change(function() {
    // console.log("Run");

    // Ensure the button starts disabled
    disable();

    console.log("Gear: ", $("input[name='gear']:checked").val());
    console.log("Goal: ", $("input[name='goal']:checked").val());
    console.log("Cardio: ", $("input[name='cardio']:checked").val());
    console.log("Group: ", $("input[name='group']:checked").val());

    // Check gear
    if (!["full", "basic", "gymless"].includes($("input[name='gear']:checked").val())) {
      console.log("Gear fail");
      // Invalid option so disable
      disable();
      return 1;
    }

    // Check goal
    if (!["low", "mix",
        "high", "cardio"].includes($("input[name='goal']:checked").val())) {
      console.log("Goal fail");
      // Invalid option so disable
      disable();
      return 1;
    }

    // Goal & group/cardio match up checks
    // Cardio selection
    if (
      ($("input[name='goal']:checked").val() == "cardio") &&
      (["hiit", "regular",
        "both"].includes($("input[name='cardio']:checked").val()))
        ) {
      console.log("Pass: Cardio");

      // Enable as valid cardio choice
      enable();
      return 1;

    } else if (
      (["low", "mix",
      "high"].includes($("input[name='goal']:checked").val())) &&
      (["chest", "back", "arms", "shoulders",
        "legs", "full", "core"].includes($("input[name='group']:checked").val()))
    ) {
      console.log("Pass: Weight");

      // Valid weight choice so enable
      enable();
      return 1;

    } else {
      console.log("Cardio / Goal mismatch Or Group / Goal Mismatch");

      // Invalid choices so disable
      disable();
      return 1;

    }

  });
});

// Change hidden field "sentiemnt" value depending on submit button - https://stackoverflow.com/questions/3797285/how-can-i-pass-a-parameter-via-submit-button
function setSent(val) {

  // Assign "sentiment" field in form to sentiment arg
  document.getElementById("sentiment").value = val;
}