const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const previewPanel = document.getElementById("previewPanel");
const preview = document.getElementById("preview");
const fileName = document.getElementById("fileName");
const predictBtn = document.getElementById("predictBtn");
const resetBtn = document.getElementById("resetBtn");
const againBtn = document.getElementById("againBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const errorBox = document.getElementById("error");
let selectedFile = null;

function chooseFile(file){
  if(!file || !file.type.startsWith("image/")) return showError("Please choose a JPG, JPEG or PNG image.");
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  fileName.textContent = file.name;
  dropZone.classList.add("hidden");
  result.classList.add("hidden");
  errorBox.classList.add("hidden");
  previewPanel.classList.remove("hidden");
}

function showError(msg){
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
  loading.classList.add("hidden");
}

fileInput.addEventListener("change", e => chooseFile(e.target.files[0]));
["dragenter","dragover"].forEach(ev => dropZone.addEventListener(ev, e => {e.preventDefault(); dropZone.classList.add("drag")}));
["dragleave","drop"].forEach(ev => dropZone.addEventListener(ev, e => {e.preventDefault(); dropZone.classList.remove("drag")}));
dropZone.addEventListener("drop", e => chooseFile(e.dataTransfer.files[0]));

async function analyze(){
  if(!selectedFile) return;
  previewPanel.classList.add("hidden");
  loading.classList.remove("hidden");
  errorBox.classList.add("hidden");
  const form = new FormData();
  form.append("file", selectedFile);
  try{
    const res = await fetch("/predict", {method:"POST", body:form});
    const data = await res.json();
    if(!res.ok) throw new Error(data.error || "Prediction failed.");
    document.getElementById("prediction").textContent = data.prediction.replaceAll("_"," ");
    document.getElementById("confidence").textContent = data.confidence + "%";
    document.getElementById("confidenceBar").style.width = data.confidence + "%";
    document.getElementById("topPredictions").innerHTML = data.top_predictions.map(p => `
      <div class="pred">
        <div>
          <div class="pred-name">${p.class.replaceAll("_"," ")}</div>
          <div class="pred-track"><span style="width:${p.confidence}%"></span></div>
        </div>
        <div class="pred-pct">${p.confidence}%</div>
      </div>`).join("");
    loading.classList.add("hidden");
    result.classList.remove("hidden");
  }catch(err){
    showError(err.message);
    previewPanel.classList.remove("hidden");
  }
}

function reset(){
  selectedFile = null;
  fileInput.value = "";
  result.classList.add("hidden");
  errorBox.classList.add("hidden");
  previewPanel.classList.add("hidden");
  loading.classList.add("hidden");
  dropZone.classList.remove("hidden");
}
predictBtn.addEventListener("click", analyze);
resetBtn.addEventListener("click", reset);
againBtn.addEventListener("click", reset);
