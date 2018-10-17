"use strict;"

function imageControl(getImgButton, fileField, profileImage) {
    var fr = new FileReader();

    fileField.change(function (e) {
      var myFile = e.currentTarget.files[0];
      fr.addEventListener('load', function () {
        profileImage.attr('src', fr.result);
      });
      fr.readAsDataURL(myFile);
    });

    getImgButton.click(function() {
        fileField.click();
    });
}
