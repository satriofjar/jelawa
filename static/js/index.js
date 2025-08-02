// Function to show popUp island

async function showModal(id) {
    // Island name and description
    const islandName = document.querySelector("#island-name");
    const islandDesc = document.querySelector("#island-desc");
    const citiesWrapper = document.querySelector("#cities-wrapper");
    console.log(window.APP_CONFIG.apiBase);

    try {
        const response = await fetch(
            window.APP_CONFIG.apiBase + `/get-island/${id}`,
        );
        const data = await response.json();
        islandName.innerHTML = data.name;
        islandDesc.innerHTML = data.desc;

        const cities = document.querySelector("#cities");
        cities.innerHTML = "";
        for (let city of data.cities) {
            cities.innerHTML += `<div class="col-5 m-2" >
                                            <input type="radio" class="btn-check" name="city-name" id="${city.name}" value="${city.name}" autocomplete="off" ${data.cities.length == 1 ? "checked" : ""}>
                                            <label class="card btn btn-city border-0 py-2 text-center th-bg rounded-3" for="${city.name}">
                                                   ${city.name} 
                                            </label>
                                        </div>`;
        }

        citiesWrapper.style.display = data.cities.length == 1 ? "none" : "inline";

        const cardMap = document.querySelector(".card-map");
        cardMap.innerHTML = `<img src="${window.APP_CONFIG.imgBase}/img/${id.toLowerCase()}.svg" class="img-fluid" alt="Pulau ${id}" />`;
        const modal = new bootstrap.Modal(document.getElementById("modal-island"));
        modal.show();
    } catch (error) {
        console.error(error.message);
    }
}


const capitalize = (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1);
};

async function getQuestions(cityName) {
    try {
        const response = await fetch(
            window.APP_CONFIG.apiBase + `/get-questions/${cityName}`,
        );
        const data = await response.json();
        sessionStorage.setItem("quizQuestion", JSON.stringify(data));
        sessionStorage.removeItem("answers");
        return data;
    } catch (error) {
        console.error(error);
        return;
    }
}

function handleQuestion(questions, idx) {
    const numQuestions = document.querySelector("#num-questions");
    const question = document.querySelector("#question");
    const answers = document.querySelector("#answares");
    const progressBar = document.querySelector(".progress-bar");
    const nextPrev = document.querySelector("#next-prev");
    const imgContainer = document.querySelector("#img-container");

    numQuestions.innerHTML = `Question <span id="current-question">${idx + 1}</span> of ${questions.length}`;
    question.innerHTML = questions[idx].text;
    answers.innerHTML = "";
    if (questions[idx].img) {
        imgContainer.innerHTML = `<img
                                      src="${questions[idx].img}"
                                      alt=""
                                      class="img-fluid rounded shadow"
                                    />`;
    }

    let userAnswers = JSON.parse(sessionStorage.getItem("answers")) || [];

    let i = 65;
    for (let answer of questions[idx].answers) {
        const isActive = userAnswers[idx]?.answer == answer.id;
        answers.innerHTML += `<button id="${answer.id}" class="btn btn-answer btn-outline-secondary ${isActive ? "actv" : ""} text-start p-3" onclick="handleSelectAnswer(${idx}, ${answer.id})">
                                    ${String.fromCharCode(i)}. ${capitalize(answer.text)}
                                 </button>`;

        i += 1;
    }
    progressBar.style.width = `${(idx + 1 / questions.length) * 100}%`;

    // prev button
    const prevBtn = `<button
    id="btn-prev"
    class="btn btn-outline-secondary"
    ${idx <= 0 ? "disabled" : ""} 
    onclick="handleNextPrevQuestion(${idx - 1})">
      Previous
  </button>`;

    // next/finish button
    const isLast = idx >= questions.length - 1;
    const nextBtn = isLast
        ? `<button id="btn-next" class="btn btn-warning text-white  ${!userAnswers.find((a) => a.question == idx) ? "disabled" : ""}" onclick="handleResult()">Finish</button>`
        : `<button id="btn-next" class="btn btn-warning text-white ${!userAnswers.find((a) => a.question == idx) ? "disabled" : ""}" onclick="handleNextPrevQuestion(${idx + 1})">Next</button>`;

    nextPrev.innerHTML = prevBtn + nextBtn;
}

// Handle show quiz
async function showQuiz(cityName) {
    let questions = JSON.parse(sessionStorage.getItem("quizQuestion"));

    if (questions) {
        if (questions[0].city != cityName) {
            console.log("ga di sini");
            questions = await getQuestions(cityName);
        }
    } else {
        questions = await getQuestions(cityName);
    }
    handleQuestion(questions, 0);
    const quiz = document.querySelector("#quiz");
    quiz.style.display = "inline";

    setTimeout(() => {
        quiz.scrollIntoView({
            behavior: "smooth",
        });
    }, 10);
}
function handleSelectAnswer(questionId, answerId) {
    const btnNext = document.getElementById("btn-next");
    const answers = document.querySelectorAll(".btn-answer");
    answers.forEach((ans) => ans.classList.remove("actv"));

    const answer = document.getElementById(answerId);
    if (answer) answer.classList.add("actv");

    let userAnswers = JSON.parse(sessionStorage.getItem("answers")) || [];

    if (userAnswers) {
        const index = userAnswers.findIndex((ans) => ans.question === questionId);
        if (index !== -1) {
            userAnswers[index].answer = answerId;
        } else {
            userAnswers.push({ question: questionId, answer: answerId });
        }
    }
    btnNext.classList.remove("disabled");

    sessionStorage.setItem("answers", JSON.stringify(userAnswers));
}
// Handle next question button
function handleNextPrevQuestion(index) {
    const questions = JSON.parse(sessionStorage.getItem("quizQuestion"));
    handleQuestion(questions, index);
}

// Handle result quiz
function handleResult() {
    const quizResult = document.querySelector("#quiz-result");
    const quizScoreRes = document.querySelector("#quiz-score-res");
    const quizScore = document.querySelector("#quiz-score");
    const feedBack = document.querySelector("#feed-back");

    const questions = JSON.parse(sessionStorage.getItem("quizQuestion"));
    const answers = JSON.parse(sessionStorage.getItem("answers"));
    let res = 0;

    answers.forEach((ans) => {
        const quest = questions[ans.question];

        const answer = quest.answers.find((a) => a.id == ans.answer);

        if (answer.is_correct) {
            res += 1;
        }
    });

    quizScoreRes.innerHTML = `${res}/${questions.length}`;
    quizScore.innerHTML = `You scored ${res} out of ${questions.length}!`;

    const feedbacks = ["Belajar lagi ya!!", "Tingkatkan terus!!", "Perfect!!"];
    if (res < 5) {
        feedBack.innerHTML = feedbacks[0];
    } else if (res < 7) {
        feedBack.innerHTML = feedbacks[1];
    } else {
        feedBack.innerHTML = feedbacks[2];
    }

    sessionStorage.removeItem("answers");
    quizResult.style.display = "inline";

    setTimeout(() => {
        quizResult.scrollIntoView({
            behavior: "smooth",
        });
    }, 10);
}

function handleRetakeQuiz(cityName) {
    const quizResult = document.querySelector("#quiz-result");
    quizResult.style.display = "none";
    const answers = document.querySelectorAll(".btn-answer");
    answers.forEach((ans) => ans.classList.remove("actv"));
    showQuiz(cityName);
}
