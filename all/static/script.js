document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("file");
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    // Debugging line: Log when the form is submitted
    console.log("Form submitted");

    // Create a FormData object and append the file
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Fetch the image and run object detection
    fetch("/upload", {
      method: "POST",
      body: formData
    })
    .then(response => {
      // Debugging line: Log the HTTP response status
      console.log("HTTP Response Status:", response.status);
      return response.json();
    })
    .then(data => {
      // Debugging line: Log the data received from the server
      console.log("Data received:", data);

      // Clear previous drawings
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw the image on the canvas
      let img = new Image();
      img.src = URL.createObjectURL(fileInput.files[0]);
      img.onload = function() {
        // Debugging line: Log when the image is loaded
        console.log("Image loaded");

        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height);

        // Debugging line: Log before drawing boxes
        console.log("Drawing boxes");

        // Draw the bounding boxes and labels
        for (const obj of data.result) {
          const [x, y, x2, y2] = obj.box;
          ctx.strokeStyle = "#FF0000";
          ctx.lineWidth = 2;
          ctx.strokeRect(x, y, x2 - x, y2 - y);

          ctx.fillStyle = "#FF0000";
          ctx.font = "24px Arial";
          const text = `${obj.label} (${Math.round(obj.confidence * 100)}%)`;
          ctx.fillText(text, x, y > 20 ? y - 5 : 20);
        }
      };
    })
    .catch(error => {
      // Debugging line: Log any errors
      console.error("Error:", error);
    });
  });
});
