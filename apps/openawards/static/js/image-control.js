"use strict;"

function imageControl(getImgButton, fileField, profileImage, callback) {
    var fr = new FileReader();

    fileField.change(function (e) {
      var myFile = e.currentTarget.files[0];
      fr.addEventListener('load', function () {
        profileImage.attr('src', fr.result);
        if (callback !== undefined) {
            callback();
        }
      });
      fr.readAsDataURL(myFile);
    });

    getImgButton.click(function() {
        fileField.click();
    });
}
