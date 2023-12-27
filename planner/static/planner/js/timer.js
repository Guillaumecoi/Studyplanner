let buttons = document.querySelectorAll(".btn");
let startBtn = document.getElementById("btn-start");
let reset = document.getElementById("btn-reset");
let pause = document.getElementById("btn-pause");
let stopBtn = document.getElementById("btn-stop");
let time = document.getElementById("time");
let set;
let count = 0;
let paused = true;
let minCount = 0;
let hourCount = 0;
let timespendField = document.getElementById("timeSpent");
time.textContent = `00:00`;

const appendZero = (value) => {
  value = value < 10 ? `0${value}` : value;
  return value;
};

pause.addEventListener(
  "click",
  (pauseTimer = () => {
    paused = true;
    clearInterval(set);
    startBtn.classList.remove("d-none");
    pause.classList.add("d-none");
  })
);

reset.addEventListener(
  "click",
  (resetTime = () => {
      pauseTimer();
      hourCount = 0;
      minCount = 0;
      count = 0;
      time.textContent = `${appendZero(minCount)}:${appendZero(count)}`;
  })
);

startBtn.addEventListener("click", () => {
  pause.classList.remove("d-none");
  startBtn.classList.add("d-none");
  if (paused) {
    paused = false;
    time.textContent = `${appendZero(minCount)}:${appendZero(count)}`;
    set = setInterval(() => {
      count++;
      if (count == 60) {
        minCount++;
        count = 0;
      }
      if (minCount == 60) {
        hourCount++;
        minCount = 0;
      }

      if (hourCount > 0) {
        time.textContent = `${appendZero(hourCount)}:${appendZero(minCount)}:${appendZero(count)}`;
      }
      else {
        time.textContent = `${appendZero(minCount)}:${appendZero(count)}`;
      }
    }, 1000);
  }
});

stopBtn.addEventListener("click", () => {
  // Stop the timer
  pauseTimer();

  // Calculate the total time spent in seconds
  let totalTimeSpent = hourCount * 3600 + minCount * 60 + count;

  // Initialize variable for current timespend in seconds
  let currentTimespendInSeconds = 0;

  // Check if the current value of timespend field is a valid time format
  if (timespendField.value.includes(":")) {
      let currentTimespend = timespendField.value.split(':').map(Number);
      currentTimespendInSeconds = currentTimespend[0] * 3600 + currentTimespend[1] * 60 + (currentTimespend[2] || 0);
  }

  // Add the new time to the current time
  let newTotalTimeSpent = totalTimeSpent + currentTimespendInSeconds;

  // Convert the total time spent to a timedelta string
  let hours = Math.floor(newTotalTimeSpent / 3600);
  let minutes = Math.floor((newTotalTimeSpent % 3600) / 60);
  let seconds = newTotalTimeSpent % 60;
  let timedeltaString = `${appendZero(hours)}:${appendZero(minutes)}:${appendZero(seconds)}`;

  // Set the value of the timespend field to the new timedelta string
  timespendField.value = timedeltaString;

  // Reset the timer
  resetTime();
});
