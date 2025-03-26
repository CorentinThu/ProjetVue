$(function() {
  const BASE_URL = "http://127.0.0.1:5000/api";
  let editType = "";

  $("#btnGetQuiz").click(refreshListeQuestionnaires);

  function refreshListeQuestionnaires() {
    fetch(`${BASE_URL}/questionnaires`)
      .then(response => {
        if (!response.ok) throw new Error(`Erreur GET questionnaires : ${response.status}`);
        return response.json();
      })
      .then(quizArray => {
        afficherQuiz(quizArray);
      })
      .catch(err => {
        console.error(err);
        $("#quizList").html(`<b>Impossible de récupérer les quiz</b> (${err.message})`);
      });
  }

  function afficherQuiz(quizArray) {
    $("#quizList").empty();
    const ul = $("<ul>");

    quizArray.forEach(q => {
      const li = $("<li>");
      li.append(`<b>Quiz #${q.id}</b> : ${q.name} (${q.questions.length} questions) `);

      const btnEditQz = $("<button>").text("Modifier ce quiz");
      btnEditQz.click(() => {
        editType = "quiz";
        $("#editId").val(q.id);
        $("#editText").val(q.name);
        $("#editAnswerContainer").hide();
        $("#editSection").show();
      });
      li.append(btnEditQz);

      const btnDelQz = $("<button>").text("Supprimer ce quiz");
      btnDelQz.click(() => {
        supprimerQuestionnaire(q.id);
      });
      li.append(btnDelQz);

      if (q.questions.length > 0) {
        const subUl = $("<ul>");
        q.questions.forEach(question => {
          const subLi = $("<li>").text(`Q${question.id} [${question.type}] : ${question.title} (Réponse: ${question.answer || "N/A"}) `);

          const btnEditQuest = $("<button>").text("Modifier question");
          btnEditQuest.click(() => {
            editType = "question";
            $("#editId").val(question.id);
            $("#editText").val(question.title);
            $("#editAnswerContainer").show();
            $("#editAnswer").val(question.answer);
            $("#editSection").show();
          });
          subLi.append(btnEditQuest);

          const btnDelQuest = $("<button>").text("Suppr. question");
          btnDelQuest.click(() => {
            supprimerQuestion(question.id);
          });
          subLi.append(btnDelQuest);

          subUl.append(subLi);
        });
        li.append(subUl);
      }

      ul.append(li);
    });

    $("#quizList").append(ul);
  }

  function createQuiz() {
    const quizName = $("#newQuizName").val().trim();
    if (!quizName) {
      alert("Veuillez saisir un nom de quiz");
      return;
    }
    const payload = { name: quizName };

    fetch(`${BASE_URL}/questionnaires`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (!response.ok) throw new Error(`Erreur création quiz: ${response.status}`);
        return response.json();
      })
      .then(newQuiz => {
        console.log("Quiz créé:", newQuiz);
        alert(`Quiz créé avec l'ID: ${newQuiz.id}`);
        $("#newQuizName").val("");
        refreshListeQuestionnaires();
      })
      .catch(err => {
        console.error(err);
        alert("Erreur: " + err.message);
      });
  }

  function createQuestion() {
    const qId = parseInt($("#newQuestionQId").val(), 10);
    const title = $("#newQuestionTitle").val().trim();
    const type = $("#newQuestionType").val();
    const answer = $("#newQuestionAnswer").val().trim();
    if (!qId || !title) {
      alert("Veuillez saisir l'ID du questionnaire et un titre.");
      return;
    }
    const payload = {
      questionnaire_id: qId,
      title: title,
      type: type,
      answer: answer
    };

    fetch(`${BASE_URL}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (!response.ok) throw new Error(`Erreur création question: ${response.status}`);
        return response.json();
      })
      .then(newQuestion => {
        console.log("Question créée:", newQuestion);
        alert(`Question créée, ID: ${newQuestion.id}`);
        $("#newQuestionQId").val("");
        $("#newQuestionTitle").val("");
        $("#newQuestionAnswer").val("");
        refreshListeQuestionnaires();
      })
      .catch(err => {
        console.error(err);
        alert("Il n'existe pas de questionnaire avec cet ID.");
      });
  }

  $("#addQuiz").click(() => {
    console.log("Icône d'ajout de quiz cliquée");
    createQuiz();
  });

  $("#delQuiz").click(() => {
    $("#newQuizName").val("");
  });

  $("#addQuestion").click(() => {
    console.log("Icône d'ajout de question cliquée");
    createQuestion();
  });

  $("#delQuestion").click(() => {
    $("#newQuestionQId").val("");
    $("#newQuestionTitle").val("");
    $("#newQuestionAnswer").val("");
  });

  function supprimerQuestionnaire(qId) {
    fetch(`${BASE_URL}/questionnaires/${qId}`, {
      method: "DELETE"
    })
      .then(response => {
        if (!response.ok) throw new Error(`Erreur suppression questionnaire: ${response.status}`);
        return response.json();
      })
      .then(data => {
        console.log("Questionnaire supprimé:", data);
        refreshListeQuestionnaires();
      })
      .catch(err => {
        console.error(err);
        alert("Erreur: " + err.message);
      });
  }

  function supprimerQuestion(questionId) {
    fetch(`${BASE_URL}/questions/${questionId}`, {
      method: "DELETE"
    })
      .then(response => {
        if (!response.ok) throw new Error(`Erreur suppression question: ${response.status}`);
        return response.json();
      })
      .then(data => {
        console.log("Question supprimée:", data);
        refreshListeQuestionnaires();
      })
      .catch(err => {
        console.error(err);
        alert("Erreur: " + err.message);
      });
  }

  $("#btnUpdate").click(() => {
    const id = $("#editId").val();
    const newText = $("#editText").val().trim();
    const newAnswer = $("#editAnswer").val().trim();

    if (!id || !newText) {
      alert("ID et texte sont obligatoires.");
      return;
    }

    let payload = {};
    let url = "";
    
    if (editType === "quiz") {
      payload = { name: newText };
      url = `${BASE_URL}/questionnaires/${id}`;
    } else if (editType === "question") {
      payload = { title: newText, answer: newAnswer };
      url = `${BASE_URL}/questions/${id}`;
    } else {
      alert("Type d'édition inconnu.");
      return;
    }
  
    fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(response => {
        if (!response.ok) throw new Error(`Erreur modification: ${response.status}`);
        return response.json();
      })
      .then(data => {
        alert("Modification effectuée.");
        $("#editSection").hide();
        refreshListeQuestionnaires();
      })
      .catch(err => {
        console.error(err);
        alert("Erreur: " + err.message);
      });
  });

  $("#btnCancelUpdate").click(() => {
    $("#editSection").hide();
  });
});
