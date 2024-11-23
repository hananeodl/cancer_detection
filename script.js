const uploadButton = document.getElementById("upload-button");
const analyseButton = document.getElementById("analyse-button");
const imageContainer = document.getElementById("image-container");
const result = document.querySelector('label');

let image;
uploadButton.addEventListener("click", () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      image = new Image();
      image.src = event.target.result;
      image.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = 224;
        canvas.height = 224;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(image, 0, 0, 224, 224);
        imageContainer.innerHTML = "";
        imageContainer.appendChild(canvas);
      };
    };
    reader.readAsDataURL(file);
  };
  input.click();
});

analyseButton.addEventListener("click", () => {
  if (image) {
    const formData = new FormData();
    formData.append("image", image);
    fetch("/analyze", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        result.innerText = ` ${data.result}`;
      });
  }
});



