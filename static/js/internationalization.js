$(document).ready(function () {
  var lang = sessionStorage.getItem("lang");

  console.log(lang);
  if (lang === null) {
    doLocalize("en");
  sessionStorage.setItem("lang", "en");
  } else {
    doLocalize(lang);
    $("#language").val(lang);
    console.log("localized " + lang);
  }
});
// $(function () {
//       var lang = sessionStorage.getItem("lang");

//       console.log(lang);
//       if (lang === null) {
//         doLocalize("en");
//       } else {
//         doLocalize(lang);
//         $("#language").val(lang);
//         console.log("localized " + lang);
//       }
//     });


function doLocalize(lang) {
  $("[data-localize]").localize("/static/internationalization/mylanguage", {
    language: lang
  });
}

$(document).on("change", "#language", function () {
  console.log("worked");
  var lang = $("#language  option:selected").val();
  sessionStorage.setItem("lang", lang);
  console.log(sessionStorage.getItem("lang"));
  doLocalize(lang);
});