function check() {
    let output = document.getElementById("dias")

    let startDate = new Date(document.getElementById("inicio").value);
    let endDate = new Date(document.getElementById("fin").value);

    if (startDate.getTime() && endDate.getTime()) {
      let timeDifference = endDate.getTime() - startDate.getTime();

      let dayDifference = Math.abs(timeDifference / (1000 * 3600 * 24));
      output.value =  dayDifference

    } else {
      output.value = 0;
    }
  };
  document.querySelector('#inicio').addEventListener("change", check, false);
  document.querySelector('#fin').addEventListener("change", check, false);
