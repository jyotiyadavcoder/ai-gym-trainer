const video = document.getElementById("video");
const placeholder = document.getElementById("placeholder");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const summary = document.getElementById("summary");
const exerciseSelect = document.getElementById("exerciseSelect");
const sideSelect = document.getElementById("sideSelect");
const title = document.getElementById("exerciseTitle");
const hint = document.getElementById("exerciseHint");

const HINTS = {
    bicep_curl: "Stand sideways, arm towards the camera, full arm visible",
    squat: "Stand sideways to the camera so your whole body is visible",
    pushup: "Place the camera at the side, so your full body is visible",
};

let pollTimer = null;

function updateTitle() {
    title.textContent = exerciseSelect.options[exerciseSelect.selectedIndex].text;
    hint.textContent = HINTS[exerciseSelect.value];
}
exerciseSelect.addEventListener("change", updateTitle);
updateTitle();

function setControls(running) {
    startBtn.disabled = running;
    stopBtn.disabled = !running;
    exerciseSelect.disabled = running;
    sideSelect.disabled = running;
}

async function updateStats() {
    try {
        const res = await fetch("/stats");
        const s = await res.json();
        document.getElementById("reps").textContent = s.reps;
        document.getElementById("stage").textContent = s.stage;
        document.getElementById("angle").textContent = s.angle;
        document.getElementById("elapsed").textContent = s.elapsed;
        document.getElementById("feedback").textContent = s.feedback;
    } catch (err) {
        console.error("Stats error:", err);
    }
}

startBtn.addEventListener("click", async () => {
    summary.textContent = "";
    await fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            exercise: exerciseSelect.value,
            side: sideSelect.value,
        }),
    });

    video.src = "/video_feed?t=" + Date.now();
    video.style.display = "block";
    placeholder.style.display = "none";

    setControls(true);
    pollTimer = setInterval(updateStats, 500);
});

stopBtn.addEventListener("click", async () => {
    clearInterval(pollTimer);
    const res = await fetch("/stop", { method: "POST" });
    const data = await res.json();

    video.src = "";
    video.style.display = "none";
    placeholder.style.display = "flex";
    placeholder.textContent = "Workout finished. Choose an exercise and press Start.";

    if (data.result) {
        let msg = `${data.result.exercise}: ${data.result.reps} reps in ${data.result.duration} seconds`;
        if (data.saved) {
            msg += ` | ${data.result.calories} kcal saved to history`;
        } else if (data.result.reps === 0) {
            msg += " | No reps, so nothing was saved";
        } else {
            msg += " | Could not save to database";
        }
        summary.textContent = msg;
    }
    setControls(false);
    updateStats();
});